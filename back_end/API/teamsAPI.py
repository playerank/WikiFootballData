from fastapi import APIRouter, responses
import services.data_service as svc

router = APIRouter(
    prefix="/teams",
    tags=["teams"]#,#Possibile implementazione della sicurezza
    # dependencies=[Depends(get_current_username)],
    # responses={404: {"description":"not found"}},
)

@router.get("")
async def get_team_list():
    """
    Return the team list from db
    """
    teams=svc.get_teams()
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
async def change_team(team_name:str, new_team_name:str):
    """
    Change the team name, if team inexistent or already confirmed definetely return error
    """
    result=svc.change_team_name(team_name, new_team_name)
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
    role=svc.verify_role(username)
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
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if not svc.modify_team(team_name, new_team_name):
        return responses.JSONResponse(content={"message":"team_name is incorrect"}, status_code=400)
    return {"message":"team updated and confirmed successfully!"}