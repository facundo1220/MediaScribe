from fastapi import APIRouter, Form
from pydantic import BaseModel
from controllers.rag_langchain_controller import (
    send_prompt,
    index_knowledge_info,
    create_new_session_chat,
    get_all_sessions_chat,
    get_sessions_chat,
    open_session_chat,
)

router = APIRouter()


class Item(BaseModel):
    media_path: str


class ItemPrompt(BaseModel):
    session_id: str
    question: str


class ItemInitChat(BaseModel):
    session_id: str


@router.post("/send_prompt_user_langchain", tags=["rag_langchain"])
async def send_prompt_langchain(item: ItemPrompt):
    value = await send_prompt(item)
    return {f"message": f"{value}"}


@router.post("/index_knowledge", tags=["index_knowledge"])
async def index_knowledge_data(item: Item):
    value = await index_knowledge_info(item)
    return {f"message": f"{value}"}


@router.post("/new_session", tags=["new_session"])
async def new_session_chat(media_path: str = Form(...)):
    value = await create_new_session_chat(media_path)
    return {f"message": f"{value}"}


@router.post("/open_session", tags=["new_session"])
async def new_session_chat(item: ItemInitChat):
    value = await open_session_chat(item)
    return {f"message": f"{value}"}


@router.get("/get_all_session", tags=["new_session"])
async def all_session_chat():
    value = await get_all_sessions_chat()
    return {f"message": f"{value}"}


@router.get("/get_session_messages/{session_id}", tags=["new_session"])
async def session_chat(session_id: str):
    value = await get_sessions_chat(session_id)
    return {f"message": f"{value}"}
