from datetime import datetime as dt
import json

class Track:
    def __init__(self, properties):
        self.tmx_id = properties["TrackId"]
        self.uid = properties["UId"]
        self.track_name = properties["TrackName"]
        self.author_time = int(properties["AuthorTime"])
        if "T" in properties["UploadedAt"]:
            self.upload_date = dt.strptime(properties["UploadedAt"], "%Y-%m-%dT%H:%M:%S")
        else:
            self.upload_date = dt.strptime(properties["UploadedAt"], "%Y-%m-%d %H:%M:%S")
        self.recs = {
            "TMX": [],
            "Dedi": []
        }

    def add_rec(self, record, lb):
        self.recs[lb].append(record)
    
    def sort_recs(self):
        for lb in self.recs.keys():
            self.recs[lb] = sorted(self.recs[lb], lambda x: x.time)

    def properties(self):
        return {
            "TrackId": self.tmx_id,
            "UId": self.uid,
            "TrackName": self.track_name,
            "AuthorTime": self.author_time,
            "UploadedAt": dt.strftime(self.upload_date, "%Y-%m-%d %H:%M:%S"),
        }
    
    def get_uid(self):
        return self.uid

    def __str__(self):
        return json.dumps(
            {
                "TrackId": self.tmx_id,
                "UId": self.uid,
                "TrackName": self.track_name,
                "AuthorTime": self.author_time,
                "UploadedAt": dt.strftime(self.upload_date, "%Y-%m-%d %H:%M:%S"),
            }
        )

class Record:
    def __init__(self, properties):
        if "PlayerLogin" in properties.keys():
            self.player_login = properties["PlayerLogin"]
        else:
            self.player_login = None

        if "PlayerId" in properties.keys():
            self.player_id = properties["PlayerId"]
        else:
            self.player_id = None

        self.time = int(properties["Time"])
        if "T" in properties["RecordDate"]:
            self.date = dt.strptime(properties["RecordDate"], "%Y-%m-%dT%H:%M:%S")
        else:
            self.date = dt.strptime(properties["RecordDate"], "%Y-%m-%d %H:%M:%S")

    def __lt__(self, other):
        if not isinstance(other, Record):
            raise TypeError(f"TypeError: '<' not supported between instances of 'Record' and '{type(other)}'.")
        else:
            return self.time < other.time

    def __gt__(self, other):
        if not isinstance(other, Record):
            raise TypeError(f"TypeError: '>' not supported between instances of 'Record' and '{type(other)}'.")
        else:
            return self.time > other.time

    def __eq__(self, other):
        if not isinstance(other, Record):
            raise TypeError(f"TypeError: '==' not supported between instances of 'Record' and '{type(other)}'.")
        else:
            return self.time == other.time

    def properties(self):
        return {
            "PlayerLogin": self.player_login,
            "PlayerId": self.player_id,
            "Time": self.time,
            "RecordDate": dt.strftime(self.date, "%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return json.dumps(
            {
                "PlayerLogin": self.player_login,
                "PlayerId": self.player_id,
                "Time": self.time,
                "RecordDate": dt.strftime(self.date, "%Y-%m-%d %H:%M:%S")
            }
        )

class Player:
    def __init__(self, properties):
        if "Login" in properties.keys():
            self.login = properties["Login"]
        else:
            self.login = None

        if "Id" in properties.keys():
            self.id = properties["Id"]
        else:
            self.id = None
        
        if "Nickname" in properties.keys():
            self.nickname = properties["Nickname"]
        else:
            self.nickname = None

        if "TeamML" in properties.keys():
            self.in_ml = properties["TeamML"]
        else:
            self.in_ml = None

    def is_member(self):
        return self.in_ml
    
    def properties(self):
        return {
                "Login": self.login,
                "Id": self.id,
                "Nickname": self.nickname,
                "TeamML": self.in_ml
            }

    def __str__(self):
        return json.dumps(
            {
                "Login": self.login,
                "Id": self.id,
                "Nickname": self.nickname,
                "TeamML": self.in_ml
            }
        )
    
