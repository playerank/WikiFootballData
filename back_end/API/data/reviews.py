import mongoengine
from typing import List
from bson import ObjectId

class Review(mongoengine.Document):
    match_id: ObjectId=mongoengine.ObjectIdField(required=True)
    data_index: int=mongoengine.IntField(required=True)
    endorsed: List[str]=mongoengine.ListField()
    disliked: List[str]=mongoengine.ListField()