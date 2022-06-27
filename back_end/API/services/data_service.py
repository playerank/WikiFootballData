from typing import List
from data.users import User
from data.requested_matches import Requested_match
from data.competitions import Competition

#USERS_API TESTED

def create_user(username: str, password: str) -> User:
    """
    Create User and add it to db
    """
    user= User()
    user.username=username
    user.password=password
    user.is_online=False # se è sempre così si può mettere default=False nella classe User
    #Valore is_editor e is_administrator sono di default settati a False
    user.save()
    return user

def find_user_by_username(username: str) -> User:
    """
    Return the User indentified by username
    """
    #query di oggetti user con username=username, io ne voglio solo uno, così indico di fermarsi al primo,
    #ovviamente esendo univoco ce n'è solo uno.
    #User.objects().filter(username=username).first() query vera, se c'è un solo filtro posso usare ->
    user= User.objects(username=username).first()
    return user

def log_user(username: str, password: str) -> str:
    """
    Return U if username is incorrect, P if password is incorrect, L if user already logged,
    A if user is admin, E if user is admin and S if is a simple user
    """
    user:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not user:
        return "U"
    if user.password!=password:
        return "P"
    if user.is_online:
        return "L"
    #L'operazione ha successo
    user.update(is_online=True)
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    else:
        return "S"

def add_editor(username: str) -> bool:
    """
    Return True if operation succeeded, False otherwise
    """
    new_editor:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not new_editor:
        return False
    new_editor.update(is_editor=True)
    return True

def get_users() -> List[User]:
    users:List[User]=list(User.objects().only('username','is_online','is_editor','is_administrator').all())
    #debug
    # for u in users:
    #     print("Utente {}: online {}, editor {}, administrator {}".format(u.username,u.is_online,u.is_editor,u.is_administrator))
    return users

def get_online_users() -> List[User]:
    online_users=list(User.objects().filter(is_online=True).only('username','is_editor','is_administrator').all())
    return online_users

#REQUESTED_MATCHES_API TESTED

def add_r_match(ht: str,at: str,cn: str,sn: str) -> int:
    existing_r_match: Requested_match=Requested_match.objects() \
        .filter(home_team=ht) \
        .filter(away_team=at) \
        .filter(competition_name=cn) \
        .filter(season_name=sn) \
        .first()
    if existing_r_match:
        #debug
        # print("Match esistente {} - {}, {} {}".format(existing_r_match.home_team,existing_r_match.away_team,existing_r_match.competition_name,existing_r_match.season_name))
        return 1
    r_match=Requested_match()
    r_match.home_team=ht
    r_match.away_team=at
    r_match.competition_name=cn
    r_match.season_name=sn
    r_match.save()
    return 0

def get_requested_matches() -> List[Requested_match]:
    r_matches:List[Requested_match]=list(Requested_match.objects().all())
    #debug
    # for r in r_matches:
    #     print("r_match {} - {}, {} {}".format(r.home_team,r.away_team,r.competition_name,r.season_name))
    return r_matches

#COMPETITIONS_API

def get_competition(competition_name: str) -> Competition:
    competition: Competition=Competition.objects(competition_name=competition_name).first()
    return competition

def get_competitions() -> List[Competition]:
    competitions:List[Competition]=list(Competition.objects().all())
    #debug
    # for c in competitions:
    #     print("Competizione {}, codice {}, confermata? {}".format(c.competition_name,c.competition_code,c.is_confirmed))
    return competitions

def add_competition(competition_name: str) -> int:
    e_competition=get_competition(competition_name)
    if e_competition:
        #debug
        # print("Competizione esistente {}, codice {}, confermata? {}".format(e_competition.competition_name,e_competition.competition_code,e_competition.is_confirmed))
        return 1
    competition=Competition()
    competition.competition_name=competition_name
    competition.save()
    return 0

def change_competition_name(competition_name: str, new_competition_name: str) -> int:
    competition=get_competition(competition_name)
    if not competition:
        return 1
    if competition.is_confirmed:
        return 2
    competition.update(competition_name=new_competition_name)
    return 0

def assess_competition(competition_name: str, competition_code: str) -> int:
    competition=get_competition(competition_name)
    if not competition:
        return 1
    if competition.is_confirmed:
        return 2
    competition.update(competition_code=competition_code,is_confirmed=True)
    return 0

def modify_competition(competition_name: str, new_competition_name: str, new_competition_code: str) -> int:
    competition=get_competition(competition_name)
    if not competition:
        return 1
    if new_competition_name==" ":
        competition.update(competition_code=new_competition_code)
    elif new_competition_code==" ":
        competition.update(competition_name=new_competition_name)
    else:
        competition.update(competition_name=new_competition_name, competition_code=new_competition_code)
    return 0