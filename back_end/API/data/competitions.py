import mongoengine

class Competition(mongoengine.Document):
    """
    Class defining a competition
    """
    competition_name: str=mongoengine.StringField(required=True)
    competition_code: str=mongoengine.StringField()
    is_confirmed: bool=mongoengine.BooleanField(default=False)


    meta={
        'db_alias': 'core',
        'collection': 'competitions'
    }