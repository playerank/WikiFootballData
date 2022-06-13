import mongoengine

class Requested_match(mongoengine.Document):
    """
    Class defining a requested match.
    """
    competition_name=mongoengine.StringField(required=True)
    season_name=mongoengine.StringField(required=True)
    home_team=mongoengine.StringField(required=True)
    away_team=mongoengine.StringField(required=True)
    
    meta={
        'db_alias': 'core',
        'collection': 'requested_matches'
    }