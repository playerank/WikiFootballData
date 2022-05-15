from fastapi import APIRouter, responses, Depends 
from pydantic import HttpUrl, Json
#from .dependencies import get_token_header

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

tmp_matches_database=[{"name":"Francia-Croazia","link":"","score":"4-2","username":"Dodo","report":"JsonReport","journal":"","data":{"5'":{"analysis":"JsonDocument","endorse":1,"dislike":2,"working":"","author":"Dodo"},"10'":""},"workers":[]}]

tmp_completed_matches_database=[{"name":"Francia-Argentina","score":"4-3","data":{"5'":{"analysis":"JsonDocument","endorse":10,"dislike":0},"10'":""}}]

requested_match_set=set("Italia-Inghilterra")

@router.get("")
async def get_match_list():
    """
    Get the match list from db
    """
    return tmp_matches_database

@router.get("/completed_matches")
async def get_completed_match_list():
    """
    Get completed match list from db
    """
    return tmp_completed_matches_database

@router.get("/completed_matches/{match_name}")
async def get_completed_data(match_name :str):
    """
    Get completed match data from db, if the match_name is incorrect return error
    """
    for elem in tmp_completed_matches_database:
        if elem["name"]==match_name:
            return elem
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.get("/requested_matches")
async def get_requested_match_list():
    """
    Get the requested_match list
    """
    return requested_match_set

@router.post("/requested_matches/{match_name}")
async def add_match_guest(match_name: str):
    """
    Add a match to the requested match set
    """
    requested_match_set.add(match_name)
    return {"message":"match added succesfully!"}

@router.post("/{match_name}") 
async def add_match(username: str,match_name: str, link: HttpUrl):
    """
    Add a new match to db
    """
    tmp_matches_database.append({"name":match_name,"link":link,"username":username})
    return {"message":"match added successfully!"}

@router.get("/{match_name}")
async def get_data(match_name: str):
    """
    Get data of the match from db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{new_match_name}")
async def change_match_name(match_name: str, new_match_name: str):
    """
    Change the name of the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"name":new_match_name})
            return {"message":"Match updated successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def change_match_link(match_name: str, link: HttpUrl):
    """
    Change the link of the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"link":link})
            return {"message":"Match updated successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}/{data_name}")#/{judgement}
async def validate_data(match_name: str,data_name: str,judgement: bool):
    """
    Add a new judgement to the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            if judgement:
                elem["data"][data_name]["endorse"]+=1
            else:
                elem["data"][data_name]["dislike"]+=1
            return {"message":"Match updated successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.get("/{match_name}")
async def get_match_report(match_name: str):
    """
    Get the match report from db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["report"]
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}/{report}")
async def add_match_report(match_name: str,match_report: Json):
    """
    Add the report to the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"report":match_report})
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.get("/{match_name}")
async def get_workers(match_name: str):
    """
    Get the wrokers set of the match from db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["name"]["workers"]
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.get("/{match_name}")
async def get_free_time_slot(match_name: str):
    """
    Get the list of the free time slot of the match from db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            time_slot=list()
            for min in elem["name"]["data"]:
                if min["working"]=="" and min["analysis"]=="":
                    time_slot.append(min)
            return time_slot
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}/{time_slot_id}")
async def analyze_time_slot(username: str,match_name: str,time_slot_id: str):
    """
    Signal the server that a user started processing the time slot, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem["data"][time_slot_id]["working"]=username
            return {"message":"working set successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}/{time_slot_id}")
async def add_data(username: str,match_name: str,time_slot_id: str,result: Json):
    """
    Add the result of the analysis to the db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem["data"][time_slot_id]["working"]=""
            elem["data"][time_slot_id]["author"]=username
            elem["data"][time_slot_id]["analysis"]=result
            return {"message":"match data updated successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.get("/{match_name}")
async def read_journal(match_name: str):
    """
    Return the journal of the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return elem["journal"]
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def assess_name(match_name: str):
    """
    Confirm definitely the match name in the db, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            return {"message":"match_name confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
