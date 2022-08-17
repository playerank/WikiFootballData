from fastapi import APIRouter, responses, Depends
from usersAPI import oauth2_scheme
from datetime import datetime
import services.player_service as svc
from services.user_service import verify_role

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
async def add_player(player_name: str, date_of_birth_str: str, nationality: str, current_team: str, club_shirt_number: int, national_team_shirt_number: int):
    """
    Add player to the collection, if player already exists return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    
    result=svc.add_player(player_name, date_of_birth, nationality, current_team, club_shirt_number, national_team_shirt_number)
    if result==1:
        return responses.JSONResponse(content={"message":f"club_shirt_number {club_shirt_number} is invalid"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"current_team {current_team} is incorrect or has not yet been saved in db"}, status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":f"nationality {nationality} is incorrect or has not yet been saved in db"}, status_code=400)
    if result==4:
        return responses.JSONResponse(content={"message":f"player {player_name} already exists"}, status_code=400)
    return {"message":"player added succesfully!"}

@router.post("/change")
async def change_player(player_name: str, date_of_birth_str: str, new_player_name: str, new_date_of_birth_str: str, new_nationality: str):
    """
    Change the player values, if player inexistent or already confirmed definetely return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    try:
        new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {new_date_of_birth_str} is in a wrong format"},status_code=400)

    result=svc.change_player(True, player_name, date_of_birth, new_player_name, new_date_of_birth, new_nationality)
    if result==1:
        return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"player already confirmed"}, status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":f"nationality {new_nationality} is incorrect or has not yet been saved in db"}, status_code=400)
    return {"message":"player changed successfully!"}

@router.post("/assess")
async def assess_player(username: str, player_name: str, date_of_birth_str: str):
    """
    Confirm definetely the player parameter, if player inexistent or already confirmed definetely return error
    Only administrators or editors can call this function
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)

    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_player(player_name, date_of_birth)
    if result==1:
       return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400) 
    if result==2:
        return responses.JSONResponse(content={"message":"player already confirmed"}, status_code=403)
    return {"message":"player confirmed successfully!"}

@router.post("/modify")
async def modify_player(username: str, player_name: str, date_of_birth_str: str, new_player_name: str, new_date_of_birth_str: str, new_nationality: str):
    """
    Modify and confirm definetely the player values, if player inexistent return error.
    Only administrators or editors can call this function
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    try:
        new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {new_date_of_birth_str} is in a wrong format"},status_code=400)

    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.change_player(False, player_name, date_of_birth, new_player_name, new_date_of_birth, new_nationality)
    if result==1:
        return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":f"nationality {new_nationality} is incorrect or has not yet been saved in db"}, status_code=400)
    return {"message":"player modified and confirmed successfully!"}

@router.post("/update")
async def update_player_conditions(player_name: str, date_of_birth_str: str, new_team: str, new_club_shirt_number: int, new_national_team_shirt_number: int):
    """
    Update the current player conditions that are the team, the club shirt number and the national team shirt number.
    if the player doesn't exist or the club shirt number is an invalid value return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)

    result=svc.update_player_conditions(player_name, date_of_birth, new_team, new_club_shirt_number, new_national_team_shirt_number)
    if result==1:
        return responses.JSONResponse(content={"message":f"Invalid shirt number {new_club_shirt_number}"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"player parameters are incorrect"}, status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":f"current_team {new_team} is incorrect or has not yet been saved in db"}, status_code=400)
    return {"message":"player conditions updated succesfully!"}