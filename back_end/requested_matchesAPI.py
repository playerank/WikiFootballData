from fastapi import APIRouter, responses
import services.data_service as svc #COSI' FUNZIONA
# import services.requested_match_service as svc

router = APIRouter(
    prefix="/requested_matches",
    tags=["requested_matches"]
)

@router.get("/")
async def get_requested_match_list(n: int):
    """
    Get n requested matches, if n==0 then return all requested matches
    """
    if n<0:
        return responses.JSONResponse(content={"message":"invalid value"},status_code=400)
    requested_match_list=svc.get_requested_matches(n)
    return requested_match_list

@router.post("/add_match")
async def add_requested_match(home_team: str, away_team: str,competition_name: str, season: str):
    """
    Add a match to the requested match list
    """
    if not svc.add_r_match(home_team,away_team,competition_name,season):
        return responses.JSONResponse(content={"message":"match already exists"},status_code=400)
    return {"message":"match added succesfully!"}