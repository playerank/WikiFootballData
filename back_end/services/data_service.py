from datetime import datetime
from typing import List
from bson import ObjectId
from pydantic import HttpUrl
from data.users import User
from data.matches import Match, Analysis
from data.events import Event
from data.competitions import Competition
from services.team_service import get_team_id
from data.rules import n
from data.reviews import Review
from services.player_service import get_player_id
from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

#USERS_API
def get_user(username: str) -> User:
    """
    Return the User indentified by username
    """
    #query di oggetti user con username=username, io ne voglio solo uno, così indico di fermarsi al primo,
    #ovviamente esendo univoco ce n'è solo uno.
    #User.objects().filter(username=username).first() query vera, se c'è un solo filtro posso usare ->
    user: User=User.objects(username=username).first()
    return user

def hash_password(password):
    """
    Return the hashed password
    """
    return pwd_context.hash(password)

def create_user(username: str, password) -> User:
    """
    Create User and add it to db, return True if operation is successful, False otherwise
    """
    user= User()
    user.username=username
    user.password=hash_password(password)
    user.is_online=False
    #Valore is_editor e is_administrator sono di default settati a False
    user.save()
    return user

def log_user(username: str, password: str):
    """
    Log a User verifying its password.
    Return U if username is incorrect, P if password is incorrect, L if user already logged,
    A if user is admin, E if user is admin and S if is a simple user
    """
    user:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not user:
        return "U"
    if not pwd_context.verify(password, user.password):
        return "P"
    if user.is_online:
        return "L"
    #L'operazione ha successo
    user.update(is_online=True)
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    return "S"

def verify_role(username: str):
    """
    Return the role of the User identified by username
    """
    user=get_user(username)
    if not user:
        return "U"
    if not user.is_online:
        return "M" #mistake
    if user.is_administrator:
        return "A"
    if user.is_editor:
        return "E"
    return "S" #simple User

def add_editor(username: str) -> bool:
    """
    Change the role of a User to editor.
    Return True if operation is successful, False otherwise
    """
    new_editor:User=User.objects(username=username).first()
    #L'operazione fallisce
    if not new_editor:
        return False
    new_editor.update(is_editor=True)
    return True

def get_users(n: int) -> List[User]:
    """
    Return the list of n Users from the db (clearly not the passwords)
    """
    if n==0:
        users:List[User]=list(User.objects().only('username','is_online','is_editor','is_administrator').all())
    else:
        users:List[User]=list(User.objects[:n].only('username','is_online','is_editor','is_administrator'))
    #debug
    # for u in users:
    #     print("Utente {}: online {}, editor {}, administrator {}".format(u.username,u.is_online,u.is_editor,u.is_administrator))
    return users

def get_online_users() -> List[User]:
    """
    Retrun the list of online Users (clearly not the passwords)
    """
    online_users=list(User.objects().filter(is_online=True).only('username','is_editor','is_administrator').all())
    return online_users

#MATCHES_API

def get_match_id(home_team: str, away_team: str, season: str, competition_name: str):
    """
    Return the id of the match identified by parameters
    """
    competition_id=get_competition_id(competition_name)
    if not competition_id:
        return 1
    home_team_id=get_team_id(home_team)
    if not home_team_id:
        return 2
    away_team_id=get_team_id(away_team)
    if not away_team_id:
        return 3
    match: Match=Match.objects() \
        .filter(home_team_id=home_team_id) \
        .filter(away_team_id=away_team_id) \
        .filter(season=season) \
        .filter(competition_id=competition_id) \
        .only('id').first()
    if not match:
        return 4
    return match.id

def get_match(match_id: ObjectId) -> Match:
    """
    Return the match identified by id
    """
    match: Match=Match.objects(id=match_id).first()
    #debug
    #print("Trovato Match {}-{}, competition_id {} season {}, completato? {}".format(match.home_team_id,match.away_team_id,match.competition_id,match.season,match.is_completed))
    return match

def get_matches(n: int) -> List[Match]:
    """
    Retrun list of n matches in the db
    """
    if n==0:
        matches: List[Match]=list(Match.objects().all())
    else:
        matches: List[Match]=list(Match.objects[:n])
    #debug
    # for m in matches:
    #     print("Match {}-{}, competition_id {} season_id {}, completato? {}".format(m.home_team_id,m.away_team_id,m.competition_id,m.season,m.is_completed))
    return matches

def get_not_completed_matches(n: int) -> List[Match]:
    """
    Return list of n not completed matches in the db
    """
    if n==0:
        nc_matches: List[Match]=list(Match.objects(is_completed=False).all())
    else:
        nc_matches: List[Match]=list(Match.objects[:n].filter(is_completed=False))
    return nc_matches

def get_completed_matches(n: int) -> List[Match]:
    """
    Return the list of n completed matches in the db
    """
    if n==0:
        c_matches: List[Match]=list(Match.objects(is_completed=True).all())
    else:
        c_matches: List[Match]=list(Match.objects[:n].filter(is_completed=True))
    #debug
    # for m in c_matches:
    #     print("Match {}-{}, competition_id {} season {}, completato? {}".format(m.home_team_id,m.away_team_id,m.competition_id,m.season,m.is_completed))
    return c_matches

def get_completed_match_data(match_id: ObjectId) -> List | int:
    """
    Return the list of data of the match identified by match_id.
    1 if the match doesn't exist, 2 if match is not completed
    """
    c_match: Match=Match.objects(id=match_id).only('is_completed','data').first()
    if not c_match:
        return 1
    if not c_match.is_completed:
        return 2
    return c_match.data

def add_match(username: str, home_team: str, away_team: str, season: str, competition_name: str,round: str,date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Create a new Match and add it to the db.
    Return 1 if competition_name is incorrect, 2 if home_team is incorrect, 3 if away_team is incorrect, 4 if already exists a match with that link. The checks are in efficency order
    """
    competition_id=get_competition_id(competition_name)
    if not competition_id:
        return 1
    home_team_id=get_team_id(home_team)
    if not home_team_id:
        return 2
    away_team_id=get_team_id(away_team)
    if not away_team_id:
        return 3
    #il link dovrebbe identificare univocamente un match
    e_match=Match.objects(link=link).only('id').first()
    if e_match:
        return 4
    match=Match()
    match.username=username
    match.home_team_id=home_team_id
    match.away_team_id=away_team_id
    match.season=season
    match.competition_id=competition_id
    match.round=round
    match.date_utc=date
    match.link=link
    match.extended_time=extended_time
    match.penalty=penalty
    match.create_data
    match.save()
    return 0

# def get_match_info(match_id: ObjectId):
#     """
#     Return the info of the match identified by match_id
#     """
#     match=get_match(match_id)
#     if not match:
#         return None
#     info=list()
#     info.append(get_competition_by_id(match.competition_id))
#     info.append(get_team_by_id(match.home_team_id))

def add_managers(match_id: ObjectId, home_team_manager: str, away_team_manager: str):
    """
    Add the managers to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if values are already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.officials_and_managers_are_confirmed:
        return 2
    match.home_team_manager=home_team_manager
    match.away_team_manager=away_team_manager
    match.journal.append(f"Managers added or changed to {home_team_manager} and {away_team_manager}")
    match.save()
    return 0

def add_officials(match_id: ObjectId, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str):
    """
    Add or change the officials to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if values are already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.officials_and_managers_are_confirmed:
        return 2
    match.officials=list()
    match.officials.append(arbitrator)
    match.officials.append(linesman1)
    match.officials.append(linesman2)
    match.officials.append(fourth_man)
    match.journal.append(f"Officials added or changed to {arbitrator}, {linesman1}, {linesman2} and {fourth_man}")
    match.save()
    return 0

def assess_off_and_man(match_id: ObjectId, username: str):
    """
    Confirm definetely values of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if values are already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.officials_and_managers_are_confirmed:
        return 2
    match.officials_and_managers_are_confirmed=True
    match.journal.append(f"Officials and Managers confirmed by {username}")
    match.save()
    return 0

def modify_off_and_man(match_id: ObjectId, username: str, home_team_manager: str, away_team_manager: str, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str) -> bool:
    """
    Modify and confirm definetely the officials and managers of the match identified by match_id.
    Return True if operation is successful, False otherwise
    """
    match=get_match(match_id)
    if not match:
        return False
    if home_team_manager!=" ":
        match.home_team_manager=home_team_manager
    if away_team_manager!=" ":
        match.away_team_manager=away_team_manager
    if arbitrator!=" ":
        match.officials[0]=arbitrator
    if linesman1!=" ":
        match.officials[1]=linesman1
    if linesman2!=" ":
        match.officials[2]=linesman2
    if fourth_man!=" ":
        match.officials[3]=fourth_man
    match.officials_and_managers_are_confirmed=True
    match.journal.append(f"Officials and managers updated and confirmed by {username}")
    match.save()
    return True

def add_team_formation(match_id, team: int, player_names: List[str], player_numbers: List[int]):
    """
    Add or change the home formation to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if formations are confirmed, player_name if player_name is incorrect
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.formations_are_confirmed:
        return 2
    i=0
    for p in player_names:
        player_id=get_player_id(p)
        if not player_id:
            return p
        match.team_append(team,player_id,p,player_numbers[i])
        i+=1
    
    if team==0:
        match.journal.append("Home team formation added or changed")
    else:
        match.journal.append("Away team formation added or changed")
    match.save()
    return 0

def assess_formations(match_id: ObjectId, username: str):
    """
    Confirm definetely the formations of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if formations are already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.formations_are_confirmed:
        return 2
    match.formations_are_confirmed=True
    match.journal.append(f"Formations confirmed by {username}")
    match.save()
    return 0

def modify_formations(match_id: ObjectId, username: str, player_names: List[str], player_numbers: List[str]):
    """
    Modify and confirm definetely the formations of the match identified by match_id.
    Return 1 if the match doesn't exist
    """
    match=get_match(match_id)
    if not match:
        return 1

def get_data(match_id: ObjectId) -> List[Analysis] | None:
    """
    Return the list of data of the match identified by match_id
    """
    match: Match=Match.objects(id=match_id).only('data').first()
    if not match:
        return None
    return match.data

def get_elaborated_data(match_id: ObjectId, n: int) -> List | None:
    """
    Return the list of n elaborated data of the match identified by match_id
    """
    match: Match=Match.objects(id=match_id).only('data').first()
    if not match:
        return None
    if match.is_completed:
        return match.data
    elaborated_data: List[Analysis]=list()
    if n==0:
        n=30
    for d in match.data:
        if d.author!=None:
            elaborated_data.append(d)
            if n==0:
                break
            n-=1
    return elaborated_data


def change_name(check: bool, match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Function that change or modify the match name(depends of the value of check).
    Before changing every value it verify that the new values aren't empty.
    """
    match=get_match(match_id)
    if not match:
        return 1
    if check and match.is_confirmed:
            return 2
    if match.extended_time!=extended_time or match.penalty!=penalty:
        match.extended_time=extended_time
        match.penalty=penalty
        match.change_data
    if season!=" ":
        match.season=season
    if round!=" ":
        match.round=round
    match.date_utc=date
    match.link=link
    if competition_name!=" ":
        competition_id=get_competition_id(competition_name)
        if competition_id:
            match.competition_id=competition_id
    if home_team!=" ":
        home_team_id=get_team_id(home_team)
        if home_team_id:
            match.home_team_id=home_team_id
    if away_team!=" ":
        away_team_id=get_team_id(away_team)
        if away_team_id:
            match.away_team_id=away_team_id
    if check:
        match.journal.append("Match name updated")
    else:
        match.is_confirmed=True
        match.journal.append("Match name updated and confirmed definitely")
    match.save()
    return 0
    

def change_match_link(match_id: ObjectId, new_link: HttpUrl):
    """
    Change the link of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the match link is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.link_is_confirmed:
        return 2
    match.link=new_link
    match.journal.append(f"Match link updated to {new_link}")
    match.save()
    return 0

def change_match_report(match_id: ObjectId, new_report: str):
    """
    Change the report of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the match report is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.report_is_confirmed:
        return 2
    match.report=new_report
    match.journal.append("Match report updated")
    match.save()
    return 0

def get_match_report(match_id: ObjectId):
    """
    Return the report of the meatch identified by match_id
    """
    match:Match=Match.objects(id=match_id).only('report').first()
    if not match:
        return None
    return match.report

def add_match_report(match_id: ObjectId, report):
    """
    Add the match report to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the match report was already present
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.report!=None:
        return 2
    match.report=report
    match.journal.append("Match report added")
    match.save()
    return 0

def get_workers(match_id: ObjectId) -> List[str] | None:
    """
    Return the list of the user that worked on the match identified by match_id
    """
    match:Match=Match.objects(id=match_id).only('working').first()
    if not match:
        return None
    return match.working

def get_free_time_slot(match_id: ObjectId):
    """
    Return the list of the time slot that aren't being analyzed by some user.
    In case of errror return 1 if the match doesn't exist, 2 if the match is already completed
    """
    match:Match=Match.objects(id=match_id).only('data').first()
    if not match:
        return 1
    if match.is_completed:
        return 2
    free_time_slot: List[Analysis]=list()
    for d in match.data:
        if not d.working and not d.author:
            free_time_slot.append(d)
    return free_time_slot

def analyze_time_slot(username: str, match_id: ObjectId, data_index: int):
    """
    Signal in the specified data that the user identified by username is analyzing it.
    Return 1 if the match doesn't exist, 2 if the match is already completed, 3 if the specified data is being analyzed or was analyzed by another user
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.is_completed:
        return 2
    if match.data[data_index].working!=None or match.data[data_index].author!=None:
        return 3
    match.data[data_index].working=username
    match.journal.append(f"User {username} started working at time slot {match.data[data_index].time_slot}")
    match.save()
    return 0

def add_data(username: str, match_id: ObjectId, data_index: int, detail: str):#Json?:
    """
    Add the detail of the specified data.
    Return 1 if the match doesn't exist, 2 if the match is already completed, 3 if the specified data is being analyzed by another user
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.is_completed:
        return 2
    if match.data[data_index].working!=username:
        return 3 
    match.data[data_index].detail=detail
    match.journal.append(f"User {username} ended working at time slot {match.data[data_index].time_slot}")
    match.save()
    return 0

def create_review(username: str, match_id: ObjectId, data_index: int, judgement: bool):
    """
    Create a Review and check some condition.
    Return -1 if the user already validated this data, return 1 if the user removed the endorsement, return 2 if the user changed the judgement from False to True,
    return 3 if the user removed the dislike, return 4 if the user changed the judgement from True to False
    """
    e_review: Review=Review.objects() \
        .filter(match_id=match_id) \
        .filter(data_index=data_index) \
        .filter(username=username) \
        .first() #ritorna l'istanza che ha match_id, data_index e username uguali ai parametri
    if e_review:
        if judgement:
            if e_review.type=="e":#vuole rimuovere mi piace
                e_review.delete()
                return 1
            else:#vuole cambiare da dislike a endorsement
                e_review.type="e"
                e_review.save()
                return 2
        else:
            if e_review.type=="d":#vuole rimuovere non mi piace
                e_review.delete()
                return 3
            else:
                e_review.type="d"
                e_review.save()
                return 4
    #se arrivo qui non esiste review
    review=Review()
    review.match_id=match_id
    review.data_index=data_index
    review.username=username
    if judgement:
        review.type="e"
    else:
        review.type="d"
    review.save()
    return 0


def validate_data(username: str, match_id: ObjectId, data_index: int, judgement: bool):
    """
    Add a judgement to the specified data.
    If the data reach n endorsements it will be added to the event collection and it will start a check to all data, if all data are completed(reached n endorsements), the whole match will be considered completed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.data[data_index].author!=None: #data is confirmed
        return 2
    if not match.data[data_index].detail:
        return 3
    result=create_review(username, match_id, data_index, judgement)
    if judgement:#endorsement
        if result==1:
           match.data[data_index].endorsements-=1
           match.journal.append(f"User {username} removed the endorsement to match data {match.data[data_index].time_slot}, it has now {match.data[data_index].endorsements} endorsements")
           match.save()
           return 0
        match.data[data_index].endorsements+=1
        if result==2:
            match.data[data_index].dislikes-=1
            match.journal.append(f"User {username} removed the dislike to match data {match.data[data_index].time_slot}, it has now {match.data[data_index].dislikes} dislikes")
        match.journal.append(f"Match data {match.data[data_index].time_slot} endorsed by {username}, it has now {match.data[data_index].endorsements} endorsements")
        if match.data[data_index].endorsements>=n:
            match.data[data_index].author=match.data[data_index].working
            match.data[data_index].working="" #qui va bene che diventi "" perchè non devo più toccarlo
            match.journal.append(f"Match data {match.data[data_index].time_slot} is now confirmed because it reached {match.data[data_index].endorsements} endorsements")
            #This analysis is added to collection Events
            event=Event()
            event.match_id=match_id
            event.data_list[data_index].time_slot=match.data[data_index].time_slot
            event.data_list[data_index].detail=match.data[data_index].detail
            event.data_list[data_index].author=match.data[data_index].author
            event.save()

            if match.check_data:
                match.is_completed=True
                match.journal.append("Match is completed because every data reached {} endorsements".format(n))
    else:#dislike
        if result==3:
            match.data[data_index].dislikes-=1
            match.journal.append(f"User {username} removed the dislike to match data {match.data[data_index].time_slot}, it has now {match.data[data_index].dislikes} dislikes")
            match.save()
            return 0
        match.data[data_index].dislikes+=1
        if result==4:
            match.data[data_index].endorsements-=1
            match.journal.append(f"User {username} removed the endorsement to match data {match.data[data_index].time_slot}, it has now {match.data[data_index].endorsements} endorsements")
        match.journal.append(f"Match data {match.data[data_index].time_slot} disliked by {username}, it has now {match.data[data_index].dislikes} dislikes")
        if match.data[data_index].dislikes>=n:
            match.data[data_index].working=None
            match.data[data_index].author=None #così è nuovamente lavorabile
            match.journal.append(f"Match data {match.data[data_index].time_slot} reached {match.data[data_index].dislikes} dislikes, it is suggested to change it")
            #devo fare altro?
    match.save()
    return 0

def read_journal(match_id: ObjectId):
    """
    Return the journal of the match identified by the match_id
    """
    match:Match=Match.objects(id=match_id).only('journal').first()
    if not match:
        return None
    return match.journal

def assess_name(username: str, match_id: ObjectId):
    """
    Confirms definitely the match name.
    Return 1 if the match doesn't exist, 2 if the match name is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.is_confirmed:
        return 2
    match.is_confirmed=True
    match.journal.append(f"Match name has been confirmed by {username}")
    match.save()
    return 0

def assess_link(username: str, match_id: ObjectId):
    """
    Confirms definitely the match link.
    Return 1 if the match doesn't exist, 2 if the match link is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.link_is_confirmed:
        return 2
    match.link_is_confirmed=True
    match.journal.append(f"Match link has been confirmed by {username}")
    match.save()
    return 0

def modify_link(username: str, match_id: ObjectId, link: HttpUrl) -> bool:
    """
    Modify and confirms definitely the match link.
    Return True if operation is successful, False otherwise
    """
    match=get_match(match_id)
    if not match:
        return False
    match.link=link
    match.link_is_confirmed=True
    match.journal.append(f"Match link has been modified and confirmed by {username}")
    match.save()
    return True

def assess_report(username: str, match_id: ObjectId):
    """
    Confirms definitely the match report.
    Return 1 if the match doesn't exist, 2 if the match report is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.report_is_confirmed:
        return 2
    match.report_is_confirmed=True
    match.journal.append(f"Match report has been confirmed by {username}")
    match.save()
    return 0

def modify_report(username: str, match_id: ObjectId, report: HttpUrl) -> bool:
    """
    Modify and confirms definitely the match report.
    Return True if operation is successful, False otherwise
    """
    match=get_match(match_id)
    if not match:
        return False
    match.report=report
    match.report_is_confirmed=True
    match.journal.append(f"Match report has been modified and confirmed by {username}")
    match.save()
    return True

#COMPETITIONS_API

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