from fastapi import WebSocket
import json

class User:
    def __init__(self, username: str, websocket: WebSocket):
        self.username = username
        self.websocket = websocket

class ConnectionManager():
    def __init__(self):
        self.active_connections: list[User] = []

    async def connect(self, user: User):
        await user.websocket.accept()
        self.active_connections.append(user)

    def disconnect(self, user: User):
        self.active_connections.remove(user)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, username: str, message: str):
        data = json.dumps({"username": username, "message": message})
        for user in self.active_connections:
            if user.username != username:
                await user.websocket.send_text(data)
