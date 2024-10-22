from fastapi import WebSocket
import json
import schemas

class User:
    def __init__(self, username: str, websocket: WebSocket):
        self.username = username
        self.websocket = websocket

class ConnectionManager():
    def __init__(self):
        self.active_users: list[User] = []

    async def connect(self, user: User):
        await user.websocket.accept()
        self.active_users.append(user)

    def disconnect(self, user: User):
        self.active_users.remove(user)

    async def send_personal_message(self, chat: schemas.Chat):
        chat_json = json.dumps({
            "sender": chat.sender,
            "receive": chat.receiver,
            "message": chat.message
        })
        for user in self.active_users:
            if(user.username==chat.receiver):
                await user.websocket.send_text(chat_json)
                break

    # async def broadcast(self, username: str, message: str):
    #     data = json.dumps({"username": username, "message": message})
    #     for user in self.active_users:
    #         if user.username != username:
    #             await user.websocket.send_text(data)
