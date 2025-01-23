from fastapi import HTTPException, UploadFile
from services.diarization_service import Diarizator
from services.azure_storage_service import Azure_Storage
from tempfile import NamedTemporaryFile
import os
from services.mongo_client_service import Mongo_Client
import mimetypes


async def extract_diarization_from_media(file: UploadFile):
    try:
        diarizator = Diarizator(file)

        value = diarizator.extract_diarization_result()
        return value
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


async def extract_text_from_media(file: UploadFile):
    try:
        diarizator = Diarizator(file)

        value = diarizator.extract_text_data()
        return value
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


async def save_diarization(file: UploadFile):
    try:

        client = Mongo_Client(os.getenv("MONGO_URI"))

        file_name = os.path.splitext(file.filename)[0]
        type_file, _ = mimetypes.guess_type(file.filename)
        upload_file_path = f"{file_name}_extraction/{file_name}.txt"
        diarizator = Diarizator(file)

        diarization_value = diarizator.extract_diarization_result()

        formatted_text = diarizator.format_diarization_text(diarization_value)

        with NamedTemporaryFile(
            delete=False, mode="w", suffix=".txt", prefix=f"{file_name}_"
        ) as temp_file:
            temp_file.write(formatted_text)
            temp_file_path = temp_file.name

        storage = Azure_Storage(
            os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
            os.getenv("AZURE_BLOB_STORAGE_KEY"),
            os.getenv("AZURE_BLOB_STORAGE_NAME"),
        )

        storage.upload_file(upload_file_path, temp_file_path)

        client.create_knowledge(file_name, type_file)

        return diarization_value

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")

    finally:
        os.remove(temp_file_path)


async def load_all_knoledges():

    try:
        client = Mongo_Client(os.getenv("MONGO_URI"))

        knowledges = client.get_all_knowledges()

        return knowledges

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
