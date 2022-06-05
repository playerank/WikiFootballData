from fastapi import APIRouter, responses#, Depends
#from .dependencies import get_token_header

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

team_db=[{"name":"F.C. Internazionale","is_confirmed":True}]

@router.get("")
async def get_team_list():
    """
    Return the team list from db
    """
    return team_db

@router.post("/{team_name}")
async def add_team(team_name: str):
    """
    Add team to the collection, if team already exists return error
    """
    for t in team_db:
        if t["name"]==team_name:
            return responses.JSONResponse(content={"message":"team already exists"}, status_code=400)
    team_db.append({"name":team_name,"is_confirmed":False})
    return {"message":"team added succesfully!"}

@router.post("/{new_team_name}")
async def change_team(team_name:str, new_team_name:str):
    """
    Change the team name, if team inexistent or already confirmed definetely return error
    """
    for t in team_db:
        if t["name"]==team_name and t["is_confirmed"]==False:
            t.update({"name":new_team_name})
            return {"message":"team name updated successfully!"}
    return responses.JSONResponse(content={"message":"team already confirmed"}, status_code=400)

@router.post("/{team_name}")
async def assess_team(team_name: str):
    """
    Confirm definetely the team name
    Only administrators or editors can call this function
    """
    for t in team_db:
        if t["name"]==team_name:
            t.update({"is_confirmed":True})
            return {"message":"team confirmed successfully!"}
    return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400)

@router.post("/{new_team_name}")
async def modify_team(team_name: str, new_team_name: str):
    """
    Modify and confirm definetely the team name
    Only administrators or editors can call this function
    """
    for t in team_db:
        if t["name"]==team_name:
            t.update({"name":new_team_name})
            return {"message":"team updated and confirmed successfully!"}
    return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400)