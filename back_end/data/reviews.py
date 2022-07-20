import mongoengine
from bson import ObjectId

class Review(mongoengine.Document):
    match_id: ObjectId=mongoengine.ObjectIdField(required=True)
    data_index: int=mongoengine.IntField(required=True)
    username: str=mongoengine.StringField(required=True)
    type: str=mongoengine.StringField(required=True) #e(ndorsement) or d(islike)

    meta={
        'db_alias': 'core',
        'collection': 'reviews'
    }