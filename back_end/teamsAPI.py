from fastapi import APIRouter, Depends, responses
from usersAPI import oauth2_scheme
import services.team_service as svc
from services.user_service import verify_role

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("")
async def get_team_list(n: int):
    """
    Return n teams from db, if n==0 then return all teams
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    teams=svc.get_teams(n)
    return teams

@router.post("/add")
async def add_team(team_name: str):
    """
    Add team to the collection, if team already exists return error
    """
    if not svc.add_team(team_name):
        return responses.JSONResponse(content={"message":f"Team {team_name} already exists"}, status_code=400)
    return {"message":"team added succesfully!"}

@router.post("/change")
async def change_team(team_name: str, new_team_name: str):
    """
    Change the team name, if team inexistent or already confirmed definetely return error
    """
    result=svc.change_team_name(True, team_name, new_team_name)
    if result==1:
        return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"team already confirmed"}, status_code=403)
    return {"message":"team name updated successfully!"}

@router.post("/assess")
async def assess_team(username: str, team_name: str):
    """
    Confirm definetely the team name, if team inexistent or already confirmed definetely return error
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_team(team_name)
    if result==1:
       return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400) 
    if result==2:
        return responses.JSONResponse(content={"message":"team already confirmed"}, status_code=403)
    return {"message":"team confirmed successfully!"}

@router.post("/modify")
async def modify_team(username: str, team_name: str, new_team_name: str):
    """
    Modify and confirm definetely the team name, if team inexistent return error
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if svc.change_team_name(False, team_name, new_team_name)==1:
        return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400)
    return {"message":"team updated and confirmed successfully!"}