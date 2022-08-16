from fastapi import Depends, FastAPI, responses
import usersAPI
import matchesAPI
import requested_matchesAPI
import competitionsAPI
import teamsAPI
import playersAPI
import data.mongo_setup as mongo_setup
from data.rules import n
from services.user_service import verify_role

app = FastAPI()
app.include_router(usersAPI.router)
app.include_router(matchesAPI.router)
app.include_router(requested_matchesAPI.router)
app.include_router(competitionsAPI.router)
app.include_router(teamsAPI.router)
app.include_router(playersAPI.router)

#ROBOMONGO sostituto di mongoDBcompass

#cd '.\Progetto wikiFootballData\back_end\API'
#uvicorn mainAPI:app --reload
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
async def get_N(username: str, token: str=Depends(usersAPI.oauth2_scheme)):
    """
    Return the value of N
    Only administrators can call this funcion
    """
    if verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    return n

@app.post("/change-N")
async def change_N(username: str, new_value: int, token: str=Depends(usersAPI.oauth2_scheme)):
    """
    Change the value of N, it's not retroactive, if new_value is incorrect return error
    Only administrators can call this function
    """
    if verify_role(username)!="A":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if new_value>usersAPI.get_user_n():
        return responses.JSONResponse(content={"message":"value is incorrect"},status_code=400)
    global n
    n=abs(new_value)
    return {"message":"N updated successfully!"}