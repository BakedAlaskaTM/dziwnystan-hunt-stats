import csv
import json
import requests
from datetime import datetime as dt
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import classes

FIELDS = ["TrackId", "TrackName", "UId", "AuthorTime", "UploadedAt"]
DATA_FILE_PATH = "Data/"

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

# Consolidation Functions
def tracks_to_json():
    tracks = load_csv("Maps.csv")
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

    with open(f'Maps.csv', 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter='@')
        writer.writerow([field for field in FIELDS])
        for track_dict in all_tracks:
            writer.writerow([track_dict[field] for field in FIELDS])
        
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

def update_tmx_recs(tracks_dict: dict):
    replays = []
    replay_dict = {}

    for id in tqdm(tracks_dict.keys()):
        response = requests.get(f"https://tmnf.exchange/api/replays?trackId={id}&fields=User.UserId%2CReplayTime%2CReplayAt")
        content = response.json()
        if response.status_code == 200:
            content_dict = content["Results"]
            replays = []
            for replay in content_dict:
                replays.append(classes.Record({"PlayerId": str(replay['User']['UserId']), "Time": replay['ReplayTime'], "RecordDate": replay['ReplayAt'].split(".")[0]}).properties())
            replay_dict[id] = sort_recs(replays, "PlayerId")
        else:
            print("ERROR: CONNECTION FAILED")
            return False
    return replay_dict

def update_dedi_recs(tracks_dict: dict):
    options = Options()
    options.page_load_strategy = "normal"
    replays = []
    replay_dict = {}
    driver = webdriver.Firefox()
    for id in tqdm(tracks_dict.keys()):
        driver.get(f"http://dedimania.net/tmstats/?do=stat&RecOrder3=RANK-ASC&Uid={tracks_dict[id][FIELDS[2]]}&Show=RECORDS")
        replays = []
        try:
            info_table = driver.find_elements(By.XPATH, "//table[@class='tabl'][2]//tr")
            for i in info_table:
                if i.get_attribute("bgcolor") == "#FFFFFF" or i.get_attribute("bgcolor") == "#F0F0F0":
                    login = i.find_element(By.XPATH, "./td[4]/a").get_attribute("innerHTML")
                    replay_time = i.find_element(By.XPATH, "./td[8]/a").get_attribute("innerHTML")
                    time_float = time_converter(replay_time)*1000
                    record_date = i.find_element(By.XPATH, "./td[14]").get_attribute("innerHTML")
                    replays.append(classes.Record({"PlayerLogin": login, "Time": time_float, "RecordDate": record_date}).properties())
        except TimeoutError:
            print("ERROR: CONNECTION FAILED")
            return False
        except:
            pass
        replay_dict[id] = sort_recs(replays, "PlayerLogin")
    driver.quit()
    return replay_dict
        
    
def update_recs(update_tmx: bool = True, update_dedi: bool = True):
    print("Updating Records:")
    tracks = load_csv(f"{DATA_FILE_PATH}Maps.csv")
    tracks_dict = {row[FIELDS[0]]: row for row in tracks}

    if update_tmx:
        print("Updating TMX Records:")
        tmx_dict = update_tmx_recs(tracks_dict)

        if not tmx_dict:
            print("ERROR: TMX UPDATE FAILURE.")
        else:
            write_json(f"{DATA_FILE_PATH}tmx_replays.json", tmx_dict)
    
    if update_dedi:
        print("Updating Dedi Records:")
        dedi_dict = update_dedi_recs(tracks_dict)
        if not dedi_dict:
            print("ERROR: DEDI UPDATE FAILURE.")
        else:
            write_json(f"{DATA_FILE_PATH}dedi_replays.json", dedi_dict)

    return True

def update_logins(logins: list):
    dedi_recs_dict = read_json(f"{DATA_FILE_PATH}dedi_replays.json")
    for track_replays in tqdm(dedi_recs_dict.values()):
        for replay in track_replays:
            login = replay["PlayerLogin"]
            if login not in logins:
                logins.append(login)
    return True

def find_players_info(logins: list, ml_logins: list):
    options = Options()
    options.page_load_strategy = "normal"
    players_dict = {}
    driver = webdriver.Firefox()
    for login in tqdm(logins):
        driver.get(f"http://dedimania.net/tmstats/?do=stat&Login={login}&Show=PLAYERS")
        try:
            info_table = driver.find_elements(By.XPATH, "//table[@class='tabl'][2]//tr")
            for i in info_table:
                if i.get_attribute("bgcolor") == "#FFFFFF" or i.get_attribute("bgcolor") == "#F0F0F0":
                    nickname = i.find_element(By.XPATH, "./td[6]/a").get_attribute("innerHTML")
                    in_ml = False
                    if login in ml_logins:
                        in_ml = True
                    player = classes.Player({"Login": login, "Nickname": nickname, "TeamML": in_ml}).properties()
                    
        except TimeoutError:
            print("ERROR: CONNECTION FAILED")
            return False
        except:
            pass

        players_dict[login] = player
    driver.quit()
    return players_dict

def update_players():
    print("Updating Players:")

    logins = read_json(f"{DATA_FILE_PATH}player_logins.json")
    if logins == None:
        logins = []
    ml_logins = read_txt(f"{DATA_FILE_PATH}ml_logins.txt")
    update_logins(logins)
    write_json(f"{DATA_FILE_PATH}player_logins.json", sorted(logins))

    players_dict = find_players_info(logins, ml_logins)
    if not players_dict:
        print("ERROR: PLAYERS UPDATE FAILURE.")
        return False
    else:
        write_json(f"{DATA_FILE_PATH}players.json", players_dict)
        return True
