from functions import *

summary_stats = read_json(f"{DATA_FILE_PATH}summary_stats.json")

directory_path = f"{MAIN_PATH}/Archive"
folder_names = sorted([name for name in os.listdir(directory_path) 
    if os.path.isdir(os.path.join(directory_path, name))])[1:]

new_dates = list(set(folder_names) - set(summary_stats.keys()))

print(new_dates)