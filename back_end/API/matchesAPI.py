from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, responses 
from pydantic import HttpUrl, Json
import services.data_service as svc

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)

@router.get("/completed_matches")
async def get_completed_match_list():
    """
    Get completed match list from db, even non-user can call this function
    """
    c_matches=svc.get_completed_matches()
    return c_matches

@router.get("/completed_matches/data")
async def get_completed_data(match_id):#id o nomi?
    """
    Get completed match data from db, if the match_id is incorrect return error, even non-user can call this function
    """
    c_data=svc.get_completed_data(match_id)
    if c_data==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if c_data==2:
        return responses.JSONResponse(content={"message":"match is not completed"},status_code=400)
    return c_data


@router.get("")
async def get_match_list():
    """
    Get the match list from db
    """
    matches=svc.get_matches()
    return matches

@router.get("/get_id")
async def get_match_id(home_team: str, away_team: str, season: str, competition_name: str):
    id=svc.get_match_id(home_team,away_team,season,competition_name)
    if id==1:
        return responses.JSONResponse(content={"message":f"competition {competition_name} is incorrect"},status_code=400)
    if id==2:
        return responses.JSONResponse(content={"message":f"home_team {home_team} is incorrect"},status_code=400)
    if id==3:
        return responses.JSONResponse(content={"message":f"away_team {away_team} is incorrect"},status_code=400)
    if id==4:
        return responses.JSONResponse(content={"message":"match doesn't exist"},status_code=400)
    return {"message":f"id of the match={id}"}

@router.post("/add")
async def add_match(username: str, home_team: str, away_team: str, season: str, competition_name: str, round: str, date_str: str, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Add a new match to db
    """
    date=datetime.strptime(date_str, '%d/%m/%Y')
    result=svc.add_match(username,home_team,away_team,season,competition_name,round,date,link,extended_time,penalty)
    if result==1:
        return responses.JSONResponse(content={"message":f"competition {competition_name} is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"home_team {home_team} is incorrect"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":f"away_team {away_team} is incorrect"},status_code=400)
    if result==4:
        return responses.JSONResponse(content={"message":"match already exists"},status_code=400)
    return {"message":"match added successfully!"}

@router.get("/get-data")
async def get_data(match_id):
    """
    Get data of the match from db, if the match_id is incorrect return error
    """
    data=svc.get_data(match_id)
    if not data:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return data

@router.post("/change-name") #da testare
async def change_match_name(match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Change the name of the match, if the match_id is incorrect or match is already confirmed return error
    """
    result=svc.change_name(True, match_id, home_team, away_team, season, competition_name, round, date, link, extended_time, penalty)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match already confirmed"},status_code=403)
    return {"message":"Match name updated successfully!"}

@router.post("/change-link")
async def change_match_link(match_id, new_link: HttpUrl):
    """
    Change the link of the match, if match_id is incorrect or match link is already confirmed return error
    """
    result=svc.change_match_link(match_id,new_link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match link already confirmed"},status_code=403)
    return {"message":"Match link updated successfully!"}
    

@router.post("/change-report")
async def change_match_report(match_id, report: str):
    """
    Change the report of the match, if match_id is incorrect or match report is already confirmed return error
    """
    result=svc.change_match_report(match_id,report)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match report already confirmed"},status_code=403)
    return {"message":"Match report updated successfully!"}

@router.get("/get-report")
async def get_match_report(match_id):
    """
    Get the match report from db, if the match_id is incorrect return error
    """
    report=svc.get_match_report(match_id)
    if not report:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return report

@router.post("/add-report")
async def add_match_report(match_id, match_report: str):#Json):
    """
    Add the report to the match, if the match_id is incorrect return error
    """
    result=svc.add_match_report(match_id, match_report)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match report already added"},status_code=400)
    return {"message":"Report added successfully!"}


@router.get("/get-workers")
async def get_workers(match_id): #DA RIMUOVERE?
    """
    Get the workers set of the match from db, if the match_id is incorrect return error
    """
    worker_list=svc.get_workers(match_id)
    if not worker_list:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return worker_list

@router.get("/get-free-slot")
async def get_free_time_slot(match_id):
    """
    Get the list of the free time slot of the match from db, if the match_id is incorrect or the match is completed return error
    """
    time_slots=svc.get_free_time_slot(match_id)
    if time_slots==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if time_slots==2:
        return responses.JSONResponse(content={"message":"match is already completed"},status_code=403)
    return time_slots

@router.post("/analyze-slot")
async def analyze_time_slot(username: str, match_id, data_index: int):
    """
    Signal the server that a user started processing the time slot, if the match_id is incorrect, the match is completed or the time_slot is not free return error
    """
    if data_index<0 or data_index>28:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.analyze_time_slot(username, match_id, data_index)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match is completed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"time_slot is being analyzed by another user"},status_code=400)
    return {"message":"working username set successfully!"}

@router.post("/add-data")
async def add_data(username: str, match_id, data_index: int, detail: str):#Json):
    """
    Add the result of the analysis to the db, if the match_id is incorrect return error
    """
    if data_index<0 or data_index>28:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.add_data(username,match_id,data_index,detail)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match is completed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"time_slot is being analyzed by another user"},status_code=400)
    return {"message":"match data updated successfully!"}

@router.post("/validate")
async def validate_data(match_id, data_index: int, judgement: bool):
    """
    Add a new judgement to the match, if the match_id is incorrect or match data is already confirmed return error
    """
    if data_index<0 or data_index>25:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.validate_data(match_id,data_index,judgement)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"data already confirmed"},status_code=403)
    return {"message":"Data judgement updated successfully!"}

@router.get("/journal")
async def read_journal(match_id):
    """
    Return the journal of the match, if the match_id is incorrect return error
    """
    journal=svc.read_journal(match_id)
    if not journal:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return journal


@router.post("/assess-name")
async def assess_name(username: str, match_id):
    """
    Confirm definitely the match name in the db, if the match_id is incorrect or match_name already confirmed return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_name(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match_name already confirmed"},status_code=400)
    return {"message":"match_name confirmed successfully!"}

@router.post("/modify-name")
async def modify_name(username: str, match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Modify and confirm definitely the match name in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.change_name(False, match_id, home_team, away_team, season, competition_name, round, date, link, extended_time, penalty)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"Match name updated successfully!"}

@router.post("/assess-link")
async def assess_link(username: str,match_id):
    """
    Confirm definitely the match link in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_link(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"link already confirmed"},status_code=400)
    return {"message":"link confirmed successfully!"}

@router.post("/modify-link")
async def modify_link(username: str,match_id, link: HttpUrl):
    """
    Modify and confirm definitely the match link in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if not svc.modify_link(username, match_id, link):
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"link updated and confirmed successfully!"}

@router.post("/assess-report") #check
async def assess_match_report(username: str, match_id):
    """
    Confirm definitely the match report in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_report(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Report already confirmed"},status_code=400)
    return {"message":"Report confirmed successfully!"}

@router.post("/modify-report")
async def modify_match_report(username: str, match_id, report: str):
    """
    Modify and confirm definitely the match report in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if not svc.modify_report(username, match_id, report):
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"report updated and confirmed successfully!"}