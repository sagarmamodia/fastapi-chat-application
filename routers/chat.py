from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException,
    status,
    Form,
    Body,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect
)
from fastapi.templating import Jinja2Templates
import config
import models
from sqlmodel import Session, select, col
from database import get_session
from typing import Annotated
import connection_manager as cm
import schemas
import json

router = APIRouter(
    tags=["Chat"]
)
templates = Jinja2Templates(directory=config.TEMPLATES_PATH)

manager = cm.ConnectionManager()

@router.post('/chat')
def chat(request: Request,
            username: str,
            session: Annotated[Session, Depends(get_session)]
):
    users_list = session.exec(select(models.User).where(models.User.username != username)).all()
    usernames_list = [user.username for user in users_list]

    return templates.TemplateResponse(
        request=request, name="chat.html", context={"username": username, "users": usernames_list}
    )

@router.post('/chat/chats', response_model=schemas.AllChatsResponse)
async def all_chats(
    chats_request: schemas.AllChatsRequest,
    session: Annotated[Session, Depends(get_session)]
):
    sender = chats_request.sender
    receiver = chats_request.receiver
    chats = session.exec( select(models.Chat).where(((models.Chat.sender==receiver) & (models.Chat.receiver==sender)) | ((models.Chat.sender==sender) & (models.Chat.receiver==receiver) ) )).all()
    chats = [chat.dict() for chat in chats]
    print(len(chats))
    return schemas.AllChatsResponse(chats=chats);
    # return {"response": "It worked"}

@router.websocket('/ws/chat/{username}')
async def websocket_endpoint(
    websocket: WebSocket,
    username: str,
    session: Annotated[Session, Depends(get_session)]
):
    user = cm.User(username, websocket)
    await manager.connect(user)
    try:
        while True:
            json_str = await websocket.receive_text()
            chat_dict = json.loads(json_str)
            print(chat_dict)
            chat = schemas.Chat(sender=chat_dict['sender'],
                                receiver=chat_dict['receiver'],
                                message=chat_dict['message']
                            )
            session.add(models.Chat(sender=chat.sender, receiver=chat.receiver, message=chat.message))
            session.commit()
            print("message added to the database")
            await manager.send_personal_message(chat)

    except WebSocketDisconnect:
        manager.disconnect(user)
        # await manager.broadcast("system", f'{user.username} left the chat')
