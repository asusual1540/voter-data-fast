import uuid
from fastapi import HTTPException, status

from app.api.user.user_model import User



class UserService:
    def __init__(self, config, db, authentication_service):
        self.config = config
        self.db = db
        self.authentication_service = authentication_service



    def get_by_username(self, username: str):
        with self.db() as session:
            print("searching user", username)
            found_user = session.query(User).filter(User.username == username).first()
            print("founduser", found_user)
            if found_user is None:
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not exist"
                )
            
            return found_user


    def delete_by_username(self, username: str, user: User):
        with self.db() as session:
            print("searching user", username)
            found_user = session.query(User).filter(User.username == username).first()
            print("founduser", found_user)
            if found_user is None:
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not exist"
                )
            if user.username != found_user.username:
                session.delete(found_user)
                session.commit()
                return {"message": "User deleted successfully"}
            else:
                return {"message": "You can not delete yourself"}

    def signup_user(self, username: str, password: str):
        with self.db() as session:
            print("searching user", username)
            existing_user = session.query(User).filter(User.username == username).first()
            print("existing_user", existing_user)
            if existing_user is not None:
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exist"
                )
            user = {
                'username': username,
                'password': self.authentication_service.get_hashed_password(password),
                'id': str(uuid.uuid4())
            }
            print("user", user)
            newUser = User(**user)

            print("newUser", newUser)
            session.add(newUser)
            session.commit()
            return self.login_user(username, password)
    

    def login_user(self, username: str, password: str):
        with self.db() as session:
            print("searching user", username, password)
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect username or password"
                )
            print("existing_user -> ", existing_user)
            hashed_pass = existing_user.password
            if not self.authentication_service.verify_password(password, hashed_pass):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect username or password"
                )
            
            return {
                "access_token": self.authentication_service.create_access_token(existing_user.username),
                "refresh_token": self.authentication_service.create_refresh_token(existing_user.username),
            }
    
        
    

        
        