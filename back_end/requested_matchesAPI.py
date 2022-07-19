from fastapi import APIRouter, responses
import services.data_service as svc

router = APIRouter(
    prefix="/requested_matches",
    tags=["requested_matches"]
)

@router.get("/")
async def get_requested_match_list():
    """
    Get the requested_match list
    """
    requested_match_list=svc.get_requested_matches()
    return requested_match_list

@router.post("/add_match")
async def add_requested_match(home_team: str, away_team: str,competition_name: str, season: str):
    """
    Add a match to the requested match list
    """
    if not svc.add_r_match(home_team,away_team,competition_name,season):
        return responses.JSONResponse(content={"message":"match already exists"},status_code=400)
    return {"message":"match added succesfully!"}