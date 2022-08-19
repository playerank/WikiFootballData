import mongoengine
from bson import ObjectId
from datetime import datetime

class Manager(mongoengine.Document):
    """
    Class defining a manager
    """
    #Values (change rarely)
    name: str=mongoengine.StringField(required=True)
    date_of_birth: datetime=mongoengine.DateTimeField(required=True)
    nationality: str=mongoengine.StringField(required=True)
    is_confirmed: bool=mongoengine.BooleanField(default=False) #confirm values
    #
    team_id: ObjectId=mongoengine.ObjectIdField(required=True)

    meta={
        'db_alias': 'core',
        'collection': 'manager'
    }