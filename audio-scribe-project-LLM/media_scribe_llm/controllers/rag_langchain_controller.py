from fastapi import HTTPException, Form
import tempfile
import pickle
from services.mongo_client_service import Mongo_Client
import io
from services.rag_langchain_service import Rag_LangChain
from services.azure_storage_service import Azure_Storage
from services.vector_store_service import Vector_Store
import os

rag_chain: Rag_LangChain


async def create_new_session_chat(media_path: str = Form(...)):
    client = Mongo_Client(os.getenv("MONGO_URI"))
    new_session = client.create_session(media_path)

    return new_session


async def get_all_sessions_chat():
    client = Mongo_Client(os.getenv("MONGO_URI"))
    new_session = client.get_all_sessions()

    return new_session


async def get_sessions_chat(session_id: str):
    client = Mongo_Client(os.getenv("MONGO_URI"))
    new_session = client.get_session_messages(session_id)

    return new_session


async def open_session_chat(items):
    global rag_chain
    client = Mongo_Client(os.getenv("MONGO_URI"))
    media_path = client.get_session_knowledge(items.session_id)

    storage = Azure_Storage(
        os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
        os.getenv("AZURE_BLOB_STORAGE_KEY"),
        os.getenv("AZURE_BLOB_STORAGE_NAME"),
    )

    _, _, vector_store = storage.get_folder_files(media_path)

    with io.BytesIO(vector_store.readall()) as f:
        vector_store_pkl = pickle.load(f)

    rag_chain = Rag_LangChain(
        os.getenv("OPENAI_API_KEY"), vector_store_pkl, client, media_path
    )

    return "ok"


async def send_prompt(items):
    try:

        global rag_chain

        result = rag_chain.invoke_and_save(
            items.session_id,
            items.question,
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interval server error {e}")


async def index_knowledge_info(item):
    try:

        client = Mongo_Client(os.getenv("MONGO_URI"))

        media_path = item.media_path

        storage = Azure_Storage(
            os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
            os.getenv("AZURE_BLOB_STORAGE_KEY"),
            os.getenv("AZURE_BLOB_STORAGE_NAME"),
        )

        text_files, image_files, _ = storage.get_folder_files(media_path, True)

        image_files_content = storage.create_images_file_content(image_files)

        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8"
        ) as temp_file:
            temp_file.write(text_files)
            temp_file_path = temp_file.name

        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8", suffix=".txt"
        ) as temp_file:
            temp_file.write(image_files_content)
            temp_file_path_image = temp_file.name

        vector_store = Vector_Store(
            [temp_file_path_image, temp_file_path]
        ).create_vector_store()

        vector_store_path = f"{media_path}/vector_store/vector_store.pkl"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as temp_file:
            pickle.dump(vector_store, temp_file)
            temp_vector_file_path = temp_file.name

        storage.upload_file(vector_store_path, temp_vector_file_path)
        client.update_index(media_path)
        return "ok"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interval server error {e}")

    finally:
        os.remove(temp_file_path_image)
        os.remove(temp_file_path)
