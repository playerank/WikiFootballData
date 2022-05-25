# from typing import Set
from fastapi import FastAPI, responses
#from .dependencies import get_query_token
import usersAPI
import matchesAPI
# from lib.user import User

app = FastAPI()#dependencies=[Depends(get_query_token)])
app.include_router(usersAPI.router)
app.include_router(matchesAPI.router)

n=5

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

@app.post("/rules/N")
async def change_N(new_value: int):
    """
    Change the value of N, it's not retroactive, if new_value is incorrect return error
    """
    if new_value>len(usersAPI.tmp_user_database):
        return responses.JSONResponse(content={"message":"value is incorrect"},status_code=400)
    global n
    n=abs(new_value)
    return {"message":"N updated successfully!"}

@app.get("/rules")
async def get_N():
    """
    Return the value of N, only administrators can call this funcion
    """
    return n
