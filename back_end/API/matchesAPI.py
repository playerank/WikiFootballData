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

@router.get("")
async def get_match_list():
    """
    Get the match list from db
    """
    return tmp_matches_database

@router.post("/{match_name}") 
async def add_match(username: str,match_name: str, link: str):#HttpUrl):
    """
    Add a new match to db
    """
    for match in tmp_matches_database:
        if match["name"]==match_name:
            return responses.JSONResponse(content={"message":"match already within the list"},status_code=400)
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
async def change_match_link(match_name: str, link: str):#HttpUrl):
    """
    Change the link of the match, if the match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"link":link})
            return {"message":"Match updated successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def change_match_report(match_name: str, report: str):
    """
    Change the report of the match, if match_name is incorrect return error
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name and elem["report"]!="":
            elem.update({"report":report})
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

@router.post("/{match_name}/report")
async def add_match_report(match_name: str,match_report: str):#Json):
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
async def add_data(username: str,match_name: str,time_slot_id: str,result: str):#Json):
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
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"is_confirmed":True})
            return {"message":"match_name confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{new_match_name}")
async def modify_name(match_name: str,new_match_name: str):
    """
    Modify and confirm definitely the match name in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"name":new_match_name})
            elem.update({"is_confirmed":True})
            return {"message":"match_name updated and confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def assess_link(match_name: str):
    """
    Confirm definitely the match link in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"link_is_confirmed":True})
            return {"message":"link confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def modify_link(match_name: str,link: str):
    """
    Modify and confirm definitely the match link in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"link":link})
            elem.update({"link_is_confirmed":True})
            return {"message":"link updated and confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def assess_match_report(match_name: str):
    """
    Confirm definitely the match report in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"report_is_confirmed":True})
            return {"message":"link confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)

@router.post("/{match_name}")
async def modify_match_report(match_name: str,report: str):
    """
    Modify and confirm definitely the match report in the db, if the match_name is incorrect return error
    Only administrators or editors can call this function
    """
    for elem in tmp_matches_database:
        if elem["name"]==match_name:
            elem.update({"report":report})
            elem.update({"report_is_confirmed":True})
            return {"message":"report updated and confirmed successfully!"}
    return responses.JSONResponse(content={"message":"match_name is incorrect"},status_code=400)
