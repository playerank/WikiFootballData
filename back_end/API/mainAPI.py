from fastapi import Depends, FastAPI, responses
import usersAPI
import matchesAPI
import requested_matchesAPI
import competitionsAPI
import teamsAPI
import playerAPI
import data.mongo_setup as mongo_setup
from data.rules import n
import services.data_service as svc

app = FastAPI()
app.include_router(usersAPI.router)
app.include_router(matchesAPI.router)
app.include_router(requested_matchesAPI.router)
app.include_router(competitionsAPI.router)
app.include_router(teamsAPI.router)
app.include_router(playerAPI.router)

mongo_setup.global_init()

@app.get("/")
async def root():
    body=(
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Wiki Football Data API</h1>"
        "</body>"
        "</html>"
    )
    return responses.HTMLResponse(content=body)

@app.get("/help")
async def get_help():
    """
    Print helpful information
    """
    body=(
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Tutorial and Guidelines</h1>"
        "</body>"
        "</html>"
    )
    return responses.HTMLResponse(content=body)

@app.get("/rules")
async def get_N(username: str):
    """
    Return the value of N
    Only administrators can call this funcion
    """
    if svc.verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    return n

@app.post("/change-N")
async def change_N(username: str, new_value: int):
    """
    Change the value of N, it's not retroactive, if new_value is incorrect return error
    Only administrators can call this function
    """
    if svc.verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if new_value>usersAPI.get_user_n():
        return responses.JSONResponse(content={"message":"value is incorrect"},status_code=400)
    global n
    n=abs(new_value)
    return {"message":"N updated successfully!"}
