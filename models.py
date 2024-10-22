from sqlmodel import Field, Session, SQLModel
from typing import Union

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    email: Union[str, None] = Field(default=None, index=True)
    password: str = Field()

class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    sender: str = Field()
    receiver: str = Field()
    message: str = Field()
