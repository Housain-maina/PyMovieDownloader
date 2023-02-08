import os
import shutil
from pymoviedownloader.utils.logger import Logger


def move_file(origin_folder=None, destination_folder=None, file_name=None):
    logger = Logger.logger(name=__name__)
    try:
        os.makedirs(destination_folder, exist_ok=True)
        logger.info(f"moving {file_name} to {destination_folder}...")
        shutil.move(origin_folder + file_name, destination_folder + file_name)
        logger.info(f"moved successfully!")
    except Exception as e:
        logger.exception(e)
