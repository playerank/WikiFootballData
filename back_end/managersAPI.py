from fastapi import APIRouter, responses, Depends
from usersAPI import oauth2_scheme
from datetime import datetime
import services.manager_service as svc
from services.user_service import verify_role

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("")
async def get_manager_list(n: int):
    """
    Return n managers from db, if n==0 then return all managers
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    managers=svc.get_managers(n)
    return managers

@router.post("/add")
async def add_manager(manager_name: str, date_of_birth_str: str, nationality: str, current_team: str):
    """
    Add manager to the collection, if manager already exists return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    
    result=svc.add_manager(manager_name, date_of_birth, nationality, current_team)
    if result==1:
        return responses.JSONResponse(content={"message":f"current_team {current_team} is incorrect or has not yet been saved in db"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"manager {manager_name} already exists"}, status_code=400)
    return {"message":"manager added succesfully!"}

@router.post("/change")
async def change_manager(manager_name: str, date_of_birth_str: str, new_manager_name: str, new_date_of_birth_str: str, new_nationality: str):
    """
    Change the manager values, if manager inexistent or already confirmed definetely return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    new_date_of_birth=None
    if new_date_of_birth_str!=" ":
        try:
            new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%Y')
        except ValueError:
            try:
                new_date_of_birth=datetime.strptime(new_date_of_birth_str, '%d/%m/%y')
            except:
                return responses.JSONResponse(content={"message":f"date {new_date_of_birth_str} is in a wrong format"},status_code=400)

    result=svc.change_manager(True, manager_name, date_of_birth, new_manager_name, new_date_of_birth, new_nationality)
    if result==1:
        return responses.JSONResponse(content={"message":"manger parameters are incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"player already confirmed"}, status_code=403)
    return {"message":"manager changed successfully!"}

@router.post("/assess")
async def assess_manager(username: str, manager_name: str, date_of_birth_str: str):
    """
    Confirm definetely the manger values, if manager inexistent or already confirmed definetely return error
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
    result=svc.assess_manager(manager_name, date_of_birth)
    if result==1:
       return responses.JSONResponse(content={"message":"manager parameters are incorrect"}, status_code=400) 
    if result==2:
        return responses.JSONResponse(content={"message":"manager already confirmed"}, status_code=403)
    return {"message":"manager confirmed successfully!"}

@router.post("/modify")
async def modify_manager(username: str, manager_name: str, date_of_birth_str: str, new_manager_name: str, new_date_of_birth_str: str, new_nationality: str):
    """
    Modify and confirm definetely the manager values, if manager inexistent return error.
    Only administrators or editors can call this function
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)
    new_date_of_birth=None
    if new_date_of_birth_str!=" ":
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
    if svc.change_manager(False, manager_name, date_of_birth, new_manager_name, new_date_of_birth, new_nationality)==1:
        return responses.JSONResponse(content={"message":"manager parameters are incorrect"}, status_code=400)
    return {"message":"manager modified and confirmed successfully!"}

@router.post("/update")
async def update_manager_team(manager_name: str, date_of_birth_str: str, new_team: str):
    """
    Update the manager current team.
    if the manager doesn't exist return error
    """
    try:
        date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_of_birth=datetime.strptime(date_of_birth_str, '%d/%m/%y')
        except:
            return responses.JSONResponse(content={"message":f"date {date_of_birth_str} is in a wrong format"},status_code=400)

    result=svc.update_manager_team(manager_name, date_of_birth, new_team)
    if result==1:
        return responses.JSONResponse(content={"message":"manager parameters are incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":f"current_team {new_team} is incorrect or has not yet been saved in db"}, status_code=400)
    return {"message":"manager team updated succesfully!"}