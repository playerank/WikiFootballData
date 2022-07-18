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

    # @property
    # def init(self,time_slot: str):
    #     """
    #     Initializes an empy object analysis
    #     """
    #     self.time_slot=time_slot
    #     self.detail=None
    #     self.working=""
    #     self.author=""
    #     self.endorsements=0
    #     self.dislikes=0

def init(time_slot: str) -> Analysis:
    a=Analysis()
    a.time_slot=time_slot
    a.detail=None
    a.working=""
    a.author=""
    a.endorsements=0
    a.dislikes=0
    return a