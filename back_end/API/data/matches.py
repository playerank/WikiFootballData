import mongoengine
from data.analysis import Analysis,init
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
    extended_time=mongoengine.BooleanField(required=True)
    penalty=mongoengine.BooleanField(required=True)
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
    def create_data(self):
        """
        Creates the empty list of analysis
        """
        self.data: List[Analysis]=list()
        self.data.append(init("1-5"))
        self.data.append(init("6-10"))
        self.data.append(init("11-15"))
        self.data.append(init("16-20"))
        self.data.append(init("21-25"))
        self.data.append(init("26-30"))
        self.data.append(init("31-35"))
        self.data.append(init("36-40"))
        self.data.append(init("41-45"))
        self.data.append(init("e_t_1"))
        self.data.append(init("45-50"))
        self.data.append(init("51-55"))
        self.data.append(init("56-60"))
        self.data.append(init("61-65"))
        self.data.append(init("66-70"))
        self.data.append(init("71-75"))
        self.data.append(init("76-80"))
        self.data.append(init("81-85"))
        self.data.append(init("86-90"))
        self.data.append(init("e_t_2"))
        if self.extended_time:
            self.data.append(init("91-95"))
            self.data.append(init("96-100"))
            self.data.append(init("101-105"))
            self.data.append(init("e_t_3"))
            self.data.append(init("106-110"))
            self.data.append(init("111-115"))
            self.data.append(init("116-120"))
            self.data.append(init("e_t_4"))
        if self.penalty:
            self.data.append("penalty")
            

    @property
    def check_data(self) -> bool:
        """"
        Check if all data are completed
        """
        for d in self.data: 
            if d.author=="":
                return False
        return True

#time_slot vanno da 1-5 a rigori
#1-5, 6-10, 11-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, recupero1, 46-50 -> 86-90, recupero2, 91-95 -> 101-105, recupero3, 106-110 -> 116-120, recupero4, rigori
#sono 26