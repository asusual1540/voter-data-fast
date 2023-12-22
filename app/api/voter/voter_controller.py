from fastapi import APIRouter, Depends, Response, status, HTTPException, Header, Form, UploadFile, File
from typing import List
import time
from pydantic import BaseModel
from app.api.user.user_model import User
from app.api.voter.voter_model import Area, AreaCreate, Voter, VoterCreate
from app.core.vdm import vdm
from starlette.responses import JSONResponse


voterRouter = APIRouter()
service = vdm.voter_service
authentication_service = vdm.authentication_service

@voterRouter.get("/{voter_id}")
async def get_by_id(voter_id: int):
    try:
        return service.get_by_id(voter_id)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@voterRouter.post("/create-voter")
async def create_voter(voter: VoterCreate, user: User = Depends(authentication_service.get_current_user)):
    try:
        return service.add_voter(voter)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    

    
@voterRouter.post("/create-area")
async def create_area(area: AreaCreate, user: User = Depends(authentication_service.get_current_user)):
    try:
        return service.add_area(area)
    except HTTPException:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    



    



    
    

