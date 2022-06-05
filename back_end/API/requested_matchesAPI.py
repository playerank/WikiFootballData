from fastapi import APIRouter, responses#, Depends
#from .dependencies import get_token_header

router = APIRouter(
    prefix="/requested_matches",
    tags=["requested_matches"],
    #dependencies=[Depends(get_token_header)],
    #responses={404: {"description": "Not found"}},
)

requested_match_list=["Italia-Inghilterra"]

@router.get("/")
async def get_requested_match_list():
    """
    Get the requested_match list
    """
    return requested_match_list

@router.post("/{match_name}")
async def add_requested_match(match_name: str):
    """
    Add a match to the requested match list
    """
    if match_name in requested_match_list:
        return responses.JSONResponse(content={"message":"match already requested"},status_code=400)
    requested_match_list.append(match_name)
    return {"message":"match added succesfully!"}