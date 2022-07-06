import mongoengine

class Final_data(mongoengine.EmbeddedDocument):
    """
    Class defining the final data
    """
    time_slot=mongoengine.StringField(required=True)
    detail=mongoengine.FileField(required=True) #??
    author=mongoengine.StringField(required=True)