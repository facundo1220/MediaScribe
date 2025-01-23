from fastapi import HTTPException, UploadFile, Form
from services.speaker_detection_service import Speaker_Detector
from services.azure_storage_service import Azure_Storage
import os
import re


async def detect_speaker(file: UploadFile, intervals: str = Form(...)):
    try:

        Detector = Speaker_Detector(file, intervals)
        return Detector.process_video()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")


async def save_speaker_detection(file: UploadFile, intervals: str = Form(...)):
    try:

        file_name = os.path.splitext(file.filename)[0]
        upload_file_path = f"{file_name}_extraction/{file_name}.txt"

        Detector = Speaker_Detector(file, intervals)

        speakers_images = Detector.process_video()

        storage = Azure_Storage(
            os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STR"),
            os.getenv("AZURE_BLOB_STORAGE_KEY"),
            os.getenv("AZURE_BLOB_STORAGE_NAME"),
        )

        for image in speakers_images:
            match = re.search(r"SPEAKER_\d+", image)
            speaker_part = match.group(0)
            upload_file_path = (
                f"{file_name}_extraction/speakers_images/{speaker_part}.jpg"
            )

            storage.upload_file(upload_file_path, image)

        return "ok"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
