from datetime import timedelta, datetime
import os
import hashlib

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema

from config import get_envs
env = get_envs() # envs have settings for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/user/login')

router = APIRouter(
    prefix="/api/user",
)

def get_current_user(token: str = Depends(oauth2_scheme),
                    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.JWT_PRIVATE_KEY, algorithms=[env.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    else:
        user = user_crud.get_user_by_name(db, username=username)
        if user is None:
            raise credentials_exception
        return user

@router.get('/check_ip', status_code=status.HTTP_204_NO_CONTENT)
def check_ip(request: Request,
            db:Session = Depends(get_db)):
    user = user_crud.get_user_by_ip(db, ip_addr=request.client.host)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Only one account per IP address is allowed [ {user.username} ]")

@router.get('/check_login', status_code=status.HTTP_204_NO_CONTENT)
def check_login(request: Request,
                user:user_schema.User = Depends(get_current_user)):
    # if get_current_user succeeds(logged in and access token valid):
    #   HTTP 204
    # else (if access token invalid):
    #   get_current_user raises HTTP_401_UNAUTHORIZED
    pass

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def user_create(request: Request,
                _user_create: user_schema.UserCreate, 
                db: Session = Depends(get_db)):
    user = user_crud.get_user_by_ip(db, ip_addr=request.client.host)
    if user:
        # allow one account per ip
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User [{user.username}, {user.registered_ip}] already exists!!")
    user = user_crud.get_user_by_name(db, username=_user_create.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User [{user.username}] already exists!!")
    user_crud.create_user(db=db, 
                    user_create=_user_create, 
                    ip_addr=request.client.host)

@router.post("/login", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
            db: Session = Depends(get_db)):
    user = user_crud.get_user_by_name(db, form_data.username)
    if not user or \
        (user.password !=  user_crud.hash_password(form_data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRATION_MIN)
    }
    access_token = jwt.encode(data, env.JWT_PRIVATE_KEY, algorithm=env.ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "user_idx": user.id
    }

@router.get('/userinfo/{user_id}', response_model=user_schema.User)
def userinfo(user_id: int,
                request: Request,
                db: Session = Depends(get_db)):
    # only serve "public" user informations
    user = user_crud.get_user_by_id(db, userid=user_id)
    if user:
        return {
            'id': user.id,
            'username': user.username,
            'participated': user.participated,
            'ranking': user.ranking,
            'register_date': user.register_date,
        }
    else:
        return {
            'id': user_id,
            'username': 'N/A',
            'participated': 0,
            'ranking': 0,
            'register_date': datetime.fromtimestamp(0)
        }