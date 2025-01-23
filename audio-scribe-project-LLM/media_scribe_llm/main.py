from fastapi import FastAPI
from routes.rag_langchain_route import router as langchain_router
import uvicorn

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(langchain_router, prefix="/langchain_rag", tags=["langchain_rag"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the MediaScribe LLM API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
