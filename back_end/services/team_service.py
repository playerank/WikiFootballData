from data.teams import Team
from services.competition_service import get_competition_id
from bson import ObjectId
from typing import List

def get_team_id(team_name: str) -> ObjectId | None:
    """
    Return the id of the team identified by team_name
    """
    team: Team=Team.objects(team_name=team_name).only('id').first()
    if not team:
        return None
    return team.id

def get_team_by_id(id: ObjectId):
    """
    Return the Team identified by id
    """
    team: Team=Team.objects(id=id).first()
    return team

def get_team(team_name: str) -> Team:
    """
    Return the team identified by team_name
    """
    team: Team=Team.objects(team_name=team_name).first()
    return team

def get_teams(n: int) -> List[Team]:
    """
    Return the list of n teams from the db
    """
    if n==0:
        teams:List[Team]=list(Team.objects().all())
    else:
        teams:List[Team]=list(Team.objects[:n])
    #debug
    # for t in teams:
    #     print("Squadra {}, confermata? {}".format(t.team_name,t.is_confirmed))
    return teams

def add_team(team_name: str, competition_name: str):
    """
    Create a team and add it to the db.
    Return 1 if competition_name is incorrect, 2 if team already exists
    """
    competition_id=get_competition_id(competition_name)
    if not competition_id:
        return 1
    e_team=get_team(team_name)
    if e_team:
        return 2
    team=Team()
    team.team_name=team_name
    team.competition_id=competition_id
    team.save()
    return 0

def change_team(check: bool, team_name: str, new_team_name: str, new_competition_name: str):
    """
    Change the name of an existing team. If check confirm it definetely
    Return 1 if the team doesn't exist, 2 if the team is already confirmed, 3 if new_competition_name is incorrect
    """
    team=get_team(team_name)
    if not team:
        return 1
    if check and team.is_confirmed:
        return 2
    if new_competition_name!="":
        competition_id=get_competition_id(new_competition_name)
        if not competition_id:
            return 3
        team.competition_id=competition_id
    if new_team_name!="":
        team.team_name=new_team_name
    if not check:
        team.is_confirmed=True
    team.save()
    return 0

def assess_team(team_name: str) -> int:
    """
    Confirm an existing team.
    Return 1 if the team doesn't exist, 2 if the team is already confirmed
    """
    team=get_team(team_name)
    if not team:
        return 1
    if team.is_confirmed:
        return 2
    team.update(is_confirmed=True)
    return 0