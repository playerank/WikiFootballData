import mongoengine

def global_init():
    mongoengine.register_connection(alias='core', name='wiki_football_db')