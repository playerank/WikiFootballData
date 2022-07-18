import mongoengine

class Team(mongoengine.Document):
    """
    Class defining a team
    """
    team_name: str=mongoengine.StringField(required=True)
    is_confirmed: bool=mongoengine.BooleanField(default=False)


    meta={
        'db_alias': 'core',
        'collection': 'teams'
    }