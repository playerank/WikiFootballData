from fastapi import Depends, FastAPI, responses
import usersAPI
import matchesAPI
import requested_matchesAPI
import competitionsAPI
import teamsAPI
import playerAPI
import data.mongo_setup as mongo_setup

app = FastAPI()
app.include_router(usersAPI.router)
app.include_router(matchesAPI.router)
app.include_router(requested_matchesAPI.router)
app.include_router(competitionsAPI.router)
app.include_router(teamsAPI.router)
app.include_router(playerAPI.router)

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
    mongo_setup.global_init()
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
async def get_N():
    """
    Return the value of N
    Only administrators can call this funcion
    """
    return n

@app.post("/rules/N")
async def change_N(new_value: int):
    """
    Change the value of N, it's not retroactive, if new_value is incorrect return error
    Only administrators can call this function
    """
    if new_value>len(usersAPI.tmp_user_database):
        return responses.JSONResponse(content={"message":"value is incorrect"},status_code=400)
    global n
    n=abs(new_value)
    return {"message":"N updated successfully!"}
