import mongoengine

class Event(mongoengine.Document):
    """
    Class defining a list of data
    """
    match_id=mongoengine.ObjectIdField(required=True)
    data=mongoengine.ListField(required=True)

    meta={
        'db_alias': 'core',
        'collection': 'events'
    }