from datetime import datetime
import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, responses
from pydantic import HttpUrl
from usersAPI import oauth2_scheme
import services.match_service as svc
from services.user_service import verify_role

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)

@router.get("/completed-matches")
async def get_completed_match_list(n: int):
    """
    Get n completed matches from db, if n==0 then return all completed matches.
    If n<0 return error.
    Even non-user can call this function
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    c_matches=svc.get_completed_matches(n)
    return c_matches

@router.get("/completed-matches/data")
async def get_completed_match_data(match_id):
    """
    Get completed match data from db.
    If match_id is incorrect or match is not completed return error.
    Even non-user can call this function
    """
    c_data=svc.get_completed_match_data(match_id)
    if c_data==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if c_data==2:
        return responses.JSONResponse(content={"message":"match is not completed"},status_code=400)
    return c_data


@router.get("")
async def get_match_list(n: int, token: str=Depends(oauth2_scheme)):
    """
    Get n matches from db, if n==0 then return all matches.
    If n<0 return error
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    matches=svc.get_matches(n)
    return matches

@router.get("/not-completed")
async def get_not_completed_match_list(n: int, token: str=Depends(oauth2_scheme)):
    """
    Get n not completed matches from db, if n==0 then return all not completed matches.
    If n<0 return error
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    nc_matches=svc.get_not_completed_matches(n)
    return nc_matches

@router.get("/get-id")
async def get_match_id(home_team: str, away_team: str, season: str, competition_name: str, token: str=Depends(oauth2_scheme)):
    """
    Get the id of the match identified by parameters.
    If competition name is incorrect, home team is incorrect, away team is incorrect or doesn't exist a match with that values return error
    """
    id=svc.get_match_id(home_team,away_team,season,competition_name)
    if id==1:
        return responses.JSONResponse(content={"message":f"competition {competition_name} is incorrect"},status_code=400)
    if id==2:
        return responses.JSONResponse(content={"message":f"home_team {home_team} is incorrect"},status_code=400)
    if id==3:
        return responses.JSONResponse(content={"message":f"away_team {away_team} is incorrect"},status_code=400)
    if id==4:
        return responses.JSONResponse(content={"message":"match doesn't exist"},status_code=400)
    #return {"message":f"id of the match={id}"}
    return id

@router.post("/add")
async def add_match(username: str, home_team: str, away_team: str, season: str, competition_name: str, round: str, date_str: str, link: HttpUrl, extended_time: bool, penalty: bool, token: str=Depends(oauth2_scheme)):
    """
    Add a new match to db.
    If date_str is in a wrong format, competition name is incorrect, home team is incorrect, away team is incorrect or already exists a match with the same values return error
    """
    try:
        date=datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        try:
            date=datetime.strptime(date_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_str} is in a wrong format"},status_code=400)
    
    result=svc.add_match(username,home_team,away_team,season,competition_name,round,date,link,extended_time,penalty)
    if result==1:
        return responses.JSONResponse(content={"message":f"competition {competition_name} is incorrect or has not yet been saved in db"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"home_team {home_team} is incorrect or has not yet been saved in db"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":f"away_team {away_team} is incorrect or has not yet been saved in db"},status_code=400)
    if result==4:
        return responses.JSONResponse(content={"message":"match already exists"},status_code=400)
    return {"message":"match added successfully!"}

@router.post("/get-complete-info")
async def get_match_complete_info(match_id, token: str=Depends(oauth2_scheme)):
    """
    Return the complete info of the requested match in dict format.
    If match_id is incorrect return error
    """
    info=svc.get_match_complete_info(match_id)
    if not info:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return info

@router.post("/add-managers")
async def add_managers(match_id, home_team_manager: str, away_team_manager: str, token: str=Depends(oauth2_scheme)):
    """
    Add the managers to the match in the db.
    If match_id is incorrect, managars are confirmed, managers have been alredy added, home_team_manager is incorrect
    or away_team_manager is incorrect return error
    """
    result=svc.add_managers(match_id,home_team_manager,away_team_manager)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"managers already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"managers already added"},status_code=403)
    if result==4:
        return responses.JSONResponse(content={"message":f"manager {home_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    if result==5:
        return responses.JSONResponse(content={"message":f"manager {away_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    return {"message":"managers added successfully!"}

@router.post("/add-officials")
async def add_officials(match_id, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str, token: str=Depends(oauth2_scheme)):
    """
    Add the officials to the match in the db.
    If match_id is incorrect, officials are confirmed or officials have been already added return error
    """
    result=svc.add_officials(match_id,arbitrator,linesman1,linesman2,fourth_man)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"officials already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"officials already added"},status_code=403)
    return {"message":"officials added successfully!"}

@router.post("/change-officials-managers")
async def change_officials_and_managers(match_id, home_team_manager: str, away_team_manager: str, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str, token: str=Depends(oauth2_scheme)):
    """
    Change the officials and managers of the match in the db.
    If match_id is incorrect, values are confirmed, home_team_manager is incorrect or away_team_manager is incorrect return error
    """
    result=svc.change_off_and_man(True, match_id, None, home_team_manager, away_team_manager, arbitrator, linesman1, linesman2, fourth_man)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"officials and managers already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":f"manager {home_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    if result==4:
        return responses.JSONResponse(content={"message":f"manager {away_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    return {"message":"values updated and confirmed successfully!"}

@router.post("/assess-officials-managers")
async def assess_officials_and_managers(match_id, username: str, token: str=Depends(oauth2_scheme)):
    """
    Confirm definetely the match officials and managers.
    If match_id is incorrect, values are confirmed or values haven't been added yet.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_off_and_man(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"values already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"values not added yet"}, status_code=403)
    return {"message":"values confirmed successfully!"}

@router.post("/modify-officials-managers")
async def modify_officials_and_managers(match_id, username: str, home_team_manager: str, away_team_manager: str, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str, token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definetely the officials and managers.
    If match_id is incorrect, analysis of the match started, home_team_manager is incorrect or away_team_manager is incorrect return error.
    Only administrators and editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.change_off_and_man(False, match_id, username, home_team_manager, away_team_manager, arbitrator, linesman1, linesman2, fourth_man)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"analysis of the match already started"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":f"manager {home_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    if result==4:
        return responses.JSONResponse(content={"message":f"manager {away_team_manager} is incorrect or has not yet been saved in db"},status_code=400)
    return {"message":"values updated and confirmed successfully!"}


@router.post("/add-home-team-formation")
async def add_home_formation(match_id, player_names: List[str], player_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Add to the match the formation of the home team, the order must be lineup then bench and 
    the lineup should be in order goalkeeper->defenders->midfielders->strikers from left to right.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    home_team_formation is confirmed, home_team_formation has been already added or there is an incorrect player_name
    return error
    """
    #debug
    #print(player_names,player_numbers)
    l1=len(player_names)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 players"},status_code=400)
    l2=len(player_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} player_names but {l2} player_numbers"},status_code=400)
    for pn in player_numbers:
        if pn<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.add_team_formation(match_id, True, player_names, player_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match home formation already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"match home formation already added"},status_code=403)
    if result!=0:
        return responses.JSONResponse(content={"message":f"player_name {result} is incorrect or has not yet been saved in db"},status_code=400)
    return {"message":"home formation addedd successfully!"}

##ALTERNATIVE VERSION
# async def add_home_formation(match_id, players: List[svc.Name_and_number]):
#     """
#     Add to the match the formation of the home team, the order must be lineup then bench and the lineup should be in order gk->d->m->s from left to right.
#     If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
#     home_team_formation is confirmed, home_team_formation has been already added or there is an incorrect player_name
#     return error
#     """
#     #debug
#     print(players)
#     l1=len(players)
#     if l1!=22:
#         return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 players"},status_code=400)
#     for p in players:
#         p.number<0 or p.number>100
#         return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
#     result=svc.add_team_formation(match_id, True, players)
#     if result==1:
#         return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
#     if result==2:
#         return responses.JSONResponse(content={"message":"match home formation already confirmed"},status_code=403)
#     if result==3:
#         return responses.JSONResponse(content={"message":"match home formation already added"},status_code=403)
#     if result!=0:
#         return responses.JSONResponse(content={"message":f"player_name {result} is incorrect or has not yet been saved in db"},status_code=400)
#     return {"message":"home formation addedd successfully!"}

@router.post("/add-away-team-formation")
async def add_away_formation(match_id, player_names: List[str], player_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Add to the match the formation of the away team, the order must be lineup then bench and 
    the lineup should be in order goalkeeper->defenders->midfielders->strikers from left to right.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    away_team_formation is confirmed, away_team_formation has been already added or there is an incorrect player_name
    return error
    """
    l1=len(player_names)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 players"},status_code=400)
    l2=len(player_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} player_names but {l2} player_numbers"},status_code=400)
    for pn in player_numbers:
        if pn<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.add_team_formation(match_id, False, player_names, player_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match away formation already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"match away formation already added"},status_code=403)
    if result!=0:
        return responses.JSONResponse(content={"message":f"player_name {result} is incorrect or has not yet been saved in db"},status_code=400)
    return {"message":"away formation addedd successfully!"}

@router.post("/change-home-team-formation")
async def change_home_formation(match_id, home_team_players: List[str], home_team_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Change the home formation of the match in the db.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    home_team_formation hasn't been already added or home_team_formation is confirmed return error
    """
    l1=len(home_team_players)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 home_team_players"},status_code=400)
    l2=len(home_team_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} home_team_players but {l2} home_team_numbers"},status_code=400)
    for n in home_team_numbers:
        if n<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.change_formation(True, match_id, True, None, home_team_players, home_team_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Home formation is absent, use the function add-home-team-formation"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"Home formation already confirmed"},status_code=403)
    return {"message":"Home formation updated successfully!"}

@router.post("/change-away-team-formation")
async def change_away_formation(match_id, away_team_players: List[str], away_team_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Change the away formation of the match in the db.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    away_team_formation hasn't been already added or away_team_formation is confirmed return error
    """
    l1=len(away_team_players)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 home_team_players"},status_code=400)
    l2=len(away_team_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} home_team_players but {l2} home_team_numbers"},status_code=400)
    for n in away_team_numbers:
        if n<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.change_formation(True, match_id, True, None, away_team_players, away_team_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Away formation is absent, use the function add-away-team-formation"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"Away formation already confirmed"},status_code=403)
    return {"message":"Away formation updated successfully!"}

@router.post("/assess-home-formation")
async def assess_home_formation(match_id, username: str, token: str=Depends(oauth2_scheme)):
    """
    Confirm definetely the match home formation.
    If match_id is incorrect, home_team_formation is confirmed or home_team_formation hasn't been added yet return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_formation(match_id, True, username)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Home formation already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"Home formation not added yet"},status_code=403)
    return {"message":"home formation confirmed successfully!"}

@router.post("/assess-away-formation")
async def assess_away_formation(match_id, username: str, token: str=Depends(oauth2_scheme)):
    """
    Confirm definetely the match away formation.
    If match_id is incorrect, away_team_formation is confirmed
    or away_team_formation hasn't been added yet return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_formation(match_id, False, username)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Away formation already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"Away formation not added yet"},status_code=403)
    return {"message":"away formation confirmed successfully!"}

@router.post("/modify-home-team-formation")
async def modify_home_formation(match_id, username: str, home_team_players: List[str], home_team_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definetely the home formation.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    home_team_formation hasn't been added yet or analysis started return error.
    Only administrators and editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    l1=len(home_team_players)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 home_team_players"},status_code=400)
    l2=len(home_team_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} home_team_players but {l2} home_team_numbers"},status_code=400)
    for n in home_team_numbers:
        if n<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.change_formation(False, match_id, True, username, home_team_players, home_team_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Home formation is absent, use the function add-home-team-formation"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"analysis of the match already started"},status_code=403)
    return {"message":"Home formation updated and confirmed successfully!"}

@router.post("/modify-away-team-formation")
async def modify_away_formation(match_id, username: str, away_team_players: List[str], away_team_numbers: List[int], token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definetely the away formation.
    If the number of values is incorrect, there is an invalid shirt number, match_id is incorrect,
    away_team_formation hasn't been added yet or analysis started return error.
    Only administrators and editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    l1=len(away_team_players)
    if l1!=22:
        return responses.JSONResponse(content={"message":"Incorrect number of values, you must insert 22 home_team_players"},status_code=400)
    l2=len(away_team_numbers)
    if l1!=l2:
        return responses.JSONResponse(content={"message":f"Incorrect number of values, there are {l1} home_team_players but {l2} home_team_numbers"},status_code=400)
    for n in away_team_numbers:
        if n<0:
            return responses.JSONResponse(content={"message":"Invalid shirt number value"},status_code=400)
    result=svc.change_formation(False, match_id, False, username, away_team_players, away_team_numbers)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Away formation is absent, use the function add-away-team-formation"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"analysis of the match already started"},status_code=403)
    return {"message":"Away formation updated and confirmed successfully!"}

@router.post("/change-info")
async def change_match_info(match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date_str: str, extended_time: bool, penalty: bool, token: str=Depends(oauth2_scheme)):
    """
    Change the info of the match in the db.
    If date_str is in a wrong format, match_id is incorrect or match is confirmed return error
    """
    if date_str!="" or date_str!=" ":
        try:
            date=datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            try:
                date=datetime.strptime(date_str, '%d/%m/%y')
            except:
                return responses.JSONResponse(content={"message":f"date {date_str} is in a wrong format"},status_code=400)
    else:
        date=None
    
    result=svc.change_info(True, None, match_id, home_team, away_team, season, competition_name, round, date, extended_time, penalty)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match already confirmed"},status_code=403)
    return {"message":"Match name updated successfully!"}

@router.post("/assess-info")
async def assess_info(username: str, match_id, token: str=Depends(oauth2_scheme)):
    """
    Confirm definitely the match info in the db.
    If match_id is incorrect or match info are confirmed return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_info(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match_name already confirmed"},status_code=400)
    return {"message":"match_name confirmed successfully!"}

@router.post("/modify-info")
async def modify_info(username: str, match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date_str: str, extended_time: bool, penalty: bool, token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definitely the match info.
    If date_str is in a wrong format, match_id id is incorrect or analysis of the match started return error
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    
    if date_str!="" or date_str!=" ":
        try:
            date=datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            try:
                date=datetime.strptime(date_str, '%d/%m/%y')
            except:
                return responses.JSONResponse(content={"message":f"date {date_str} is in a wrong format"},status_code=400)
    else:
        date=None
    
    result=svc.change_info(False, username, match_id, home_team, away_team, season, competition_name, round, date, extended_time, penalty)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"analysis of the match already started"},status_code=403)
    return {"message":"Match name updated successfully!"}

@router.post("/add-link")
async def add_link(match_id, link: HttpUrl, token: str=Depends(oauth2_scheme)):
    """
    Add the link to the match in the db.
    If match_id is incorrect or link has been already added return error
    """
    result=svc.add_link(match_id, link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"link of the match already added"},status_code=403)
    return {"message":"Link added successfully!"}

@router.post("/change-link")
async def change_match_link(match_id, new_link: HttpUrl, token: str=Depends(oauth2_scheme)):
    """
    Change the link of the match in the db.
    If match_id is incorrect or match link is confirmed return error
    """
    result=svc.change_link(True, None, match_id, new_link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match link already confirmed"},status_code=403)
    return {"message":"Match link updated successfully!"}

@router.post("/assess-link")
async def assess_link(username: str, match_id, token: str=Depends(oauth2_scheme)):
    """
    Confirm definitely the match link in the db.
    If match_id is incorrect or link is confirmed return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_link(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"link already confirmed"},status_code=400)
    return {"message":"link confirmed successfully!"}

@router.post("/modify-link")
async def modify_link(username: str,match_id, link: HttpUrl, token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definitely the match link.
    If match_id is incorrect or analysis of the match started return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.change_link(False, username, match_id, link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==3:
        return responses.JSONResponse(content={"message":"analysis of the match already started"},status_code=403)
    return {"message":"link updated and confirmed successfully!"}

@router.get("/get-report")
async def get_match_report(match_id, token: str=Depends(oauth2_scheme)):
    """
    Get the match report of the specified match.
    If match_id is incorrect return error
    """
    report_link=svc.get_match_report(match_id)
    if not report_link:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return report_link

@router.post("/add-report")
async def add_match_report(match_id, report_link: HttpUrl, token: str=Depends(oauth2_scheme)):#report is Json?
    """
    Add the report to the match in the db.
    If match_id is incorrect or match report has been already added return error
    """
    result=svc.add_match_report(match_id, report_link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match report already added"},status_code=400)
    return {"message":"Report added successfully!"}

##ALTERNATIVE VERSION
# async def add_match_report(match_id, report: UploadFile= File(...)):#, token: str=Depends(oauth2_scheme)):#report is Json?
#     """
#     Add the report to the match in the db.
#     If match_id is incorrect or match report has been already added return error
#     """
#     #debug
#     print(report.filename)

@router.post("/change-report")
async def change_match_report(match_id, report_link: HttpUrl, token: str=Depends(oauth2_scheme)):
    """
    Change the report of the match in the db.
    If match_id is incorrect or match report is confirmed return error
    """
    result=svc.change_match_report(True, None, match_id, report_link)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match report already confirmed"},status_code=403)
    return {"message":"Match report updated successfully!"}

@router.post("/assess-report")
async def assess_match_report(username: str, match_id, token: str=Depends(oauth2_scheme)):
    """
    Confirm definitely the match report in the db.
    If match_id is incorrect, match report is confirmed or match report hasn't been added yet return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_match_report(username, match_id)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"Report already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"Report not added yet"},status_code=403)
    return {"message":"Report confirmed successfully!"}

@router.post("/modify-report")
async def modify_match_report(username: str, match_id, report_link: HttpUrl, token: str=Depends(oauth2_scheme)):
    """
    Modify and confirm definitely the match report.
    If match_id is incorrect return error.
    Only administrators or editors can call this function
    """
    role=verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if svc.change_match_report(False, username, match_id, report_link)==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return {"message":"report updated and confirmed successfully!"}

@router.get("/get-workers")
async def get_workers(match_id, token: str=Depends(oauth2_scheme)): #NON IMPLEMENTATA PER SCELTA, si potrebbe rimuovere
    """
    Get the workers set of the match from db.
    If match_id is incorrect return error
    """
    worker_list=svc.get_workers(match_id)
    if not worker_list:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return worker_list

@router.get("/get-free-slot")
async def get_free_time_slot(match_id, token: str=Depends(oauth2_scheme)):
    """
    Return the list of the link and the free time slots of the match from db.
    If match_id is incorrect, match is completed, match values aren't confirmed return error
    """
    time_slots=svc.get_free_time_slot(match_id)
    if time_slots==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if time_slots==2:
        return responses.JSONResponse(content={"message":"match is already completed"},status_code=403)
    if time_slots==3:
        return responses.JSONResponse(content={"message":"match name is not confirmed"},status_code=403)
    if time_slots==4:
        return responses.JSONResponse(content={"message":"link is not confirmed"},status_code=403)
    if time_slots==5:
        return responses.JSONResponse(content={"message":"officials and amanagers are not confirmed"},status_code=403)
    if time_slots==6:
        return responses.JSONResponse(content={"message":"home formation is not confirmed"},status_code=403)
    if time_slots==7:
        return responses.JSONResponse(content={"message":"away formation is not confirmed"},status_code=403)
    return time_slots

@router.post("/analyze-slot")
async def analyze_time_slot(username: str, match_id, data_index: int, token: str=Depends(oauth2_scheme)):
    """
    Signal the server that a user started processing the time slot and return the string in the json format needed by soccerLogger to start working on the match.
    If match_id is incorrect, match is completed, match values aren't confirmed or
    the chosen time_slot is being analyzed by another user return error.
    This function should be called after "get_free_time_slot"
    """
    if data_index<0 or data_index>28:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.analyze_time_slot(username, match_id, data_index)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match is completed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"match values haven't been confirmed yet"},status_code=403)
    if result==4:
        return responses.JSONResponse(content={"message":"time_slot is being analyzed by another user"},status_code=400)
    soccerLogger_json_input=json.dumps(result, indent=4)
    return soccerLogger_json_input

@router.post("/add-detail")
async def add_detail(username: str, match_id, data_index: int, detail: str, token: str=Depends(oauth2_scheme)):
    """
    Add the result of the analysis to the match in the db.
    If match_id is incorrect, match is completed, match values aren't confirmed or
    the chosen time_slot is being analyzed by another user return error.
    This function should be called after "analyze_time_slot"
    """
    json_list_detail: List[Dict[str,Any]]=json.loads(detail)
    #AGGIUNGERE CONTROLLI SUL TIPO?
    if data_index<0 or data_index>28:
        return responses.JSONResponse(content={"message":f"data_index {data_index} is incorrect"},status_code=400)
    result=svc.add_detail(username,match_id,data_index,json_list_detail)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"match is completed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"match values haven't been confirmed yet"},status_code=403)
    if result==4:
        return responses.JSONResponse(content={"message":"time_slot is being analyzed by another user"},status_code=400)
    return {"message":"match detail updated successfully!"}

@router.get("/get-analysis")
async def get_analysis(match_id, n: int, token: str=Depends(oauth2_scheme)):
    """
    Get n anaysis of the match from db, if n==0 get all analysis.
    If n<0 or match_id is incorrect return error
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid n value"},status_code=400)
    analysis=svc.get_analysis(match_id, n)
    if not analysis:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return analysis

@router.get("/get-elaborated-analysis")
async def get_elaborated_analysis(match_id, n: int, token: str=Depends(oauth2_scheme)):
    """
    Get n elaborated analysis of the match from db, if n==0 get all elaborated analysis of the match.
    If n<0, match_id is incorrect or this match doesn't have any elaborated analysis return error
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid n value"},status_code=400)
    e_analysis=svc.get_elaborated_analysis(match_id, n)
    if e_analysis==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if not e_analysis:
        return responses.JSONResponse(content={"message":"this match doesn't have any elaborated analysis"},status_code=400)
    return e_analysis

@router.post("/validate")
async def validate_analysis(username: str, match_id, data_index: int, judgement: bool, token: str=Depends(oauth2_scheme)): #token: str=Depends(oauth2_scheme)):
    """
    Add a new judgement to the analysis of the match in the db.
    If match_id is incorrect, the specified analysis is confirmed or there is no detail to validate return error
    """
    if data_index<0 or data_index>28:
        return responses.JSONResponse(content={"message":"invalid data_index, it can be from 0 to 28"},status_code=400)
    result=svc.validate_analysis(username,match_id,data_index,judgement)
    if result==1:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"analysis already confirmed"},status_code=403)
    if result==3:
        return responses.JSONResponse(content={"message":"no detail to validate"},status_code=400)
    return {"message":"Analysis judgement updated successfully!"}

@router.get("/journal")
async def read_journal(match_id, token: str=Depends(oauth2_scheme)):
    """
    Return the journal of the match in the db.
    If match_id is incorrect return error
    """
    journal=svc.read_journal(match_id)
    if not journal:
        return responses.JSONResponse(content={"message":"match_id is incorrect"},status_code=400)
    return journal