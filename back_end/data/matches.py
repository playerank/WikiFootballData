import mongoengine

class Match(mongoengine.Document):
    """
    Class defining a match.
    """
    competition_id=mongoengine.IntField(required=True)
    round_id=mongoengine.IntField(required=True)
    season_id=mongoengine.IntField(required=True)
    date_utc=mongoengine.DateTimeField(required=True)#o int
    match_id=mongoengine.IntField(required=True)
    label=mongoengine.StringField(required=True)
    #home_team: Team
    #away_team: Team
    additional_attributes=mongoengine.ListField()
    #da aggiornare

    meta={
        'db_alias': 'core',
        'collection': 'matches'
    }
