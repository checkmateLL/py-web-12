from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel
from src.repository import users as repository_users
from src.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=["auth"])

auth_service = AuthService()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: UserModel, db: Session = Depends(get_db)):
    existing_user = repository_users.get_user_by_email(body.email, db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    hashed_password = auth_service.get_password_hash(body.password)
    body.password = hashed_password
    new_user = repository_users.create_user(body, db)
    return new_user

@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository_users.get_user_by_email(body.username, db)
    if user is None or not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token({"sub": user.email})
    refresh_token = auth_service.create_refresh_token({"sub": user.email})
    repository_users.update_token(user, refresh_token, db)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
