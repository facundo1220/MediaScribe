from fastapi import APIRouter, UploadFile
from controllers.diarization_controller import (
    extract_diarization_from_media,
    extract_text_from_media,
    save_diarization,
    load_all_knoledges,
)

router = APIRouter()


@router.post("/extract_diarization_from_media", tags=["diarization"])
async def extract_diarization(file: UploadFile):
    value = await extract_diarization_from_media(file)
    return {"message": f"{value}"}


@router.post("/extract_text_from_media", tags=["diarization"])
async def extract_text(file: UploadFile):
    value = await extract_text_from_media(file)
    return [{"message": f"{value}"}]


@router.post("/save_diarization_azure", tags=["diarization"])
async def save_diarization_azure(file: UploadFile):
    value = await save_diarization(file)
    return {"message": f"{value}"}


@router.get("/get_all_knoledges", tags=["diarization"])
async def get_knoledges():
    value = await load_all_knoledges()
    return {"message": f"{value}"}
