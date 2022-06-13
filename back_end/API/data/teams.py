import mongoengine

class Team(mongoengine.Document):
    """
    Class defining a team
    """
    team_name=mongoengine.StringField(required=True)
    is_confirmed=mongoengine.BooleanField(default=False)


    meta={
        'db_alias': 'core',
        'collection': 'teams'
    }