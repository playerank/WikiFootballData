from typing import Any, Dict, List
import mongoengine

class Analysis(mongoengine.EmbeddedDocument):
    """
    Class defining an analysis
    """
    time_slot: str=mongoengine.StringField(required=True)
    detail: List[Dict[str,Any]]=mongoengine.ListField()
    working: str=mongoengine.StringField()
    author: str=mongoengine.StringField()
    endorsements: int=mongoengine.IntField(required=True)
    dislikes: int=mongoengine.IntField(required=True)

def init(time_slot: str) -> Analysis:
    a=Analysis()
    a.time_slot=time_slot
    a.detail=None
    a.working=None
    a.author=None
    a.endorsements=0
    a.dislikes=0
    return a