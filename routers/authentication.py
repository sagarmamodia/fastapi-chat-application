from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import config
from sqlmodel import Session, select
from database import get_session
from typing import Annotated
import models

router = APIRouter(
    tags=["signin/signup"]
)

templates = Jinja2Templates(directory=config.TEMPLATES_PATH)

@router.get('/')
async def index(request: Request, session: Annotated[Session, Depends(get_session)]):
    # users_list = session.exec(select(models.User)).all()
    # print(users_list)
    return templates.TemplateResponse(
        request=request, name="authentication.html"
    )

@router.post('/signin')
async def signin(request: Request,
        username: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(models.User).where(models.User.username==username)).first()
    if not user:
        return templates.TemplateResponse(
            request=request, name="response.html", context={"response": f'User with username "{username}" does not exist.'}
        )

    if(user.password!=password):
        return templates.TemplateResponse(
            request=request, name="response.html", context={"response": "Invalid username and password"}
        )

    return RedirectResponse(f'/chat?username={username}')

@router.post('/signup')
def signup(
    request:Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(models.User).where(models.User.username==username)).all()
    if user:
        return templates.TemplateResponse(
            request=request, name="response.html", context={"response": "username already exists, please signin"}
        )

    session.add(models.User(username=username, email=email, password=password))
    session.commit()

    return templates.TemplateResponse(
        request=request, name="response.html", context={"response": "your account has been successfully created, please signin"}
    )
