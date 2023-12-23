from fastapi import APIRouter, Depends, Query, Response, status, HTTPException, Header, Form, UploadFile, File
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

@voterRouter.get("/")
async def voters(
    per_page: int = Query(10, description="Items per page", ge=1), 
    page: int = Query(1, description="Page number", ge=1),
    name: str = Query("", description="name"),
    voter_no: str = Query("", description="voter_no"),
    father_name: str = Query("", description="father_name"),
    mother_name: str = Query("", description="mother_name"),
    occupation: str = Query("", description="occupation"),
    address: str = Query("", description="address"),
    area_id: str = Query("", description="area_id"),
):
    return service.get_voter(per_page, page, name, voter_no, father_name, mother_name, occupation, address, area_id)


@voterRouter.get("/area")
async def areas(
    per_page: int = Query(10, description="Items per page", ge=1), 
    page: int = Query(1, description="Page number", ge=1),
    gender: str = Query("", description="gender"),
    district: str = Query("", description="district"),
    sub_district: str = Query("", description="sub_district"),
    city_corporation: str = Query("", description="city_corporation"),
    union: str = Query("", description="union"),
    ward_no: str = Query("", description="ward_no"),
    voter_area: str = Query("", description="voter_area"),
    total_voter: str = Query("", description="total_voter"),
    voter_area_no: str = Query("", description="voter_area_no"),
    total_voter_female: str = Query("", description="total_voter_female"),
):
    return service.get_voter_area(per_page, page, gender, district, sub_district, city_corporation, union, ward_no, voter_area, total_voter, voter_area_no, total_voter_female)


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
    



    



    
    

