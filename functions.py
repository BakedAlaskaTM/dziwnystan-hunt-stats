import csv
import json
from datetime import datetime
import classes

def write_csv(filename: str, info_list: list, fields: list):
    try:
        with open(filename, 'w', newline='', encoding="UTF-8") as csvfile:
            writer = csv.writer(csvfile, delimiter='@')
            writer.writerow([field for field in fields])
            for line_dict in info_list:
                writer.writerow([line_dict[field] for field in fields])    
    except:
        return False
    else:
        return True


def load_csv(filename: str):
    tracks = []
    try:
        with open(filename, "r", encoding="UTF-8") as csvfile:
            maps_file = csv.DictReader(csvfile, delimiter="@")
            for line in maps_file:
                tracks.append(line)
    except FileNotFoundError:
        print(f"FileNotFoundError: File '{filename}' does not exist.")
        return []
    else:
        return tracks

def write_json(filename: str, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def upload_track_data(filename: str, tracks: list):
    track_data = [str(track) for track in tracks]
    write_json(filename, track_data)
    return True

def read_json(filename):
    return json.load(filename)

def load_track_data(filename):
    raw_track_info = read_json(filename)
    tracks = []
    for track_data in raw_track_info:
        track = classes.Track(track_data)
        for lb, recs in track["Record"].items():
            for rec_data in recs:
                track.add_rec(classes.Record(rec_data), lb)
                
