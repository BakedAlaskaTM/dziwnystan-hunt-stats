# Trackmania WR Tracker

This project is a Python-based data collection tool for Trackmania Nations Forever. It retrieves Trackmania World Record (WR) data from two primary databases—[TMX (Trackmania Exchange)](https://tmnf.exchange/) and [Dedimania](http://dedimania.net/tmstats/)—for a specified set of tracks. The program then merges this data into a unified dataset, which can later be used to generate summary statistics, such as the number of world records held per player, or tracking how many world records are held by the **ML** team.

## Features

- **Data Collection:** Automatically fetches track and record data from TMX and Dedimania APIs.
- **Data Merging:** Combines data from both sources into a unified, easy-to-use dataset.
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
