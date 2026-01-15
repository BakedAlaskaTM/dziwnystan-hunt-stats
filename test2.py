from functions import *

players_dict = read_json(f"{DATA_FILE_PATH}players.json")

dedi_dict = players_dict["dedi"]["dedi"]
tmx_dict = players_dict["dedi"]["tmx"]

write_json(f"{DATA_FILE_PATH}players.json", {"dedi": dedi_dict, "tmx": tmx_dict})