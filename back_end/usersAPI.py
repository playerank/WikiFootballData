from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, responses
import services.data_service as svc

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

SECRET_KEY='Q3HSkAyAeeX7yKfdfC2xWaSsZQJKI3CILskncv0Z9ZcmO5cRGEpmeB9GRAVP53z1' #64
ALGORITHM="HS256"
##RICORDARSI DI FARE LAVORI ESTETICI (come strip(), etc)
#Molto probabilmente da fare nel main
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from jose import jwt

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: Dict[str, str], expires_delta: timedelta):
    to_encode= data.copy()
    expire=datetime.utcnow()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/sign_up")
async def sign_up(username: str, password: str):
    """
    Register a new user
    """
    existing_user=svc.find_user_by_username(username)
    if existing_user:
        return responses.JSONResponse(content={"message":f"username {username} already exists"},status_code=400)
    #hashed_password=hash_password(password)
    new_user=svc.create_user(username,password)
    return {"message":"user created succesfully!"}#id={new_user.id} debug

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm= Depends()):#username: str, password: str):
    """
    Log in a new User, if username doesen't exist or password is incorrect return error.
    FUNCTION CALLED AUTOMATICALLY BY THE SECURITY SYSTEM DO NOT CALL IT
    """
    username=form_data.username
    password=form_data.password
    result=svc.log_user(username, password)
    if result=="U":
        raise HTTPException(status_code=400, detail=f"username {username} is incorrect")
    if result=="P":
        raise HTTPException(status_code=400, detail="password is incorrect")
    if result=="L":
        raise HTTPException(status_code=400, detail="user already online")
    access_token=create_access_token({"sub":username}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type":"bearer"}


@router.get("/logout")
async def logout(username: str, token: str=Depends(oauth2_scheme)):
    """
    Log out a User, if username is not online return error
    """
    user=svc.find_user_by_username(username)
    if not user or user.is_online==False:
        return responses.JSONResponse(content={"message":"FATAL ERROR"},status_code=400)
    user.update(is_online=False)
    return {"message": "successful logout!"}

@router.post("/{username}/role")
async def add_editor(username: str, user: str, token: str=Depends(oauth2_scheme)):
    """
    Change user role to editor, if username is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if not svc.add_editor(user):
        return responses.JSONResponse(content={"message":"username is incorrect!"},status_code=400)
    return {"message": f"user {user} role updated successfully!"}

@router.get("")
async def get_user_list(username: str, token: str=Depends(oauth2_scheme)):
    """
    Get the user list from db, the return is in raw format(a list of user object)
    Only administrators can call this function
    """
    if svc.verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    users=svc.get_users()
    return users

@router.get("/online")
async def get_online_user_list(username: str, token: str=Depends(oauth2_scheme)):
    """
    Get the online user list from db, the return is in raw format(a list of user object)
    Only administrators can call this function
    """
    if svc.verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    online_user_list=svc.get_online_users()
    return online_user_list

def get_user_n():
    users=svc.get_users()
    return len(users)