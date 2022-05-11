#WORK IN PROGRESS
import json
import fastapi
from pydantic import HttpUrl, Json

app=fastapi.FastAPI()

n=5

tmp_user_database=[{"username":"Dodo","password":"12"}]
#manca lista degli utenti online da verificare al login e al logout

tmp_completed_matches_database=[{"name":"Francia-Argentina","score":"4-3","data":{"5'":{"analysis":"JsonDocument","endorse":10,"dislike":0},"10'":""}}]

tmp_matches_database=[{"name":"Francia-Croazia","link":"","score":"4-2","username":"Dodo","report":"JsonReport","journal":"","data":{"5'":{"analysis":"JsonDocument","endorse":1,"dislike":2,"working":"","author":"Dodo"},"10'":""},"workers":[]}]

requested_match_set=set("Italia-Inghilterra")

@app.get("/")
async def root():
    body=(
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Wiki Football Data API</h1>"
        "</body>"
        "</html>"
    )
    return fastapi.responses.HTMLResponse(content=body)

@app.post("/users/{username},{password}")
async def sign_up(username: str, password: str):
    if {"username":username,"password":password} in tmp_user_database:
        return {"message":"username already exists"}
    tmp_user_database.append({"username":username,"password":password})
    return {"message":"user created succesfully!"}

@app.get("/users/{username},{password}")
async def login(username: str, password: str):
    if {"username":username,"password":password} in tmp_user_database:
        return {"message":"successful login!"}
    return fastapi.responses.JSONResponse(content={"message":"username or password is incorrect"},status_code=400)

@app.get("/users/{username}")
async def logout(username: str):
    #controllo su online_users
    return {"message":"succesful logout!"}

@app.get("/completed_matches")
async def get_completed_mach_list():
    return tmp_completed_matches_database

@app.get("/completed_matches/{match_name}/data")
async def get_completed_data(match_name :str):
    """
    Get completed match data from db
    """
    for elem in tmp_completed_matches_database:
        if elem["name"]==match_name:
            return elem
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/requested_matches/{match_name}")
async def add_match_guest(match_name: str):
    requested_match_set.add(match_name)
    return {"message":"match added succesfully!"}

@app.get("/help")
async def get_help():
    body=(
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Tutorial and Guidelines</h1>"
        "</body>"
        "</html>"
    )
    return fastapi.responses.HTMLResponse(content=body)

@app.get("/matches")
async def get_match_list():
    return tmp_matches_database

@app.post("/matches/{match_name}/info/{username},{link}") #non funziona
async def add_match(username: str,match_name: str, link: HttpUrl):
    tmp_matches_database.append({"name":match_name,"link":link,"username":username})
    return {"message":"match added successfully!"}

@app.get("/matches/{match_name}/data")
async def get_data(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/info/{new_match_name}")
async def change_match_name(match_name: str, new_match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"name":new_match_name})
            return {"message":"Match updated successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/info/{link}")
async def change_match_link(match_name: str, link: HttpUrl):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"link":link})
            return {"message":"Match updated successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/{data_name}/{judgement}")
async def validate_data(match_name: str,data_name: str,judgement: bool):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            if judgement:
                elem["data"][data_name]["endorse"]+=1
            else:
                elem["data"][data_name]["dislike"]+=1
            return {"message":"Match updated successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.get("/matches/{match_name}/info")
async def get_match_report(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["report"]
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/info/{report}")
async def add_match_report(match_name: str,match_report: Json):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"report":match_report})
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.get("/matches/{match_name}/info")
async def get_workers(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["name"]["workers"]
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.get("/matches/{match_name}/data")
async def get_free_time_slot(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            time_slot=list()
            for min in elem["name"]["data"]:
                if min["working"]=="" and min["analysis"]=="":
                    time_slot.append(min)
            return time_slot
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/data/{username},{time_slot_id}")
async def analyze_time_slot(username: str,match_name: str,time_slot_id: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem["data"][time_slot_id]["working"]=username
            return {"message":"working set successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.post("/matches/{match_name}/data/{username},{time_slot_id},{result}")
async def add_data(username: str,match_name: str,time_slot_id: str,result: Json):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem["data"][time_slot_id]["working"]=""
            elem["data"][time_slot_id]["author"]=username
            elem["data"][time_slot_id]["analysis"]=result
            return {"message":"match data updated successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.get("/matches/{match_id}/data")
async def read_journal(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["journal"]
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@app.get("/users")
async def get_user_list():
    return tmp_user_database

@app.post("/rules/{new_value}")
async def change_N(new_value: int):
    if new_value>len(tmp_user_database): 
        return fastapi.responses.JSONResponse(content={"message":"value is incorrect"},status_code=400)
    global n
    n=abs(new_value)
    return {"message":"N updated successfully!"}

@app.post("/matches/{match_name}/info")
async def assess_name(match_name: str):
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return {"message":"match_name confirmed successfully!"}
    return fastapi.responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
