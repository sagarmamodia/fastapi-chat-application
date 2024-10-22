from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
import sys
sys.path.append('routers/')
import authentication
import chat

app = FastAPI()
app.include_router(authentication.router)
app.include_router(chat.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
