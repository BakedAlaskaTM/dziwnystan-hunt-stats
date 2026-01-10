import os, shutil
from pathlib import Path

COPY_PATH = r"C:\Users\HS\Documents\Python-Projects\Website\Website\data"
DATA_FOLDER = r"C:\Users\HS\Documents\Python-Projects\TM Testing\Data"
DATA_FILES = ["dedi_records.json", "tmx_records.json", "players.json", "tracks.json"]
for file in DATA_FILES:
    shutil.copyfile(rf"{DATA_FOLDER}\{file}", rf"{COPY_PATH}")
print("Data files copied successfully.")