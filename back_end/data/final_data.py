import mongoengine

class Final_data(mongoengine.EmbeddedDocument):
    """
    Class defining the final data
    """
    time_slot: str=mongoengine.StringField(required=True)
    detail=mongoengine.StringField(required=True) #vedi detail in analysis
    author: str=mongoengine.StringField(required=True)