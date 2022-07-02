import mongoengine

class Match(mongoengine.Document):
    """
    Class defining a match.
    """
    competition_id=mongoengine.ObjectIdField(required=True)
    round=mongoengine.StringField(required=True)
    season=mongoengine.StringField(required=True)
    date_utc=mongoengine.DateTimeField(required=True)
    #label=mongoengine.StringField(required=True)
    home_team_id=mongoengine.ObjectIdField(required=True)
    away_team_id=mongoengine.ObjectIdField(required=True)
    additional_attributes=mongoengine.ListField()
    link=mongoengine.URLField(required=True)
    link_is_confirmed=mongoengine.BooleanField(default=False)
    username=mongoengine.StringField(required=True)
    report=mongoengine.FileField() #??
    report_is_confirmed=mongoengine.BooleanField(default=False)
    journal=mongoengine.ListField(default=["Match created!"])
    data=mongoengine.ListField()
    working=mongoengine.ListField()
    is_confirmed=mongoengine.BooleanField(default=False)
    is_completed=mongoengine.BooleanField(default=False)

    meta={
        'db_alias': 'core',
        'collection': 'matches'
    }