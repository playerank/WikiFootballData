from fastapi import APIRouter, responses
import services.data_service as svc

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

online_user_list=list()

tmp_user_database=[{"username":"Dodo","password":"12"}]
##RICORDARSI DI FARE LAVORI ESTETICI (come strip(), etc) IN FRONT END
@router.post("/{username}")
async def sign_up(username: str, password: str):
    """
    Register a new user
    """
    existing_user=svc.find_user_by_username(username)
    if existing_user:
        return responses.JSONResponse(content={"message":f"username {username} already exists"},status_code=400)
    new_user=svc.create_user(username,password)
    return {"message":"user created succesfully!"}#id={new_user.id} debug

@router.get("/login")
async def login(username: str, password: str):
    """
    Log in a new User, if username doesen't exist or password is incorrect return error
    """
    response=svc.log_user(username, password)
    #decidere se usare switch
    if response=="U":
        return responses.JSONResponse(content={"message":f"username {username} is incorrect"},status_code=400)
    if response=="P":
        return responses.JSONResponse(content={"message":"password is incorrect"},status_code=400)
    if response=="L":
        return responses.JSONResponse(content={"message":"user already online"},status_code=400)
    return {"message": f"successful login!{response}"}


@router.get("/logout")
async def logout(username: str):
    """
    Log out a User, if username is not online return error
    """
    user=svc.find_user_by_username(username)
    if not user or user.is_online==False:
        return responses.JSONResponse(content={"message":"FATAL ERROR"},status_code=400)
    user.update(is_online=False)
    return {"message": "successful logout!"}

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