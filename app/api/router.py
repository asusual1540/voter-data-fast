from fastapi import APIRouter
from app.api.user.user_controller import userRouter
from app.api.voter.voter_controller import voterRouter

router = APIRouter()


router.include_router(userRouter, prefix="/user", tags=["User Data"])
router.include_router(voterRouter, prefix="/voter", tags=["Voter Data"])
