from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuthRequest(BaseModel):
    username: str = None
    password: str = None
    

class UserOut(BaseModel):
    id: UUID
    username: str


class SystemUser(UserOut):
    password: str



class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)

    
    username = Column(String(500), default=None, nullable=False)
    password = Column(String(1000), default=None, nullable=False)
    
    created_on = Column(DateTime, default=datetime.utcnow, nullable=True)


    
    def as_dict(self):
        def format_date(date):
            if date:
                return date.isoformat()
            else:
                return None
        return {
                column.name: getattr(self, column.name) if column.name != "created_on"
                else format_date(getattr(self, column.name))
                for column in self.__table__.columns
            }
