from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, responses 
from pydantic import HttpUrl, Json
import services.data_service as svc

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)

# fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

# tmp_matches_database=[{"name":"Francia-Croazia","link":"","score":"4-2","username":"Dodo","report":"JsonReport","journal":"","data":{"5'":{"analysis":"JsonDocument","endorse":1,"dislike":2,"working":"","author":"Dodo"},"10'":""},"workers":[]}]

# tmp_completed_matches_database=[{"name":"Francia-Argentina","score":"4-3","data":{"5'":{"analysis":"JsonDocument","endorse":10,"dislike":0},"10'":""}}]

@router.get("/completed_matches")
async def get_completed_match_list():
    """
    Get completed match list from db
    """
    c_matches=svc.get_completed_matches()
    return c_matches

@router.get("/completed_matches/data")
async def get_completed_data(match_id):#id o nomi?
    """
    Get completed match data from db, if the match_id is incorrect return error
    """
    # for elem in tmp_completed_matches_database:
    #     if elem["name"]==match_name:
    #         return elem
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    id: ObjectId=svc.get_match_id(home_team,away_team,season,competition_name)
    if not id:
        return responses.JSONResponse(content={"message":"match not found!"},status_code=400)
    return {"message":f"id of the match={id}"}

@router.post("/add") 
async def add_match(username: str, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Add a new match to db
    """
    # for match in tmp_matches_database:
    #     if match["name"]==match_name:
    #         return responses.JSONResponse(content={"message":"match already within the list"},status_code=400)
    # tmp_matches_database.append({"name":match_name,"link":link,"username":username})
    # return {"message":"match added successfully!"}
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         return elem
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    data=svc.get_data(match_id)
    if not data:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return data

@router.post("/change-name")
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"link":link})
    #         return {"message":"Match updated successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name and elem["report"]!="":
    #         elem.update({"report":report})
    #         return {"message":"Match updated successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    result=svc.change_match_report(match_id,report)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match report already confirmed"},status_code=403)
    return {"message":"Match report updated successfully!"}

@router.post("/validate")
async def validate_data(match_id, data_index: int, judgement: bool):
    """
    Add a new judgement to the match, if the match_id is incorrect or match data is already confirmed return error
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         if judgement:
    #             elem["data"][data_name]["endorse"]+=1
    #         else:
    #             elem["data"][data_name]["dislike"]+=1
    #         return {"message":"Match updated successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    if data_index<0 or data_index>25:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.validate_data(match_id,data_index,judgement)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"data already confirmed"},status_code=403)
    return {"message":"Data judgement updated successfully!"}

@router.get("/get-report")
async def get_match_report(match_id):
    """
    Get the match report from db, if the match_id is incorrect return error
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         return elem["report"]
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    report=svc.get_match_report(match_id)
    if not report:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return report

@router.post("/add-report")
async def add_match_report(match_id, match_report: str):#Json):
    """
    Add the report to the match, if the match_id is incorrect return error
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"report":match_report})
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         return elem["name"]["workers"]
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    worker_list=svc.get_workers(match_id)
    if not worker_list:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return worker_list

@router.get("/get-free-slot")
async def get_free_time_slot(match_id):
    """
    Get the list of the free time slot of the match from db, if the match_id is incorrect or the match is completed return error
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         time_slot=list()
    #         for min in elem["name"]["data"]:
    #             if min["working"]=="" and min["analysis"]=="":
    #                 time_slot.append(min)
    #         return time_slot
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem["data"][time_slot_id]["working"]=username
    #         return {"message":"working set successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem["data"][time_slot_id]["working"]=""
    #         elem["data"][time_slot_id]["author"]=username
    #         elem["data"][time_slot_id]["analysis"]=result
    #         return {"message":"match data updated successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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

@router.get("/journal")
async def read_journal(match_id):
    """
    Return the journal of the match, if the match_id is incorrect return error
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         return elem["journal"]
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"is_confirmed":True})
    #         return {"message":"match_name confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
    result=svc.assess_name(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match_name already confirmed"},status_code=400)
    return {"message":"match_name confirmed successfully!"}

@router.post("/modify-name")
async def modify_name(match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Modify and confirm definitely the match name in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"name":new_match_name})
    #         elem.update({"is_confirmed":True})
    #         return {"message":"match_name updated and confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"link_is_confirmed":True})
    #         return {"message":"link confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"link":link})
    #         elem.update({"link_is_confirmed":True})
    #         return {"message":"link updated and confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
    if not svc.modify_link(username, match_id, link):
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"link updated and confirmed successfully!"}

@router.post("/assess-report")
async def assess_match_report(username: str, match_id):
    """
    Confirm definitely the match report in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"report_is_confirmed":True})
    #         return {"message":"Report confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
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
    # for elem in tmp_matches_database:
    #     if elem["name"]==match_name:
    #         elem.update({"report":report})
    #         elem.update({"report_is_confirmed":True})
    #         return {"message":"report updated and confirmed successfully!"}
    # return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
    #controllo dell'user
    if not svc.modify_report(username, match_id, report):
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"report updated and confirmed successfully!"}