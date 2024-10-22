from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class Chat(BaseModel):
    sender: str
    receiver: str
    message: str
    # timestamp: timestamp

class AllChatsResponse(BaseModel):
    chats: list[Chat]

class AllChatsRequest(BaseModel):
    sender: str
    receiver: str
