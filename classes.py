from datetime import datetime
import json

class Track:
    def __init__(self, properties):
        self.tmx_id = int(properties["TrackId"])
        self.uid = int(properties["UId"])
        self.track_name = properties["TrackName"]
        self.author_time = int(properties["AuthorTime"])
        self.upload_date = datetime.strptime(properties["UploadedAt"], "%Y-%m-%dT%H:%M:%S")
        self.recs = {
            "TMX": [],
            "Dedi": []
        }

    
    def add_rec(self, record, lb):
        self.recs[lb].append(record)
    
    def sort_recs(self):
        for lb in self.recs.keys():
            self.recs[lb] = sorted(self.recs[lb], lambda x: x.time)

    def __str__(self):
        return json.dumps(
            {
                "TrackId": self.tmx_id,
                "UId": self.uid,
                "TrackName": self.track_name,
                "AuthorTime": self.author_time,
                "UploadedAt": datetime.strftime(self.upload_date, "%Y-%m-%d %H:%M:%S"),
                "Records": {lb: [str(rec) for rec in self.recs[lb]] for lb in self.recs.keys()}
            }
        )

class Record:
    def __init__(self, properties):
        self.player = Player(properties["Player"])
        self.time = int(properties["Time"])
        if "T" in properties["RecordDate"]:
            self.date = datetime.strptime(properties["RecordDate"], "%Y-%m-%dT%H:%M:%S")
        else:
            self.date = datetime.strptime(properties["RecordDate"], "%Y-%m-%d %H:%M:%S")
    
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

    def __str__(self):
        return json.dumps(
            {
                "Player": str(self.player),
                "Time": self.time,
                "RecordDate": datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S")
            }
        )

class Player:
    def __init__(self, properties):
        self.login = properties["Login"]
        self.nickname = properties["Nickname"]
        self.in_ml = properties["TeamML"]

    def count_wr(self):
        return self.in_ml
    
    def __str__(self):
        return json.dumps(
            {
                "Login": self.login,
                "Nickname": self.nickname,
                "TeamML": self.in_ml
            }
        )
    
