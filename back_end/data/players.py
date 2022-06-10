import mongoengine

class Player(mongoengine.Document):
    """
    Class defining a player
    """
    player_name=mongoengine.StringField(required=True)
    is_confirmed=mongoengine.BooleanField(default=False)


    meta={
        'db_alias': 'core',
        'collection': 'players'
    }