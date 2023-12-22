"""Docugen module."""
from app.api.user.user_service import UserService
from app.api.voter.voter_service import VoterService
from app.core.services.authentication import AuthenticationService

from app.core.config import Config
from app.core.database import Database


class Vdm:
    
    config = Config()
    db = Database(config.DB_URL)
    authentication_service = AuthenticationService(config, db.session)
    voter_service = VoterService(config, db.session, authentication_service)
    user_service = UserService(config, db.session, authentication_service)

        
vdm = Vdm()





