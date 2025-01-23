from fastapi import FastAPI
from routes.diarization_routes import router as diarization_router
from routes.speaker_detection_routes import router as speaker_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()
origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(diarization_router, prefix="/diarization", tags=["diarization"])
app.include_router(speaker_router, prefix="/speaker", tags=["speaker"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the MediaScribe API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
