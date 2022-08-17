from data.teams import Team
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

def add_team(team_name: str) -> bool:
    """
    Create a team and add it to the db.
    Return True if operation is successful, False otherwise
    """
    e_team=get_team(team_name)
    if e_team:
        return False
    team=Team()
    team.team_name=team_name
    team.save()
    return True

def change_team_name(check: bool, team_name: str, new_team_name: str):
    """
    Change the name of an existing team.
    Return 1 if the team doesn't exist, 2 if the team is already confirmed
    """
    team=get_team(team_name)
    if not team:
        return 1
    if check and team.is_confirmed:
        return 2
    if check:
        team.update(team_name=new_team_name)
    else:
        team.update(team_name=new_team_name, is_confirmed=True)
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