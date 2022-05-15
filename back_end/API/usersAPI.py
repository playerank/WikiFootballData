from fastapi import APIRouter, responses, Depends
#from .dependencies import get_token_header
from mainAPI import tmp_user_database

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

n=5

online_user_set=set()

#tmp_user_database=[{"username":"Dodo","password":"12"}]

@router.post("/{username}")
async def sign_up(username: str, password: str):
    """
    Register a new user
    """
    if {"username":username,"password":password} in tmp_user_database:
        return {"message":"username already exists"}
    tmp_user_database.append({"username":username,"password":password})
    return {"message":"user created succesfully!"}

@router.get("/login")
async def login(username: str, password: str):
    """
    Log in a new User, if username doesen't exist or password is incorrect return error
    """
    if {"username":username,"password":password} in tmp_user_database:
        return {"message":"successful login! e codice che identifica il ruolo"}
    return responses.JSONResponse(content={"message":"username or password is incorrect"},status_code=400)

@router.get("/logout")
async def logout(username: str):
    """
    Log out a User, if username is not online return error
    """
    if username in online_user_set:
        return {"message":"succesful logout!"}
    return responses.JSONResponse(content={"message":"FATAL ERROR"},status_code=400)

@router.get("/users")
async def get_user_list():
    """
    Get the user list from db, only administrators can call this function
    """
    return tmp_user_database
