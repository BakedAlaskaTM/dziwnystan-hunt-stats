from functions import *

def calculate_wr(dedi, tmx):
    try:
        dedi_wr = sort_recs(dedi, "PlayerLogin")[0]
    except:
        dedi_wr = None
    try:
        tmx_wr = sort_recs(tmx, "PlayerId")[0]
    except:
        tmx_wr = None
    if tmx_wr is None and dedi_wr is not None:
        return dedi_wr
    elif tmx_wr is not None and dedi_wr is None:
        return tmx_wr
    elif tmx_wr is None and dedi_wr is None:
        return None
    else:
        if dedi_wr["Time"] < tmx_wr["Time"]:
            return dedi_wr
        elif dedi_wr["Time"] > tmx_wr["Time"]:
            return tmx_wr
        else:
            if dt.strptime(dedi_wr["RecordDate"], "%Y-%m-%d %H:%M:%S") > dt.strptime(tmx_wr["RecordDate"], "%Y-%m-%d %H:%M:%S"):
                return dedi_wr
            else:
                return tmx_wr

def generate_ml_stats(wrs_dict):
    ml_stats = {}

    for wr in wrs_dict.values():
        if wr is not None:
            if wr["PlayerId"] is None:
                if players["dedi"][wr["PlayerLogin"]]["TeamML"]:
                    if wr["PlayerLogin"] not in ml_stats.keys():
                        ml_stats[wr["PlayerLogin"]] = 0
                    else:
                        ml_stats[wr["PlayerLogin"]] += 1
            else:
                if players["tmx"][wr["PlayerId"]]["TeamML"]:
                    if ml_info_inv[wr["PlayerId"]] not in ml_stats.keys():
                        ml_stats[ml_info_inv[wr["PlayerId"]]] = 0
                    else:
                        ml_stats[ml_info_inv[wr["PlayerId"]]] += 1
    return ml_stats

data_files = ["dedi_records.json", "tmx_records.json"]
directory_path = "Archive"
players = read_json(f"{DATA_FILE_PATH}players.json")
tracks = read_json(f"{DATA_FILE_PATH}tracks.json")

ml_info = read_json(f"{DATA_FILE_PATH}ml_info.json")
ml_info_inv = {}
for player in ml_info.values():
    for id in player["TMX"]:
        if id not in ml_info_inv.keys():
            ml_info_inv[str(id)] = player["Login"]

folder_names = [name for name in os.listdir(directory_path) 
    if os.path.isdir(os.path.join(directory_path, name))]

for i in range(len(folder_names)):
    folder_names[i] = dt.strptime(folder_names[i], "%Y-%m-%d")

prev = dt.strftime(sorted(folder_names, reverse=True)[0], "%Y-%m-%d")

wrs_gained = 0
wrs_lost = 0

# Analyse prev data
prev_wrs = {}
prev_dedi = read_json(f"{directory_path}/{prev}/{prev}_{data_files[0]}")
prev_tmx = read_json(f"{directory_path}/{prev}/{prev}_{data_files[1]}")
for track_id in tracks.keys():
    prev_wrs[track_id] = calculate_wr(prev_dedi[track_id], prev_tmx[track_id])

ml_stats_prev = generate_ml_stats(prev_wrs)

print(ml_stats_prev)

cur_wrs = {}
cur_dedi = read_json(f"{DATA_FILE_PATH}{data_files[0]}")
cur_tmx = read_json(f"{DATA_FILE_PATH}{data_files[1]}")
for track_id in tracks.keys():
    cur_wrs[track_id] = calculate_wr(cur_dedi[track_id], cur_tmx[track_id])

ml_stats_cur = generate_ml_stats(cur_wrs)

print(ml_stats_cur)

