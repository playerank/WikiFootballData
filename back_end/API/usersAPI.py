from fastapi import APIRouter, responses#, Depends
#from .dependencies import get_token_header

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

online_user_list=list()

tmp_user_database=[{"username":"Dodo","password":"12"}]

@router.post("/{username}")
async def sign_up(username: str, password: str):
    """
    Register a new user
    """
    for user in tmp_user_database:
        if user["username"]==username:
            return {"message":"username already exists"}
    tmp_user_database.append({"username":username,"password":password})
    return {"message":"user created succesfully!"}

@router.get("/login")
async def login(username: str, password: str):
    """
    Log in a new User, if username doesen't exist or password is incorrect return error
    """
    if {"username":username,"password":password} in tmp_user_database:
        for user in online_user_list:
            if user["username"]==username:
                return responses.JSONResponse(content={"message":"username already online"},status_code=400)
        online_user_list.append({"username":username, "password":password})
        return {"message":"successful login! e codice che identifica il ruolo"}
    return responses.JSONResponse(content={"message":"username or password is incorrect"},status_code=400)

@router.get("/logout")
async def logout(username: str):
    """
    Log out a User, if username is not online return error
    """
    for user in online_user_list:
        if user["username"]==username:
            online_user_list.remove(user)
            return {"message":"succesful logout!"}
    return responses.JSONResponse(content={"message":"FATAL ERROR"},status_code=400)

@router.post("/{username}/role")
async def add_editor(username: str):
    """
    Change user role to editor, if username is incorrect return error
    Only administrators or editors can call this function
    """
    for user in tmp_user_database:
        if user["username"]==username:
            user.update["is_editor":True]
            return {"message":"user role updated successfully!"}
    return responses.JSONResponse(content={"message":"username is incorrect!"},status_code=400)

@router.get("")
async def get_user_list():
    """
    Get the user list from db
    Only administrators can call this function
    """
    return tmp_user_database

@router.get("/online")
async def get_online_user_list():
    """
    Get the online user list from db
    Only administrators can call this function
    """
    return online_user_list
