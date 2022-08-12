import mongoengine
from bson import ObjectId

class Match_Player(mongoengine.EmbeddedDocument):
    """
    Class defining a simple version of a player
    """
    player_id: ObjectId=mongoengine.ObjectIdField(required=True)
    player_name: str=mongoengine.StringField(required=True)
    shirt_number: int=mongoengine.IntField(required=True)