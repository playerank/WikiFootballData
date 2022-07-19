from fastapi import APIRouter, Depends, responses
from usersAPI import oauth2_scheme
import services.data_service as svc

router = APIRouter(
    prefix="/competitions",
    tags=["competitions"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("")
async def get_competition_list():
    """
    Return the competition list from db
    """
    competition_list=svc.get_competitions()
    return competition_list

@router.post("/add")
async def add_competition(competition_name: str):
    """
    Add competition to the collection, if competition already exists return error
    """
    if not svc.add_competition(competition_name):
        return responses.JSONResponse(content={"message":f"Competition {competition_name} already exists"}, status_code=400)
    return {"message":"competition added succesfully!"}
    
@router.post("/change")
async def change_competition(competition_name:str, new_competition_name:str):
    """
    Change the competition name, if competition inexistent or already confirmed definetely return error
    """
    result=svc.change_competition_name(competition_name,new_competition_name)
    if result==1:
        return responses.JSONResponse(content={"message":"competition_name is incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"competition already confirmed"}, status_code=403)
    return {"message":"competition name updated successfully!"}

@router.post("/assess")
async def assess_competition(username: str, competition_name: str, competition_code: str):
    """
    Confirm definetely the competition name and add the competition code, if competition inexistent or already confirmed definetely return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    result=svc.assess_competition(competition_name,competition_code)
    if result==1:
        return responses.JSONResponse(content={"message":"competition_name is incorrect"}, status_code=400)
    if result==2:
        return responses.JSONResponse(content={"message":"competition already confirmed"}, status_code=403)
    return {"message":"competition confirmed successfully!"}

@router.post("/modify")
async def modify_competition(username: str, competition_name: str, new_competition_name: str, new_competition_code: str):
    """
    Modify and confirm definetely the competition name and code, if competition inexistent return error
    Only administrators or editors can call this function
    """
    role=svc.verify_role(username)
    if role!="A" and role!="E":
        return responses.JSONResponse(content={"message":"Forbidden Operation"},status_code=403)
    if not svc.modify_competition(competition_name,new_competition_name,new_competition_code):
        return responses.JSONResponse(content={"message":"competition_name is incorrect"}, status_code=400)
    return {"message":"competition updated and confirmed successfully!"}