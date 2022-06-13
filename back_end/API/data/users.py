import mongoengine

class User(mongoengine.Document):
    """
    Class defining a User
    """
    username=mongoengine.StringField(required=True)
    password=mongoengine.StringField(required=True)
    is_online=mongoengine.BooleanField()
    is_editor=mongoengine.BooleanField(default=False)
    is_administrator=mongoengine.BooleanField(default=False)
    
    meta = {
        'db_alias': 'core',
        'collection':'users'
    }