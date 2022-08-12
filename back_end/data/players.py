import mongoengine
from bson import ObjectId
from datetime import datetime

class Player(mongoengine.Document):
    """
    Class defining a player
    """
    #Values (change rarely)
    player_name: str=mongoengine.StringField(required=True)
    date_of_birth: datetime=mongoengine.DateTimeField(required=True)
    national_team_id: ObjectId=mongoengine.ObjectIdField(required=True)
    is_confirmed: bool=mongoengine.BooleanField(default=False) #confirm values
    #Conditions (change very often)
    team_id: ObjectId=mongoengine.ObjectIdField(required=True)
    club_shirt_number: int=mongoengine.IntField(required=True)
    national_team_shirt_number: int=mongoengine.IntField(default=-1)

    meta={
        'db_alias': 'core',
        'collection': 'players'
    }