from typing import List
import mongoengine

class Final_data(mongoengine.EmbeddedDocument):
    """
    Class defining the final data
    """
    time_slot: str=mongoengine.StringField(required=True)
    detail: List[str]=mongoengine.ListField(required=True)
    author: str=mongoengine.StringField(required=True)