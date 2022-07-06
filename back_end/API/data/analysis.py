import mongoengine

class Analysis(mongoengine.EmbeddedDocument):
    """
    Class defining an analysis
    """
    time_slot=mongoengine.StringField(required=True)
    detail=mongoengine.FileField() ##??
    working=mongoengine.StringField(required=True)
    author=mongoengine.StringField(default=None)
    endorsements=mongoengine.IntField(default=0)
    dislikes=mongoengine.IntField(default=0)
