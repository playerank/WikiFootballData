import mongoengine
from pydantic import HttpUrl
from typing import List
from bson import ObjectId
from datetime import datetime
from data.analysis import Analysis,init
from data.match_players import Match_Player,create_player_info

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
    officials: List[str]=mongoengine.ListField()
    home_manager_id: ObjectId=mongoengine.ObjectIdField()
    away_manager_id: ObjectId=mongoengine.ObjectIdField()
    officials_and_managers_are_confirmed=mongoengine.BooleanField(default=False)
    home_team_formation: List[Match_Player]=mongoengine.EmbeddedDocumentListField(Match_Player)
    away_team_formation: List[Match_Player]=mongoengine.EmbeddedDocumentListField(Match_Player)
    formations_are_confirmed: bool=mongoengine.BooleanField(default=False)
    additional_attributes: List=mongoengine.ListField()
    working: List[str]=mongoengine.ListField()
    link: HttpUrl=mongoengine.URLField(required=True)
    link_is_confirmed: bool=mongoengine.BooleanField(default=False)
    report: str=mongoengine.StringField()
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
        #DELETE
        if l==29: #ends with penalty
            if not self.penalty:
                self.data.pop() #now ends with e_t_4
            if not self.extended_time:
                for x in range(8):
                    self.data.pop() #now ends with e_t_2
        #DELETE AND MAYBE ADD
        elif l==28: #ends with e_t_4
            if not self.extended_time:
                for x in range(8):
                    self.data.pop()
            if self.penalty:
                self.data.append("penalty")
        elif l==21: #pochissime le partite terminate ai rigori senza supplementari però esistono Community Shield, replay di partite di carabao cup etc
            if not self.penalty:
                self.data.pop() #now ends with e_t_2
            if self.extended_time:
                self.data.append(init("91-95"))
                self.data.append(init("96-100"))
                self.data.append(init("101-105"))
                self.data.append(init("e_t_3"))
                self.data.append(init("106-110"))
                self.data.append(init("111-115"))
                self.data.append(init("116-120"))
                self.data.append(init("e_t_4"))
        #ADD
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
            if not d.author:
                return False
        return True
    
    @property
    def team_append(self, home: bool, player_id: ObjectId, player_name: str, shirt_number: int):
        """
        Append to the indicated formation the Match_Player object with the right parameters
        """
        p=Match_Player()
        p.player_id=player_id
        p.player_name=player_name
        p.shirt_number=shirt_number
        if home:
            self.home_team_formation.append(p)
        else:
            self.away_team_formation.append(p)

#time_slot vanno da 1-5 a rigori
#1-5, 6-10, 11-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, recupero1, 46-50 -> 86-90, recupero2, 91-95 -> 101-105, recupero3, 106-110 -> 116-120, recupero4, rigori
#sono 29

def create_info_dict(m: Match):
    """
    Return a dict with all the information required by soccerLogger, in the right format
    """
    d=dict()
    d={
        "addictional attirbutes":m.additional_attributes,
        "competition_id":m.competition_id,
        "date_utc":m.date_utc,
        "match_id":m.id,
        "round":m.round,
        "season":m.season,
        "match official":{
            "arbitrator":m.officials[0],
            "linesman1":m.officials[1],
            "linesman2":m.officials[2],
            "fourth_man":m.officials[3]
        },
        "home_team":{
            "team_id":m.home_team_id,
            "coach_id":m.home_manager_id,
            "score":0,
            "formation":{
                "bench":[
                    create_player_info(m.home_team_formation[12]),
                    create_player_info(m.home_team_formation[13]),
                    create_player_info(m.home_team_formation[14]),
                    create_player_info(m.home_team_formation[15]),
                    create_player_info(m.home_team_formation[16]),
                    create_player_info(m.home_team_formation[17]),
                    create_player_info(m.home_team_formation[18]),
                    create_player_info(m.home_team_formation[19]),
                    create_player_info(m.home_team_formation[20]),
                    create_player_info(m.home_team_formation[21]),
                    create_player_info(m.home_team_formation[22]),
                    create_player_info(m.home_team_formation[23])
                ],
                "lineup":[
                    create_player_info(m.home_team_formation[0]),
                    create_player_info(m.home_team_formation[1]),
                    create_player_info(m.home_team_formation[2]),
                    create_player_info(m.home_team_formation[3]),
                    create_player_info(m.home_team_formation[4]),
                    create_player_info(m.home_team_formation[5]),
                    create_player_info(m.home_team_formation[6]),
                    create_player_info(m.home_team_formation[7]),
                    create_player_info(m.home_team_formation[8]),
                    create_player_info(m.home_team_formation[9]),
                    create_player_info(m.home_team_formation[10]),
                ]
            }
        },
        "away_team_formation":{
            "team_id":m.away_team_formation,
            "coach_id":m.away_manager_id,
            "score":0,
            "formation":{
                "bench":[
                    create_player_info(m.away_team_formation[12]),
                    create_player_info(m.away_team_formation[13]),
                    create_player_info(m.away_team_formation[14]),
                    create_player_info(m.away_team_formation[15]),
                    create_player_info(m.away_team_formation[16]),
                    create_player_info(m.away_team_formation[17]),
                    create_player_info(m.away_team_formation[18]),
                    create_player_info(m.away_team_formation[19]),
                    create_player_info(m.away_team_formation[20]),
                    create_player_info(m.away_team_formation[21]),
                    create_player_info(m.away_team_formation[22]),
                    create_player_info(m.away_team_formation[23])
                ],
                "lineup":[
                    create_player_info(m.away_team_formation[0]),
                    create_player_info(m.away_team_formation[1]),
                    create_player_info(m.away_team_formation[2]),
                    create_player_info(m.away_team_formation[3]),
                    create_player_info(m.away_team_formation[4]),
                    create_player_info(m.away_team_formation[5]),
                    create_player_info(m.away_team_formation[6]),
                    create_player_info(m.away_team_formation[7]),
                    create_player_info(m.away_team_formation[8]),
                    create_player_info(m.away_team_formation[9]),
                    create_player_info(m.away_team_formation[10]),
                ]
            }
        }
    }
    return d