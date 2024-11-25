from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import TokenModel, UserModel, UserResponse
from src.utils import Hash, create_access_token
from src.repository.users import get_user_by_email, create_user

SECRET_KEY = "b3cf40e3b9b8e237f5f7db6f78b72fbbaff0ad2377a9de7c0136e4a3d36e4916"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter(tags=["auth"])

hash_handler = Hash()

import logging
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserModel, db: Session = Depends(get_db)):
    try:
        logger.info("Attempting to create user with email: %s", body.email)
        exist_user = get_user_by_email(email=body.email, db=db)
        if exist_user:
            logger.error("User with email %s already exists", body.email)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
        body.password = hash_handler.get_password_hash(body.password)
        logger.info("Password hashed successfully")
        new_user = create_user(body, db)
        logger.info("User created successfully")
        return UserResponse(user=new_user, detail="User successfully created")
    except Exception as e:
        logger.error("Error occurred while creating user: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/login", response_model=TokenModel)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(form_data.username, db=db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not hash_handler.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    # Generate JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/refresh_token", response_model=TokenModel)
def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise credentials_exception

    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}