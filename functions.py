import csv
import json
import requests
import re
from datetime import datetime as dt
import datetime as dtm
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import classes
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

FIELDS = ["TrackId", "TrackName", "UId", "AuthorTime", "UploadedAt"]
DATA_FILE_PATH = "Data/"
WEBSITE_FILE_PATH = "D:/Devin stuff/Python Stuff/Website/data/"
REGEX_STRING = '[$][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]|[$][a-zA-Z]'

def read_txt(filename: str):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print(f"FileNotFoundError: File '{filename}' does not exist.")
        return []
    else:
        contents = file.read().split("\n")
        file.close()
        return contents


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
        json.dump(data, json_file, indent=4, ensure_ascii=True)

def upload_track_data(filename: str, tracks: dict):
    track_data = {track_id: track.properties() for track_id, track in tracks.items()}
    write_json(filename, track_data)
    return True

def read_json(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print(f"FileNotFoundError: File '{filename}' does not exist.")
        return None
    else:
        file_str = file.read()
        file.close()
    return json.loads(file_str)

def load_track_data(track_file):
    raw_track_info = read_json(track_file)
    tracks = {}
    for track_id, track_data in raw_track_info.items():
        tracks[track_id] = classes.Track(track_data)
    return tracks

def time_converter(time_str):
    split_time = time_str.split(":")
    length = len(split_time)
    time_seconds = 0
    for i in range(length):
        time_seconds += float(split_time[(length-1)-i]) * (60**i)
    return time_seconds

def update_buffer_file(data: dict, progress: int|list, data_for: str):
    filename = f"{DATA_FILE_PATH}data_buffer.json"
    buffer_dict = read_json(filename)
    if buffer_dict is None:
        buffer_dict = {}
    if data_for == "players":
        if type(progress) == int:
            print("Error: progress must be a list for players data.")
            return
        buffer_dict[data_for] = {
            "Date": dt.now(dtm.UTC).timestamp(),
            "UpdatedLogins": progress,
            "Data": data[data_for]
        }
    else:
        if type(progress) == list:
            print("Error: item_num must be an int for records data.")
            return
        buffer_dict[data_for] = {
            "Date": dt.now(dtm.UTC).timestamp(),
            "ItemNum": progress,
            "Data": data[data_for]
        }
    write_json(filename, buffer_dict)

def read_buffer_file(data_for: str):
    filename = f"{DATA_FILE_PATH}data_buffer.json"
    buffer_dict = read_json(filename)
    if data_for == "players":
        if buffer_dict is None or data_for not in buffer_dict:
            return [None, [], None]
        return [dt.fromtimestamp(buffer_dict[data_for]["Date"], dtm.UTC), buffer_dict["UpdatedLogins"], buffer_dict[data_for]["Data"]]
    
    if buffer_dict is None or data_for not in buffer_dict:
        return [None, 0, None]
    return [dt.fromtimestamp(buffer_dict[data_for]["Date"], dtm.UTC), buffer_dict[data_for]["ItemNum"], buffer_dict[data_for]["Data"]]

def clear_buffer_file(data_for: list|str):
    filename = f"{DATA_FILE_PATH}data_buffer.json"
    buffer_dict = read_json(filename)
    if buffer_dict is None:
        buffer_dict = {}
    if type(data_for) == str:
        data_for = [data_for]
    for data_key in data_for:
        if data_key in buffer_dict:
            del buffer_dict[data_key]
    write_json(filename, buffer_dict)

# Consolidation Functions
def tracks_to_json():
    tracks = load_csv(f"{DATA_FILE_PATH}Maps.csv")
    tracks_dict = {row[FIELDS[0]]: classes.Track(row) for row in tracks}
    upload_track_data(f"{DATA_FILE_PATH}tracks.json", tracks_dict)

# Setup Functions
def get_tracks_from_author(author_id: int):
    more = True
    all_tracks = []

    while more:
        if not all_tracks:
            response = requests.get(f"https://tmnf.exchange/api/tracks?order1=1&count=1000&authoruserid={author_id}&fields=TrackId%2CTrackName%2CUId%2CAuthorTime%2CUploadedAt")
        else:
            response = requests.get(f"https://tmnf.exchange/api/tracks?after={after_id}&order1=1&count=1000&authoruserid={author_id}&fields=TrackId%2CTrackName%2CUId%2CAuthorTime%2CUploadedAt")

        content_dict = response.json()
        more = content_dict["More"]
        all_tracks += content_dict["Results"]
        after_id = content_dict["Results"][-1]["TrackId"]
        
    write_csv(f"{DATA_FILE_PATH}Maps.csv", all_tracks, FIELDS)

# Updater Functions
def sort_recs(recs: list, player_id_key: str):
    sorted_recs = sorted(recs, key=lambda x: (x['Time'], dt.strptime(x['RecordDate'], "%Y-%m-%d %H:%M:%S")))
    sorted_and_unique_recs = []
    player_ids = []
    for rec in sorted_recs:
        if rec[player_id_key] not in player_ids:
            sorted_and_unique_recs.append(rec)
            player_ids.append(rec[player_id_key])
        
    return sorted_and_unique_recs

def merge_recs(old_recs: dict, new_recs: dict, player_id_key: str):
    for track_id, recs in new_recs.items():
        if track_id in old_recs:
            combined_recs = old_recs[track_id] + recs
            old_recs[track_id] = sort_recs(combined_recs, player_id_key)
        else:
            old_recs[track_id] = recs
    return old_recs

def update_tmx_recs(tracks_dict: dict):
    session = requests.Session()
    replays = []
    buffer_date, progress, replay_dict = read_buffer_file("dedi")
    if replay_dict is None:
        replay_dict = {}

    if buffer_date is not None and buffer_date < dt.now(dtm.UTC) - dtm.timedelta(days=2):
        progress = 0
        replay_dict = {}

    track_ids = list(tracks_dict.keys())[progress:]

    def fetch_tmx(track_id):
        url = (
            "https://tmnf.exchange/api/replays"
            f"?trackId={track_id}&fields=User.UserId%2CReplayTime%2CReplayAt"
        )
        try:
            r = session.get(url, timeout=10)
            if r.status_code != 200:
                return track_id, None
            return track_id, r.json()["Results"]
        except Exception:
            return track_id, None

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fetch_tmx, track_id): track_id
            for track_id in track_ids
        }

        for future in tqdm(as_completed(futures), total=len(futures)):
            track_id, content_dict = future.result()
            if content_dict == None:
                print("ERROR: CONNECTION FAILED")
                update_buffer_file(replay_dict, progress, "tmx")
                return False
            replays = []
            for replay in content_dict:
                replays.append(classes.Record({"PlayerId": str(replay['User']['UserId']), "Time": replay['ReplayTime'], "RecordDate": replay['ReplayAt'].split(".")[0]}).properties())
            replay_dict[track_id] = sort_recs(replays, "PlayerId")
            progress += 1
    session.close()
    clear_buffer_file("tmx")
    return replay_dict

def update_dedi_recs(tracks_dict: dict):
    session = requests.Session()
    players_dict = read_json(f"{DATA_FILE_PATH}players.json")["dedi"]
    ml_logins = read_txt(f"{DATA_FILE_PATH}ml_logins.txt")
    players_buffer_date, updated_players, players_dict_buffer = read_buffer_file("players")
    if players_dict_buffer is not None and players_buffer_date is not None and players_buffer_date >= dt.now(dtm.UTC) - dtm.timedelta(days=2):
        for login in updated_players:
            players_dict[login] = players_dict_buffer[login]
    recs_buffer_date, progress, replay_dict = read_buffer_file("dedi")
    if replay_dict is None:
        replay_dict = {}
    if recs_buffer_date is None or recs_buffer_date < dt.now(dtm.UTC) - dtm.timedelta(days=2):
        progress = 0
        replay_dict = {}
    
    for id in tqdm(list(tracks_dict.keys())[progress:]):
        response = session.get(f"http://dedimania.net:8000/MAP?uid={tracks_dict[id][FIELDS[2]]}")
        content = response.content.decode("utf-8")
        if response.status_code == 200:
            replays = []
            content = content.split("\r\n")
            for line in content[1:len(content)-1]:
                    line = line.split(",")
                    login = line[4][4:]
                    nickname = re.sub(REGEX_STRING, "", line[6])
                    replay_time = int(line[1])
                    record_date = int(line[3])
                    replays.append(classes.Record({"PlayerLogin": login, "Time": replay_time, "RecordDate": record_date}).properties())
                    if login not in updated_players:
                        if login not in players_dict:
                            in_ml = False
                            if login in ml_logins:
                                in_ml = True
                            players_dict[login] = classes.Player({"Login": login, "Nickname": nickname, "TeamML": in_ml}).properties()
                            updated_players.append(login)
                        else:
                            players_dict[login] = classes.Player({"Login": login, "Nickname": nickname, "TeamML": players_dict[login]["TeamML"]}).properties()
                    updated_players.append(login)
            replay_dict[id] = sort_recs(replays, "PlayerLogin")
        else:
            print("ERROR: CONNECTION FAILED")
            update_buffer_file(replay_dict, progress, "dedi")
            update_buffer_file(players_dict, updated_players, "players")
            return False
        progress += 1
        time.sleep(2.5)  # To prevent overwhelming the dedi server
    session.close()
    clear_buffer_file(["dedi", "players"])
    update_players(players_dict, "dedi")
    return replay_dict


def update_recs(update_tmx: bool = True, update_dedi: bool = True):
    print("Updating Records:")
    tracks = load_csv(f"{DATA_FILE_PATH}Maps.csv")
    tracks_dict = {row[FIELDS[0]]: row for row in tracks}

    if update_tmx:
        print("Updating TMX Records:")
        tmx_dict = read_json(f"{DATA_FILE_PATH}tmx_records.json")
        new_dict = update_tmx_recs(tracks_dict)

        if not new_dict:
            print("ERROR: TMX UPDATE FAILURE.")
        else:
            write_json(f"{DATA_FILE_PATH}tmx_records.json", merge_recs(tmx_dict, new_dict, "PlayerId"))
        
        update_tmx_players()
    
    if update_dedi:
        print("Updating Dedi Records:")
        dedi_dict = read_json(f"{DATA_FILE_PATH}dedi_records.json")
        new_dict = update_dedi_recs(tracks_dict)
        if not new_dict:
            print("ERROR: DEDI UPDATE FAILURE.")
        else:
            write_json(f"{DATA_FILE_PATH}dedi_records.json", merge_recs(dedi_dict, new_dict, "PlayerLogin"))
    return True

def update_logins(logins: list):
    dedi_recs_dict = read_json(f"{DATA_FILE_PATH}dedi_records.json")
    for track_replays in tqdm(dedi_recs_dict.values()):
        for replay in track_replays:
            login = replay["PlayerLogin"]
            if login not in logins:
                logins.append(login)
    return True

def update_players(player_info, source):
    players_dict = read_json(f"{DATA_FILE_PATH}players.json")
    players_dict[source] = player_info
    write_json(f"{DATA_FILE_PATH}players.json", players_dict)
    return True

def update_tmx_players():
    tmx_records = read_json(f"{DATA_FILE_PATH}tmx_records.json")
    ml_info = read_json(f"{DATA_FILE_PATH}ml_info.json")
    ml_ids = []
    for ids in ml_info.values():
        ml_ids += ids
    ml_ids = list(set(ml_ids))
    user_ids = set()
    for records in tmx_records.values():
        for record in records:
            user_ids.add(record["PlayerId"])

    user_ids = list(user_ids)

    player_data = {}

    def get_player_info(ids):
        if ids == []:
            return
        joined_ids = "%2C".join(ids[:100])
        response = requests.get(f"https://tmnf.exchange/api/users?id={joined_ids}&count=100&fields=UserId%2CName")
        data = response.json()
        for player in data["Results"]:
            if int(player["UserId"]) in ml_ids:
                player_data[player["UserId"]] = classes.Player({"Id": player["UserId"], "Nickname": player["Name"], "TeamML": True}).properties()
            else:
                player_data[player["UserId"]] = classes.Player({"Id": player["UserId"], "Nickname": player["Name"], "TeamML": False}).properties()

        get_player_info(ids[100:])

    get_player_info(user_ids)

    update_players(player_data, "tmx")

def copy_data_to_website():
    files = ["tracks.json", "dedi_records.json", "tmx_records.json", "players.json", "ml_info.json"]
    for file in files:
        write_json(f"{WEBSITE_FILE_PATH}{file}", read_json(f"{DATA_FILE_PATH}{file}"))

def archive_prev_data():
    current_date = dt.strftime(dt.now(dtm.UTC), "%Y-%m-%d")
    os.makedirs(f"Archive/{current_date}", exist_ok=True)
    files = ["tracks.json", "dedi_records.json", "tmx_records.json", "players.json", "ml_info.json"]
    for file in files:
        write_json(f"Archive/{current_date}/{current_date}_{file}", read_json(f"{DATA_FILE_PATH}{file}"))
