from fastapi import APIRouter, responses#, Depends
#from .dependencies import get_token_header

router = APIRouter(
    prefix="/competitions",
    tags=["competitions"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

competition_db=[{"name":"Serie A","code":"ITA 1"}]

@router.get("")
async def get_competition_list():
    """
    Return the competition list from db
    """
    return competition_db

@router.post("/{competition_name}")
async def add_competition(competition_name: str):
    """
    Add competition to the collection, if competition already exists return error
    """
    for c in competition_db:
        if c["name"]==competition_name:
            return responses.JSONResponse(content={"message":"competition already exists"}, status_code=400)
    competition_db.append({"name":competition_name,"code":""})
    return {"message":"competition added succesfully!"}

@router.post("/{new_competition_name}")
async def change_competition(competition_name:str, new_competition_name:str):
    """
    Change the competition name, if competition inexistent or already confirmed definetely return error
    """
    for c in competition_db:
        if c["name"]==competition_name and c["code"]=="":
            c.update({"name":new_competition_name})
            return {"message":"competition name updated successfully!"}
    return responses.JSONResponse(content={"message":"competition already confirmed"}, status_code=400)

@router.post("/{competition_name}")
async def assess_competition(competition_name: str, competition_code: str):
    """
    Confirm definetely the competition name and add the competition code
    Only administrators or editors can call this function
    """
    for c in competition_db:
        if c["name"]==competition_name:
            c.update({"code":competition_code})
            return {"message":"competition confirmed successfully!"}
    return responses.JSONResponse(content={"message":"competition_name is incorrect"}, status_code=400)

@router.post("/{new_competition_name}")
async def modify_competition(competition_name: str, new_competition_name: str, new_competition_code: str):
    """
    Modify and confirm definetely the competition name and code
    Only administrators or editors can call this function
    """
    for c in competition_db:
        if c["name"]==competition_name or c["code"]==competition_name:
            c.update({"name":new_competition_name},{"code":new_competition_code})
            return {"message":"competition updated and confirmed successfully!"}
    return responses.JSONResponse(content={"message":"competition_name is incorrect"}, status_code=400)