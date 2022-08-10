import mongoengine
from bson import ObjectId

class Player(mongoengine.Document):
    """
    Class defining a player
    """
    player_name: str=mongoengine.StringField(required=True)
    nationality: str=mongoengine.StringField(required=True)
    current_team: ObjectId=mongoengine.ObjectIdField(required=True)
    club_shirt_number: int=mongoengine.IntField(required=True)
    national_team_shirt_number: int=mongoengine.IntField(default=-1)
    is_confirmed: bool=mongoengine.BooleanField(default=False)

    meta={
        'db_alias': 'core',
        'collection': 'players'
    }