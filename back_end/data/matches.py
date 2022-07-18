import mongoengine
from pydantic import HttpUrl
from data.analysis import Analysis,init
from typing import List
from bson import ObjectId
from datetime import datetime

class Match(mongoengine.Document):
    """
    Class defining a match.
    """
    competition_id: ObjectId=mongoengine.ObjectIdField(required=True)
    home_team_id: ObjectId=mongoengine.ObjectIdField(required=True)
    away_team_id: ObjectId=mongoengine.ObjectIdField(required=True)
    season: str=mongoengine.StringField(required=True)
    round: str=mongoengine.StringField(required=True)
    date_utc: datetime=mongoengine.DateTimeField(required=True)
    username: str=mongoengine.StringField(required=True)
    #label=mongoengine.StringField(required=True)
    extended_time: bool=mongoengine.BooleanField(required=True)
    penalty: bool=mongoengine.BooleanField(required=True)
    is_confirmed: bool=mongoengine.BooleanField(default=False)
    additional_attributes: List=mongoengine.ListField()
    working: List[str]=mongoengine.ListField()
    link: HttpUrl=mongoengine.URLField(required=True)
    link_is_confirmed: bool=mongoengine.BooleanField(default=False)
    report=mongoengine.StringField()
    report_is_confirmed: bool=mongoengine.BooleanField(default=False)
    journal: List[str]=mongoengine.ListField(default=["Match created!"])
    data: List[Analysis]=mongoengine.EmbeddedDocumentListField(Analysis)
    is_completed: bool=mongoengine.BooleanField(default=False)

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
        self.data.append(init("e_t_2")) #index 19
        if self.extended_time:
            self.data.append(init("91-95")) #index 20
            self.data.append(init("96-100"))
            self.data.append(init("101-105"))
            self.data.append(init("e_t_3"))
            self.data.append(init("106-110"))
            self.data.append(init("111-115"))
            self.data.append(init("116-120"))
            self.data.append(init("e_t_4")) #index 27
        if self.penalty:
            self.data.append("penalty") #index 28
    
    @property
    def change_data(self):
        l=len(self.data)
        #ELIMINO
        if l==29: #termina con penalty
            if not self.penalty:
                self.data.pop() #ora termina con e_t_4
            if not self.extended_time:
                for x in range(8):
                    self.data.pop() #ora termina con e_t_2
        #ELIMINO E FORSE AGGIUNGO
        elif l==28: #termina con e_t_4
            if not self.extended_time:
                for x in range(8):
                    self.data.pop()
            if self.penalty:
                self.data.append("penalty")
        elif l==21: #pochissime le partite terminate ai rigori senza supplementari però esistono Community Shield, replay di partite di carabao cup etc
            if not self.penalty:
                self.data.pop() #ora termina con e_t_2
            if self.extended_time:
                self.data.append(init("91-95"))
                self.data.append(init("96-100"))
                self.data.append(init("101-105"))
                self.data.append(init("e_t_3"))
                self.data.append(init("106-110"))
                self.data.append(init("111-115"))
                self.data.append(init("116-120"))
                self.data.append(init("e_t_4"))
        #AGGIUNGO
        elif l==20:
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
        """
        Check if all data are completed
        """
        for d in self.data: 
            if d.author=="":
                return False
        return True

#time_slot vanno da 1-5 a rigori
#1-5, 6-10, 11-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, recupero1, 46-50 -> 86-90, recupero2, 91-95 -> 101-105, recupero3, 106-110 -> 116-120, recupero4, rigori
#sono 29