from datetime import datetime
from typing import List
from bson import ObjectId
from pydantic import HttpUrl
from data.matches import Match, Analysis, create_info_dict
from data.events import Event
from data.rules import n
from data.reviews import Review
from services.competition_service import get_competition_id, get_competition_by_id
from services.team_service import get_team_id, get_team_by_id
from services.player_service import get_player_id
from services.manager_service import get_manager_id, get_manager_by_id

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

def get_match_info(match_id: ObjectId):
    """
    Return the info of the match identified by match_id
    """
    m=get_match(match_id)
    if not m:
        return None
    info=dict()
    info={
        "Competition":get_competition_by_id(m.competition_id),
        "Home Team":get_team_by_id(m.home_team_id),
        "Away Team":get_team_by_id(m.away_team_id),
        "Season":m.season,
        "Round":m.round,
        "Date":m.date_utc
    }
    if m.penalty:
        info.update({"End":"Penalties"})
    elif m.extended_time:
        info.update({"End":"120th minute"})
    else:
        info.update({"End":"90th minute"})
    if m.is_confirmed:
        info.update({"Match Name":"Confirmed"})
    else:
        info.update({"Match Name":"Not confirmed"})
    info.update({
        "Officials":m.officials,
        "Home Manager":get_manager_by_id(m.home_manager_id),
        "Away Manager":get_manager_by_id(m.away_manager_id)
    })
    if m.officials_and_managers_are_confirmed:
        info.update({"Officials and Managers":"Confirmed"})
    else:
        info.update({"Officials and Managers":"Not confirmed"})
    info.update({"Home Team Formation":m.home_team_formation})
    if m.home_formation_is_confirmed:
        info.update({"Home Team": "Confirmed"})
    else:
        info.update({"Home Team": "Not confirmed"})
    info.update({"Away Team":m.away_team_formation})
    if m.away_formation_is_confirmed:
        info.update({"Away Team": "Confirmed"})
    else:
        info.update({"Away Team": "Not confirmed"})
    info.update({"Link":m.link})
    if m.link_is_confirmed:
        info.update({"Link":"Confirmed"})
    else:
        info.update({"Link":"Not confirmed"})
    info.update({"Report":m.report})
    if m.report_is_confirmed:
        info.update({"Report":"Confirmed"})
    else:
        info.update({"Report":"Not confirmed"})
    if m.is_completed:
        info.update({"Match analisys":"Completed"})
    else:
        info.update({"Match analysis":"Not completed"})
    return info

def add_managers(match_id: ObjectId, home_team_manager: str, away_team_manager: str):
    """
    Add the managers to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if values are already confirmed, 3 if managers already added, 4 if home_team_manager is incorrect, 5 if away_team_manager is incorrect
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.officials_and_managers_are_confirmed:
        return 2
    if match.home_manager_id or match.away_manager_id:
        return 3
    home_manager_id=get_manager_id(home_team_manager)
    if not home_manager_id:
        return 4
    away_manager_id=get_manager_id(away_team_manager)
    if not away_manager_id:
        return 5
    match.home_manager_id=home_manager_id
    match.away_manager_id=away_manager_id
    match.journal.append(f"Managers added or changed to {home_team_manager} and {away_team_manager}")
    match.save()
    return 0

def add_officials(match_id: ObjectId, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str):
    """
    Add the officials to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if values are already confirmed and 3 if values already added
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.officials_and_managers_are_confirmed:
        return 2
    if match.officials:
        return 3
    match.officials=list()
    match.officials.append(arbitrator)
    match.officials.append(linesman1)
    match.officials.append(linesman2)
    match.officials.append(fourth_man)
    match.journal.append(f"Officials added: {arbitrator}, {linesman1}, {linesman2} and {fourth_man}")
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

def change_off_and_man(check: bool, match_id: ObjectId, username: str, home_team_manager: str, away_team_manager: str, arbitrator: str, linesman1: str, linesman2: str, fourth_man: str):
    """
    Change or modify the officials and managers of the match identified by match_id.
    Return 1 if match doesn't exist, 2 if values already confirmed, 3 if home_team_manager is incorrect, 4 if away_team_manager is incorrect
    """
    match=get_match(match_id)
    if not match:
        return 1
    if check and match.officials_and_managers_are_confirmed:
        return 2
    if home_team_manager!=" ":
        home_manager_id=get_manager_id(home_team_manager)
        if not home_manager_id:
            return 3
        match.home_manager_id=home_manager_id
    if away_team_manager!=" ":
        away_manager_id=get_manager_id(away_team_manager)
        if not away_manager_id:
            return 4
        match.away_manager_id=away_manager_id
    if arbitrator!=" ":
        match.officials[0]=arbitrator
    if linesman1!=" ":
        match.officials[1]=linesman1
    if linesman2!=" ":
        match.officials[2]=linesman2
    if fourth_man!=" ":
        match.officials[3]=fourth_man
    if check:
        match.journal.append("Officials and managers updated")
    else:
        match.officials_and_managers_are_confirmed=True
        match.journal.append(f"Officials and managers updated and confirmed by {username}")
    match.save()
    return 0

def add_team_formation(match_id: ObjectId, home: bool, player_names: List[str], player_numbers: List[int]):
    """
    Add the requested formation to the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the requested formation is confirmed, 3 if formation already added, player_name if player_name is incorrect
    """
    match=get_match(match_id)
    if not match:
        return 1
    if home:
        if match.home_formation_is_confirmed:
            return 2
        if match.home_team_formation:
            return 3
    else:
        if match.away_formation_is_confirmed:
            return 2
        if match.away_team_formation:
            return 3
    i=0
    for p in player_names:
        player_id=get_player_id(p)
        if not player_id:
            return p
        match.team_append(home,player_id,p,player_numbers[i])
        i+=1
    
    if home:
        match.journal.append("Home team formation added")
    else:
        match.journal.append("Away team formation added")
    match.save()
    return 0

def assess_formation(match_id: ObjectId, home: bool, username: str):
    """
    Confirm definetely the requested formation of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the requested formation is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if home:
        if match.home_formation_is_confirmed:
            return 2
        match.home_formation_is_confirmed=True
        match.journal.append(f"Home formation confirmed by {username}")
    else:
        if match.away_formation_is_confirmed:
            return 2
        match.away_formation_is_confirmed=True
        match.journal.append(f"Away formation confirmed by {username}")
    match.save()
    return 0

def change_formation(check: bool, match_id: ObjectId, home: bool, username: str, player_names: List[str], player_numbers: List[int]):
    """
    Change or modify the requested formation of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the formation didn't exist, 3 if formation already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if home:
        if not match.home_team_formation:
            return 2
        if check and match.home_formation_is_confirmed:
            return 3
    else:
        if not match.away_team_formation:
            return 2
        if check and match.away_formation_is_confirmed:
            return 3
    i=0
    for p in player_names:
        if p=="":
            if player_numbers[i]>0:#User wants to modify tha number but not the name 
                if home:
                    match.home_team_formation[i].shirt_number=player_numbers[i]
                else:
                    match.away_team_formation[i].shirt_number=player_numbers[i]
        else:#User wants to modify the name
            player_id=get_player_id(p)
            if not player_id:#Mistake, skip entirely(name and number) this modification
                i+=1
                continue
            if home:
                match.home_team_formation[i].player_name=p
                match.home_team_formation[i].player_id=player_id
                if player_numbers[i]>0:#User wants to modify even the number
                    match.home_team_formation[i].shirt_number=player_numbers[i]
            else:
                match.away_team_formation[i].player_name=p
                match.away_team_formation[i].player_id=player_id
                if player_numbers[i]>0:#User wants to modify even the number
                    match.away_team_formation[i].shirt_number=player_numbers[i]
        i+=1
    #outside the for
    if home:
        if check:
            match.journal.append("Home team formation updated")
        else:
            match.home_formation_is_confirmed=True
            match.journal.append(f"Home team formation updated and confirmed by {username}")
    else:
        if check:
            match.journal.append("Away team formation updated")
        else:
            match.away_formation_is_confirmed=True
            match.journal.append(f"Away team formation updated and confirmed by {username}")
    match.save()
    return 0

def change_name(check: bool, username: str, match_id, home_team: str, away_team: str, season: str, competition_name: str, round: str, date: datetime, link: HttpUrl, extended_time: bool, penalty: bool):
    """
    Change or modify the match name(depends of the value of check).
    Return 1 if the match doesn't exist, 2 if the match_name is already confirmed
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
        match.journal.append(f"Match name updated and confirmed definitely by {username}")
    match.save()
    return 0

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

def change_link(check: bool, username: str, match_id: ObjectId, new_link: HttpUrl):
    """
    Change the link of the match identified by match_id, if check==False confirm it definetely.
    Return 1 if the match doesn't exist, 2 if the match link is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if check and match.link_is_confirmed:
        return 2
    match.link=new_link
    if check:
        match.journal.append(f"Match link updated to {new_link}")
    else:
        match.link_is_confirmed=True
        match.journal.append(f"Match link modified and confirmed by {username}")
    match.save()
    return 0

def assess_link(username: str, match_id: ObjectId):
    """
    Confirm definitely the link of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the match link is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if match.link_is_confirmed:
        return 2
    match.link_is_confirmed=True
    match.journal.append(f"Match link confirmed by {username}")
    match.save()
    return 0

def get_match_report(match_id: ObjectId):
    """
    Return the report of the match identified by match_id
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

def change_match_report(check: bool, username: str, match_id: ObjectId, new_report: str):
    """
    Change the report of the match identified by match_id.
    Return 1 if the match doesn't exist, 2 if the match report is already confirmed
    """
    match=get_match(match_id)
    if not match:
        return 1
    if check and match.report_is_confirmed:
        return 2
    match.report=new_report
    if check:
        match.journal.append("Match report updated")
    else:
        match.report_is_confirmed=True
        match.journal.append(f"Match report modified and confirmed by {username}")
    match.save()
    return 0

def assess_match_report(username: str, match_id: ObjectId):
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
    Return the list of the link and the time slot not analyzed yet or that aren't being analyzed by some user.
    Return 1 if the match doesn't exist, 2 if the match is already completed, 3 if the match name is not confirmed
    4 if the link is not confirmed, 5 if the officials and managers are not confirmed,
    6 and 7 if formations are not confirmed
    """
    match:Match=Match.objects(id=match_id).only('link','data').first()
    if not match:
        return 1
    if match.is_completed:
        return 2
    if not match.is_confirmed:
        return 3
    if not match.link_is_confirmed:
        return 4
    if not match.officials_and_managers_are_confirmed:
        return 5
    if not match.home_formation_is_confirmed:
        return 6
    if not match.away_formation_is_confirmed:
        return 7
    free_time_slot: List[str]=list()
    free_time_slot.append(match.link)
    for d in match.data:
        if not d.working and not d.author:
            free_time_slot.append(d.time_slot)
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
    return create_info_dict(match)

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

def get_data(match_id: ObjectId, n: int) -> List[Analysis] | None:
    """
    Return a list of n data of the match identified by match_id
    """
    match: Match=Match.objects(id=match_id).only('data').first()
    if not match:
        return None
    if n==0 or n>=30:
        return match.data
    data_list=list()
    for d in match.data:
        if n==0: break
        data_list.append(d)
        n-=1
    return data_list

def get_elaborated_data(match_id: ObjectId, n: int) -> List[Analysis] | None:
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