import mongoengine

class User(mongoengine.Document):
    """
    Class defining a Usera
    """
    usename=mongoengine.StringField(required=True)
    password=mongoengine.StringField(required=True)
    is_online=mongoengine.BooleanField(required=True)
    is_editor=mongoengine.BooleanField(required=True)
    is_administrator=mongoengine.BooleanField(required=True)
    
    meta ={
        'db_alias': 'core',
        'collection':'users'
    }