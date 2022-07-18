import mongoengine

class Requested_match(mongoengine.Document):
    """
    Class defining a requested match.
    """
    competition_name: str=mongoengine.StringField(required=True)
    season_name: str=mongoengine.StringField(required=True)
    home_team: str=mongoengine.StringField(required=True)
    away_team: str=mongoengine.StringField(required=True)
    
    meta={
        'db_alias': 'core',
        'collection': 'requested_matches'
    }