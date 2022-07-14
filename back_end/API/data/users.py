import mongoengine

class User(mongoengine.Document):
    """
    Class defining a User
    """
    username: str=mongoengine.StringField(required=True)
    password=mongoengine.StringField(required=True)
    is_online: bool=mongoengine.BooleanField()
    is_editor: bool=mongoengine.BooleanField(default=False)
    is_administrator: bool=mongoengine.BooleanField(default=False)
    
    meta = {
        'db_alias': 'core',
        'collection':'users'
    }