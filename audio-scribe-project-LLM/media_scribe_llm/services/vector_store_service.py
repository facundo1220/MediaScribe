from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


class Vector_Store:
    def __init__(self, files):
        self.files = files

    def create_vector_store(self):
        all_docs = []

        for file_path in self.files:
            loader = TextLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(all_docs)
        # vector_store = Chroma.from_documents(
        #    documents=splits, embedding=OpenAIEmbeddings()
        # )

        return splits
