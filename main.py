# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union
import sys
import os
import config
from fastapi import (
    Cookie,
    Request,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
    Form
)
import json
from connection_manager import ConnectionManager, User

app = FastAPI()

templates = Jinja2Templates(directory=config.TEMPLATES_PATH)

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

manager = ConnectionManager()

@app.post('/join')
def join_chat(request: Request, username: Union[str, None] = Form()):
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"username": username}
    )

@app.websocket('/ws/{username}')
async def websocket_endpoint(
    websocket: WebSocket,
    username: str
):
    user = User(username, websocket)
    await manager.connect(user)
    await manager.broadcast("system", f'{username} joined the chat.')
    try:
        while True:
            message = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", user)
            await manager.broadcast(username, message)

    except WebSocketDisconnect:
        manager.disconnect(user)
        await manager.broadcast("system", f'{user.username} left the chat')
