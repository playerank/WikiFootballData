from data.managers import Manager
from datetime import datetime
from bson import ObjectId
from typing import List
from services.team_service import get_team_id

def get_manager_id(manager_name: str) -> ObjectId | None:
    """
    Return the id of the manager identified by manager_name
    """
    manager: Manager=Manager.objects(name=manager_name).first()
    if not manager:
        return None
    return manager.id

def get_manager_by_id(id: ObjectId) -> Manager:
    """
    Return the manager identified by id
    """
    manager: Manager=Manager.objects(id=id).first()
    return manager

def get_manager(manager_name: str, date_of_birth: datetime) -> Manager:
    """
    Return the manager identified by manager_name
    """
    manager: Manager=Manager.objects().filter(name=manager_name).filter(date_of_birth=date_of_birth).first()
    return manager

def get_managers(n: int):
    """
    Return list of n managers from db
    """
    if n==0:
        managers:List[Manager]=list(Manager.objects().all())
    else:
        managers:List[Manager]=list(Manager.objects[:n])
    return managers

def add_manager(manager_name: str, date_of_birth: datetime, nationality: str, current_team: str):
    """
    Create a manager and add it to the db.
    Return 1 if current_team is incorrect, 2 if manager already exists in the db
    """
    team_id=get_team_id(current_team)
    if not team_id:
        return 1
    e_manager=get_manager(manager_name, date_of_birth)
    if e_manager:
        return 2
    manager=Manager()
    manager.name=manager_name
    manager.date_of_birth=date_of_birth
    manager.nationality=nationality
    manager.save()
    return 0

def change_manager(check: bool, manager_name: str, date_of_birth: datetime, new_manager_name: str, new_date_of_birth: datetime, new_nationality: str):
    """
    Change the values of an existing manager and if not check confirm it definetely
    Return 1 if the manager doesn't exist, 2 if check and the values are already confirmed
    """
    e_manager=get_manager(manager_name, date_of_birth)
    if not e_manager:
        return 1
    if check and e_manager.is_confirmed:
        return 2
    if new_manager_name!=" ":
        e_manager.name=new_manager_name
    if new_date_of_birth!=None:
        e_manager.date_of_birth=new_date_of_birth
    if new_nationality!=" ":
        e_manager.nationality=new_nationality
    if not check:
        e_manager.is_confirmed=True
    e_manager.save()
    return 0

def assess_manager(manager_name: str, date_of_birth: datetime):
    """
    Confirm an existing manager.
    Return 1 if the manager doesn't exist, 2 if the manager is already confirmed
    """
    e_manager=get_manager(manager_name, date_of_birth)
    if not e_manager:
        return 1
    if e_manager.is_confirmed:
        return 2
    e_manager.update(is_confirmed=True)
    return 0

def update_manager_team(manager_name: str, date_of_birth: datetime, new_team: str):
    """
    Update the team of an existing manager.
    Return 1 if the manager doesn't exist, 2 if new_team is incorrect
    """
    e_manager=get_manager(manager_name, date_of_birth)
    if not e_manager:
        return 1
    if new_team!=" ":
        team_id=get_team_id(new_team)
        if not team_id:
            return 2
        e_manager.team_id=team_id
    e_manager.save()
    return 0