from functions import *

ml_info = read_json(f"{DATA_FILE_PATH}ml_info.json")

for key, value in ml_info.items():
    ml_info[key] = {
        "Login": key,
        "TMX": value
    }

write_json(f"{DATA_FILE_PATH}ml_info.json", ml_info)