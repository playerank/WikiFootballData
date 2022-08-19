import mongoengine
from bson import ObjectId

class Team(mongoengine.Document):
    """
    Class defining a team
    """
    team_name: str=mongoengine.StringField(required=True)
    competition_id: ObjectId=mongoengine.ObjectIdField(required=True)
    is_confirmed: bool=mongoengine.BooleanField(default=False)

    meta={
        'db_alias': 'core',
        'collection': 'teams'
    }