from fastapi import APIRouter, responses, Depends
from usersAPI import oauth2_scheme
import services.data_service as svc

router = APIRouter(
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("")
async def get_player_list(n: int):
    """
    Return n players from db, if n==0 then return all players
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    players=svc.get_players(n)
    return players

@router.post("/add")
async def add_player(player_name: str,nationality: str, current_team: str, club_shirt_number: int, national_team_shirt_number: int):
    """
    Add player to the collection, if player already exists return error
    """
    result=svc.add_player(player_name, nationality, current_team, club_shirt_number, national_team_shirt_number)
    if result==1:
        return responses.JSONResponse(content={"message":f"club_shirt_number {club_shirt_number} is invalid"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"player {player_name} already exists"}, status_code=400)
    return {"message":"player added succesfully!"}

@router.post("/change")
async def change_player(username: str, player_name: str, nationality: str, current_team: str, new_player_name: str, new_nationality: str, new_current_team: str):
    """
    Change the player values, if player inexistent or already confirmed definetely return error
    """
    check=False
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        check=True
    result=svc.change_player(player_name, nationality, current_team, new_player_name, new_nationality, new_current_team, check)
    if result==1:
        return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"player already confirmed"}, status_code=403)
    return {"message":"player changed successfully!"}

@router.post("/assess")
async def assess_player(username: str, player_name: str, nationality: str, current_team: str):
    """
    Confirm definetely the player parameter, if player inexistent or already confirmed definetely return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_player(player_name, nationality, current_team)
    if result==1:
       return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400) 
    if result==2:
        return responses.JSONResponse(content={"message":"player already confirmed"}, status_code=403)
    return {"message":"player confirmed successfully!"}

@router.post("/update")
async def update_player_conditions(player_name: str, nationality: str, current_team: str, new_team: str, new_club_shirt_number: int, new_national_team_shirt_number: int):
    """
    Update the current player conditions that are the team, the club shirt number and the national team shirt number.
    if the player doesn't exist or the club shirt number is an invalid value return error
    """
    result=svc.update_player_conditions(player_name, nationality, current_team, new_team, new_club_shirt_number, new_national_team_shirt_number)
    if result==1:
        return responses.JSONResponse(content={"message":f"Invalid shirt number {new_club_shirt_number}"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400)
    return {"message":"player conditions updated succesfully!"}