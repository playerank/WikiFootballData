from fastapi import APIRouter, responses#, Depends
#from .dependencies import get_current_username

router = APIRouter(
    prefix="/players",
    tags=["players"]#,#Possibile implementazione della sicurezza
    # dependencies=[Depends(get_current_username)],
    # responses={404: {"description":"not found"}},
)