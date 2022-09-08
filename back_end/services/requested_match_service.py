from data.requested_matches import Requested_match
from typing import List


def get_requested_matches(n: int) -> List[Requested_match]:
    """
    Return the list of n requested matches
    """
    if n==0:
        r_matches:List[Requested_match]=list(Requested_match.objects().all())
    else:
        r_matches:List[Requested_match]=list(Requested_match.objects[:n])
    #debug
    # for r in r_matches:
    #     print("r_match {} - {}, {} {}".format(r.home_team,r.away_team,r.competition_name,r.season_name))
    return r_matches

def add_r_match(home_team: str,away_team: str,competition_name: str,season: str) -> bool:
    """
    Create and add to the db a requested_match.
    Return False if already exists a requested_match with the same values
    """
    existing_r_match: Requested_match=Requested_match.objects() \
        .filter(home_team=home_team) \
        .filter(away_team=away_team) \
        .filter(competition_name=competition_name) \
        .filter(season_name=season) \
        .first()
    if existing_r_match:
        #debug
        # print("Match esistente {} - {}, {} {}".format(existing_r_match.home_team,existing_r_match.away_team,existing_r_match.competition_name,existing_r_match.season_name))
        return False
    r_match=Requested_match()
    r_match.home_team=home_team
    r_match.away_team=away_team
    r_match.competition_name=competition_name
    r_match.season_name=season
    r_match.save()
    return True

def remove_r_match(home_team: str,away_team: str,competition_name: str,season: str) -> bool:
    """
    Remove from the db the requested match.
    Return False if doesn't exist a requested match with the same values
    """
    existing_r_match: Requested_match=Requested_match.objects() \
        .filter(home_team=home_team) \
        .filter(away_team=away_team) \
        .filter(competition_name=competition_name) \
        .filter(season_name=season) \
        .first()
    if not existing_r_match:
        return False
    existing_r_match.delete()
    return True