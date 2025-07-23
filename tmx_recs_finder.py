from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import csv
import functions

FIELDS = ["TrackId", "TrackName", "UId", "AuthorTime", "UploadedAt"]

tracks = functions.load_csv("Maps.csv")

