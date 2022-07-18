import mongoengine

class Analysis(mongoengine.EmbeddedDocument):
    """
    Class defining an analysis
    """
    time_slot: str=mongoengine.StringField(required=True)
    detail=mongoengine.StringField() ##FileField?? DictField o ListField probabilmente, event pysoccer
    working: str=mongoengine.StringField(required=True)
    author: str=mongoengine.StringField(required=True)
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