from fastapi import APIRouter, UploadFile, Form
from controllers.speaker_detection_controller import (
    detect_speaker,
    save_speaker_detection,
)

router = APIRouter()


@router.post("/speaker_detection", tags=["speaker_detection"])
async def speaker_detection(file: UploadFile, intervals: str = Form(...)):
    value = await detect_speaker(file, intervals)
    return [{"message": f"{value}"}]


@router.post("/save_detection", tags=["speaker_detection"])
async def save_detection(file: UploadFile, intervals: str = Form(...)):
    value = await save_speaker_detection(file, intervals)
    return [{"message": f"{value}"}]
