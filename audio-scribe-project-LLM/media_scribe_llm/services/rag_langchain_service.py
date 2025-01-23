from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from operator import itemgetter
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable
from services.azure_storage_service import Azure_Storage
import os
from langchain.tools import BaseTool


media_path: str


class SpeakerTool(BaseTool):
    name = "returnPhoto"
    description = "use this tool when the user request the photo of a speaker"

    def _run(self, speaker):
        global media_path

        storage = Azure_Storage(
            os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
            os.getenv("AZURE_BLOB_STORAGE_KEY"),
            os.getenv("AZURE_BLOB_STORAGE_NAME"),
        )

        _, img, _ = storage.get_folder_files(media_path)

        img_path = [item for item in img if speaker in item][0]

        image_url = storage.get_image_url(img_path)

        return image_url


class Rag_LangChain:
    def __init__(self, api_key, vector_store, mongo_client, media):
        global media_path
        media_path = media

        self.mongo_client = mongo_client

        # create the llm
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=api_key)

        self.tools = [SpeakerTool()]
        self.llm_with_tools = llm.bind_tools(self.tools)

        self.vectorstore = Chroma.from_documents(
            documents=vector_store, embedding=OpenAIEmbeddings()
        )
        self.retriever = self.vectorstore.as_retriever()

        # create de contextualize system prompt
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm_with_tools, self.retriever, contextualize_q_prompt
        )
        # Answer the question from RAG
        qa_system_prompt = """You are an assistant for answering questions based on text extracted from a video or audio.\
        All questions will relate to the content of the provided text, which is a transcription of the video or audio.\
        You may receive questions like "What is the video about?" or specific details about the content. \
        If you don't know the answer, just say that you don't know. \
        Use four sentences maximum and keep the answer concise.\

        {context}"""

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        # question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        # rag_chain = create_retrieval_chain(
        #    history_aware_retriever, question_answer_chain
        # )

        # self.conversational_rag_chain = RunnableWithMessageHistory(
        #    rag_chain,
        #    self.get_session_history,
        #    input_messages_key="input",
        #    history_messages_key="chat_history",
        #    output_messages_key="answer",
        # )

        ## chain with tools

        self.rag_chain = (
            {
                "context": history_aware_retriever,
                "input": itemgetter("input"),
                "chat_history": itemgetter("chat_history"),
            }
            | qa_prompt
            | self.llm_with_tools
        )

        # self.store = {}

    # def load_session_history(self, session_id: str) -> BaseChatMessageHistory:
    #    chat_history = ChatMessageHistory()
    #    session = self.mongo_client.get_session_history(session_id)
    #    if session:
    #        for message in session:
    #            chat_history.add_message(
    #                {"role": message["role"], "content": message["content"]}
    #            )

    #    return chat_history

    def load_session_history(self, session_id: str) -> List:
        chat_history = []
        session = self.mongo_client.get_session_history(session_id)
        if session:
            for message in session:
                chat_history.extend([HumanMessage(content=message[0]), message[1]])

        return chat_history

    # def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
    #    try:
    #        if session_id not in self.store:
    #            self.store[session_id] = self.load_session_history(session_id)
    #        return self.store[session_id]
    #    except Exception as e:
    #        print(f"error get_session_history: {e}")

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        try:
            session_history = self.load_session_history(session_id)

            return session_history
        except Exception as e:
            print(f"error get_session_history: {e}")

    @tool
    def returnPhoto(speaker: str) -> str:
        "browse a speaker"

        global media_path

        storage = Azure_Storage(
            os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
            os.getenv("AZURE_BLOB_STORAGE_KEY"),
            os.getenv("AZURE_BLOB_STORAGE_NAME"),
        )

        _, img, _ = storage.get_folder_files(media_path)

        img_path = [item for item in img if speaker in item][0]

        image_url = storage.get_image_url(img_path)

        return image_url

    def call_tools(self, msg: AIMessage) -> Runnable:
        tool_map = {tool.name: tool for tool in self.tools}
        tool_calls = msg.tool_calls.copy()
        for tool_call in tool_calls:
            tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])
        return tool_calls

    def invoke_and_save(self, session_id, input_text):
        try:

            result = self.rag_chain.invoke(
                {
                    "input": input_text,
                    "chat_history": self.get_session_history(session_id),
                }
            )

            tools = self.call_tools(result)

            if tools:

                response = f"Calling tool {tools[0]['name']}...<{tools[0]['output']}>"

                self.mongo_client.add_message(
                    session_id,
                    input_text.replace("'", ""),
                    response,
                )

                return response

            else:
                self.mongo_client.add_message(
                    session_id,
                    input_text.replace("'", ""),
                    result.content.replace("'", ""),
                )

                return result.content
        except Exception as e:
            print(f"error invoke_and_save: {e}")
