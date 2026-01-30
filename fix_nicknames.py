from functions import *

def get_nickname(login):
    response = session.get(f"https://www.xaseco.org/metastats.php?tmf={login}")
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        nick = re.sub(REGEX_STRING, "", content.split('<td width="35%">')[1].split("</td>")[0])
        return nick
    else:
        print("ERROR: CONNECTION FAILED")
        return None

dedi_recs = read_json(f"{DATA_FILE_PATH}dedi_records.json")
players = read_json(f"{DATA_FILE_PATH}players.json")["dedi"]
ml_info = read_json(f"{DATA_FILE_PATH}ml_info.json")

logins = players.keys()
missing_players = []

for track_replays in dedi_recs.values():
        for replay in track_replays:
            if replay["PlayerLogin"] not in logins:
                missing_players.append(replay["PlayerLogin"])

session = requests.Session()

for login in tqdm(missing_players):
    players[login] = classes.Player({"Login": login, "Nickname": get_nickname(login), "TeamML": login in ml_info.keys()}).properties()

session.close()

update_players(players, "dedi")

