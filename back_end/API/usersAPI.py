from fastapi import APIRouter, responses
import services.data_service as svc

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

##RICORDARSI DI FARE LAVORI ESTETICI (come strip(), etc)
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
    result=svc.log_user(username, password)
    #decidere se usare switch
    if result=="U":
        return responses.JSONResponse(content={"message":f"username {username} is incorrect"},status_code=400)
    if result=="P":
        return responses.JSONResponse(content={"message":"password is incorrect"},status_code=400)
    if result=="L":
        return responses.JSONResponse(content={"message":"user already online"},status_code=400)
    return {"message": f"successful login!{result}"}


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
async def add_editor(username: str, user: str):
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
async def get_user_list(username: str):
    """
    Get the user list from db, the return is in raw format(a list of user object)
    Only administrators can call this function
    """
    if svc.verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    users=svc.get_users()
    return users

@router.get("/online")
async def get_online_user_list(username: str):
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