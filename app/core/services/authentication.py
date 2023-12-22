from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from jose import jwt
from pydantic import ValidationError
from app.api.user.user_model import TokenPayload, SystemUser, User


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)




class AuthenticationService:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.password_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)


    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)

        
    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.config.JWT_SECRET_KEY, self.config.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=self.config.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.config.JWT_REFRESH_SECRET_KEY, self.config.ALGORITHM)
        return encoded_jwt
    

        
    async def get_current_user(self, token: str = Depends(reuseable_oauth)) -> User:
        try:
            payload = jwt.decode(
                token, self.config.JWT_SECRET_KEY, algorithms=[self.config.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        with self.db() as session:
            user = session.query(User).filter(User.username == token_data.sub).first()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Could not find user",
                )
        
            return user
    
    