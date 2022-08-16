from data.competitions import Competition
from bson import ObjectId
from typing import List

def get_competition_id(competition_name: str) -> ObjectId | None:
    """
    Return the id of the competition identified by competition_name
    """
    competition: Competition=Competition.objects(competition_name=competition_name).only('id').first()
    if not competition:
        return None
    return competition.id

def get_competition_by_id(id: ObjectId):
    """
    Return the Competition identified by id
    """
    competition: Competition=Competition.objects(id=id).first()
    return competition

def get_competition(competition_name: str) -> Competition:
    """
    Return the competition identified by competition_name
    """
    competition: Competition=Competition.objects(competition_name=competition_name).first()
    return competition

def get_competition_by_id(id: ObjectId) -> Competition:
    """
    Return the competition identified by id
    """
    competition: Competition=Competition.objects(id=id).first()
    return competition

def get_competitions(n: int) -> List[Competition]:
    """
    Return the list of n competitions from the db
    """
    if n==0:
        competitions: List[Competition]=list(Competition.objects().all())
    else:
        competitions: List[Competition]=list(Competition.objects[:n])
    #debug
    # for c in competitions:
    #     print("Competizione {}, codice {}, confermata? {}".format(c.competition_name,c.competition_code,c.is_confirmed))
    return competitions

def add_competition(competition_name: str) -> bool:
    """
    Create a competition and add it to the db.
    Return True if operation is successful, False otherwise
    """
    e_competition=get_competition(competition_name)
    if e_competition:
        #debug
        # print("Competizione esistente {}, codice {}, confermata? {}".format(e_competition.competition_name,e_competition.competition_code,e_competition.is_confirmed))
        return False
    competition=Competition()
    competition.competition_name=competition_name
    competition.save()
    return True

def change_competition_name(competition_name: str, new_competition_name: str):
    """
    Change the name of an existing competition.
    Return 1 if the competition doesn't exist, 2 if the competition is already confirmed
    """
    competition=get_competition(competition_name)
    if not competition:
        return 1
    if competition.is_confirmed:
        return 2
    competition.update(competition_name=new_competition_name)
    return 0

def assess_competition(competition_name: str, competition_code: str):
    """
    Confirm an existing competition.
    Return 1 if the competition doesn't exist, 2 if the competition is already confirmed
    """
    competition=get_competition(competition_name)
    if not competition:
        return 1
    if competition.is_confirmed:
        return 2
    competition.update(competition_code=competition_code,is_confirmed=True)
    return 0

def modify_competition(competition_name: str, new_competition_name: str, new_competition_code: str) -> bool:
    """
    Modify the name, the code or both of an existing competition.
    Return True if operation is successful, False otherwise
    """
    competition=get_competition(competition_name)
    if not competition:
        return False
    if new_competition_name==" ":
        competition.update(competition_code=new_competition_code)
    elif new_competition_code==" ":
        competition.update(competition_name=new_competition_name)
    else:
        competition.update(competition_name=new_competition_name, competition_code=new_competition_code)
    return True