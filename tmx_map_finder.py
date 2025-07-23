from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import csv
import functions

FIELDS = ["TrackId", "TrackName", "UId", "AuthorTime", "UploadedAt"]

driver = webdriver.Edge()
more = True
all_tracks = []

while more:
    if not all_tracks:
        driver.get(f"https://tmnf.exchange/api/tracks?order1=1&count=1000&authoruserid=8672272&fields=TrackId%2CTrackName%2CUId%2CAuthorTime%2CUploadedAt")
    else:
        driver.get(f"https://tmnf.exchange/api/tracks?after={after_id}&order1=1&count=1000&authoruserid=8672272&fields=TrackId%2CTrackName%2CUId%2CAuthorTime%2CUploadedAt")

    content = driver.find_element(By.TAG_NAME, "pre").get_attribute("innerHTML")
    content_dict = json.loads(content)
    more = content_dict["More"]
    all_tracks += content_dict["Results"]
    after_id = content_dict["Results"][-1]["TrackId"]
driver.close()

with open(f'Maps.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='@')
    writer.writerow([field for field in FIELDS])
    for track_dict in all_tracks:
        writer.writerow([track_dict[field] for field in FIELDS])
    
functions.write_csv("Maps.csv", all_tracks, FIELDS)
