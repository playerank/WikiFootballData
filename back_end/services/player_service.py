from data.players import Player
from datetime import datetime
from bson import ObjectId
from typing import List
from services.team_service import get_team_id

def get_player_id(player_name: str) -> ObjectId | None:
    """
    Return the id of the player identified by player_name
    """
    player: Player=Player.objects(player_name=player_name).first()
    if not player:
        return None
    return player.id

def get_player_by_id(id: ObjectId):
    """
    Return the player identified by id
    """
    player: Player=Player.objects(id=id).first()
    return player

def get_player(player_name: str, date_of_birth: datetime) -> Player:
    """
    Return the player identified by player_name
    """
    player: Player=Player.objects().filter(player_name=player_name).filter(date_of_birth=date_of_birth).first()
    return player

def get_players(n: int):
    """
    Return list of n players from db
    """
    if n==0:
        players:List[Player]=list(Player.objects().all())
    else:
        players:List[Player]=list(Player.objects[:n])
    return players

def add_player(player_name: str, date_of_birth: datetime, nationality: str, current_team: str, club_shirt_number: int, national_team_shirt_number: int):
    """
    Create a player and add it to the db.
    Return 1 if club shirt number is invalid, 2 if current_team is incorrect, 3 if nationality is incorrect, 4 if player already exists in the db
    """
    if club_shirt_number<=0 and current_team!="free agent":
        return 1
    if national_team_shirt_number==0 or national_team_shirt_number<=0:
        national_team_shirt_number=-1
    team_id=get_team_id(current_team)
    if not team_id:
        return 2
    national_team_id=get_team_id(nationality)
    if not national_team_id:
        return 3
    e_player=get_player(player_name, date_of_birth)
    if e_player:
        return 3
    player=Player()
    player.player_name=player_name
    player.date_of_birth=date_of_birth
    player.team_id=team_id
    player.national_team_id=national_team_id
    player.club_shirt_number=club_shirt_number
    player.national_team_shirt_number=national_team_shirt_number
    player.save()
    return 0

def change_player(check: bool, player_name: str, date_of_birth: datetime, new_player_name: str, new_date_of_birth: datetime, new_nationality: str):
    """
    Change the name of an existing team and if not check confirm it definetely
    Return 1 if the player doesn't exist, 2 if check and the team is already confirmed, 3 if nationality is incorrect
    """
    e_player=get_player(player_name, date_of_birth)
    if not e_player:
        return 1
    if check and e_player.is_confirmed:
        return 2
    if new_player_name!=" ":
        e_player.player_name=new_player_name
    if new_date_of_birth!=None:
        e_player.date_of_birth=new_date_of_birth
    if new_nationality!=" ":
        national_team_id=get_team_id(new_nationality)
        if not national_team_id:
            return 3
        e_player.national_team_id=national_team_id
    if not check:
        e_player.is_confirmed=True
    e_player.save()
    return 0

def assess_player(player_name: str, date_of_birth: datetime):
    """
    Confirm an existing player.
    Return 1 if the player doesn't exist, 2 if the player is already confirmed
    """
    e_player=get_player(player_name, date_of_birth)
    if not e_player:
        return 1
    if e_player.is_confirmed:
        return 2
    e_player.update(is_confirmed=True)
    return 0

def update_player_conditions(player_name: str, date_of_birth: datetime, new_team: str, new_club_shirt_number: int, new_national_team_shirt_number: int):
    """
    Update the condition of an existing player.
    Return 1 if the player doesn't exist, 2 if new_club_shirt_number is invalid, 3 if current_team is incorrect
    """
    e_player=get_player(player_name, date_of_birth)
    if not e_player:
        return 1
    if new_club_shirt_number<=0 and (new_team!="free agent" or (new_team!=" " and e_player.team_id!=get_team_id("free agent"))):
        return 2
    if new_team!=" ":
        team_id=get_team_id(new_team)
        if not team_id:
            return 3
        e_player.team_id=team_id
    if new_national_team_shirt_number>0:
        e_player.national_team_shirt_number=new_national_team_shirt_number
    e_player.club_shirt_number=new_club_shirt_number
    e_player.save()
    return 0