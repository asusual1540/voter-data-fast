from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.api.user.user_model import SystemUser, TokenSchema, User, UserAuthRequest, UserOut
from app.core.vdm import vdm

userRouter = APIRouter()
service = vdm.user_service
authentication_service = vdm.authentication_service


@userRouter.post('/signup', summary="Create new user")
async def create_user(data: UserAuthRequest):
    # querying database to check if user already exist
    try:
        return service.signup_user(data.username, data.password)
    except HTTPException as err:
        print("error in signup", err)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    

@userRouter.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        return service.login_user(form_data.username, form_data.password)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    

    
@userRouter.get('/me', summary='Get details of currently logged in user')
async def get_me(user: SystemUser = Depends(authentication_service.get_current_user)):
    return user


@userRouter.get("/{username}")
async def get_by_username(username: str, user: User = Depends(authentication_service.get_current_user)):
    try:
        return service.get_by_username(username)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@userRouter.delete("/{username}")
async def remove(username: str, user: User = Depends(authentication_service.get_current_user)):
    try:
        return service.delete_by_username(username, user)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

