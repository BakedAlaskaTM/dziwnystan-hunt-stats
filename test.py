from functions import *

data_files = ["dedi_records.json", "tmx_records.json"]
directory_path = "Archive"
players = read_json(f"{DATA_FILE_PATH}players.json")
tracks = read_json(f"{DATA_FILE_PATH}tracks.json")

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
for 


            
            