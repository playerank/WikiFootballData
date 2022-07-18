import mongoengine
from data.final_data import Final_data
from typing import List
from bson import ObjectId

class Event(mongoengine.Document):
    """
    Class defining a list of analysis
    """
    match_id: ObjectId=mongoengine.ObjectIdField(required=True)
    data_list: List[Final_data]=mongoengine.EmbeddedDocumentListField(Final_data)

    meta={
        'db_alias': 'core',
        'collection': 'events'
    }