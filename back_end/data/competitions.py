import mongoengine

class Competition(mongoengine.Document):
    """
    Class defining a competition
    """
    competition_name=mongoengine.StringField(required=True)
    competition_code=mongoengine.StringField()
    is_confirmed=mongoengine.BooleanField(default=False)


    meta={
        'db_alias': 'core',
        'collection': 'competitions'
    }