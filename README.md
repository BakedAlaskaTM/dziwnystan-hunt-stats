# Trackmania WR Tracker

I made this as a way to check my Trackmania team's progress on trying to hold every world record on maps by Dziwnystan (~1200 maps and counting). It's gone through a few stages of evolution but this is a semi-finished version (still want to add more features like tracking changes in #WRs over time, etc). Currently it's entirely for personal use so code looks a bit cursed. (0% vibe coded at the moment, will increase when I add more features)
I also made a small website (70% vibe coded xdd) to display the data/summary stats for my team members [here](https://bakedalaskatm.github.io/). 
Github Repo: [bakedalaskatm.github.io](https://github.com/BakedAlaskaTM/bakedalaskatm.github.io)

## Introduction

This project is a Python-based data collection tool for Trackmania Nations Forever. It retrieves Trackmania World Record (WR) data from two primary databases: [TMX (Trackmania Exchange)](https://tmnf.exchange/) and [Dedimania](http://dedimania.net/tmstats/), for a specified set of tracks. The program then merges this data into a unified dataset, which can later be used to generate summary statistics, such as the number of world records held per player, or tracking how many world records are held by the **ML** team.

## Features

- **Data Collection:** Automatically fetches track and record data from TMX and Dedimania APIs.
- **Data Merging:** Combines data from both sources into a unified, easy-to-use dataset (JSON format).
- **Nickname Formatting:** Handles and fixes Trackmania's custom nickname formatting.

## Project Structure

- `main.py`: The main entry point for running the data collection pipeline.
- `classes.py`: Contains the object-oriented data models used to represent tracks, players, and records.
- `functions.py`: Core utility functions for API requests and data processing.
- `tmx_map_finder.py`: Helper script to find and extract track information from TMX.
- `fix_nicknames.py`: Utility to process and clean Trackmania player nicknames (handling color codes and formatting).
- `Data/`: Directory where the fetched data and generated statistics are stored.
- `Archive/`: Directory for archiving older datasets or runs.

## Prerequisites

- Python 3.x
- Required Python packages (e.g., `requests`). You can install dependencies via pip.

## Customization

To track a different team or a different set of maps, you can modify the configuration section within `main.py` or `functions.py` as needed.

## License

This project is open-source and available for personal use and modification.
