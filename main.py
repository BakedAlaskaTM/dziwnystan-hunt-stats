import os
import sys
import functions
import logging

logging.basicConfig(
    filename=f"{functions.MAIN_PATH}/Logs/run.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    functions.archive_prev_data()

    functions.update_recs()

    functions.copy_data_to_website()

if __name__ == "__main__":
    logging.info("Script started")
    logging.info(f"Python executable: {sys.executable}")
    logging.info(f"Working directory: {os.getcwd()}")
    logging.info(f"Script location: {__file__}")
    logging.info(f"Process ID: {os.getpid()}")
    try:
        main()
    except Exception:
        logging.exception("Script crashed")

    logging.info("Script finished")