import mongoengine

class User(mongoengine.Document):
    usename=mongoengine.StringField(required=True)
    password=mongoengine.StringField(required=True)
    role=mongoengine.StringField(required=True)
    #da aggiornare
    meta ={
        'db_alias': 'core',
        'collection':'users'
    }