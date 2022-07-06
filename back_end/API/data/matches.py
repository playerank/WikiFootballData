import mongoengine
from data.analysis import Analysis
from typing import List

class Match(mongoengine.Document):
    """
    Class defining a match.
    """
    competition_id=mongoengine.ObjectIdField(required=True)
    round=mongoengine.StringField(required=True)
    season=mongoengine.StringField(required=True)
    date_utc=mongoengine.DateTimeField(required=True)
    #label=mongoengine.StringField(required=True)
    home_team_id=mongoengine.ObjectIdField(required=True)
    away_team_id=mongoengine.ObjectIdField(required=True)
    additional_attributes=mongoengine.ListField()
    link=mongoengine.URLField(required=True)
    link_is_confirmed=mongoengine.BooleanField(default=False)
    username=mongoengine.StringField(required=True)
    report=mongoengine.StringField() #FileFiled??
    report_is_confirmed=mongoengine.BooleanField(default=False)
    journal: List[str]=mongoengine.ListField(default=["Match created!"])
    data: List[Analysis]=mongoengine.EmbeddedDocumentListField(Analysis)
    working=mongoengine.ListField()
    is_confirmed=mongoengine.BooleanField(default=False)
    is_completed=mongoengine.BooleanField(default=False)

    meta={
        'db_alias': 'core',
        'collection': 'matches'
    }

    @property
    def check_data(self) -> bool:
        """"
        Check if all data are completed
        """
        for x in range(20): #senza supplementare, 25 coi supplementari
            if not self.data[x]:
                return False
            if not self.data[x].author:
                return False
        return True

#time_slot vanno da 1-5 a rigori
#1-5, 6-10, 11-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, recupero1, 46-50 -> 86-90, recupero2, 91-95 -> 101-105, recupero3, 106-110 -> 116-120, recupero4, rigori
#sono 26