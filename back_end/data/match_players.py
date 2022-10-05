import mongoengine
from bson import ObjectId

class Match_Player(mongoengine.EmbeddedDocument):
    """
    Class defining a simple version of a player
    """
    player_id: ObjectId=mongoengine.ObjectIdField(required=True)
    player_name: str=mongoengine.StringField(required=True)
    shirt_number: int=mongoengine.IntField(required=True)

def create_player_info(p: Match_Player):
    d=dict()
    d={
        "shirt_number":p.shirt_number,
        "name":p.player_name,
        "goals":0,
        "own_goals":0,
        "played_minutes":0,
        "player_id":f"{p.player_id}",
        "red_cards":0,
        "yellow_card":0
    }
    return d