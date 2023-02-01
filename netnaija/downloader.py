import time
import os.path
import shutil
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.logger import Logger


class Downloader:
    def __init__(self, driver):
        self.driver, self.download_path = driver
        self.logger = Logger.logger(name=__name__)

    def download_subtitle(self, url):
        try:
            self.driver.get(url)
            self.logger.info("downloading subtitle...")
            download_element = self.driver.find_element(
                By.XPATH, "//a[@title='Download Subtitle']"
            )
            self.driver.execute_script("arguments[0].click();", download_element)
            time.sleep(5)
            subtitle_title = self.driver.find_element(By.TAG_NAME, "h1").get_attribute(
                "innerText"
            )
            if os.path.isfile(self.download_path + subtitle_title):
                self.logger.info(
                    "subtitle already exists at "
                    + self.download_path
                    + subtitle_title
                    + " skipping download..."
                )
                return
            file_size = self.driver.find_element(
                By.XPATH, "//span[@class='size-number']"
            ).get_attribute("innerHTML")
            download_btn = self.driver.find_element(
                By.XPATH, "//button[@class='btn shadow-sm download mt-3 mt-sm-0']"
            )
            self.driver.execute_script("arguments[0].click();", download_btn)
            file_path = self.download_path + subtitle_title
            while not os.path.exists(file_path):
                self.logger.info(f"downloading {subtitle_title} with file size:{file_size}")
                time.sleep(5)
            if os.path.isfile(file_path):
                self.logger.info("subtitle Downloaded at " + file_path)
            else:
                raise ValueError("%s isn't a file!" % file_path)
        except NoSuchElementException:
            self.logger.warning("invalid subtitle url...")

    def download_video(self, url, with_subtitle=False, create_folder=False):
        try:
            if with_subtitle:
                self.download_subtitle(url)
            self.driver.get(url)
            self.logger.info("downloading video...")
            video_element = self.driver.find_element(
                By.XPATH, "//a[@title='Download Video']"
            )
            self.driver.execute_script("arguments[0].click();", video_element)
            time.sleep(5)
            video_title = self.driver.find_element(By.TAG_NAME, "h1").get_attribute(
                "innerText"
            )
            if os.path.isfile(self.download_path + video_title):
                self.logger.info(
                    "video already exists at "
                    + self.download_path
                    + video_title
                    + " skipping download..."
                )
                return
            file_size = self.driver.find_element(
                By.XPATH, "//span[@class='size-number']"
            ).get_attribute("innerHTML")
            download_btn = self.driver.find_element(
                By.XPATH, "//button[@class='btn shadow-sm download mt-3 mt-sm-0']"
            )
            self.driver.execute_script("arguments[0].click();", download_btn)
            file_path = self.download_path + video_title
            while not os.path.exists(file_path):
                self.logger.info(f"downloading {video_title} with file size:{file_size}")
                time.sleep(5)
            if os.path.isfile(file_path):
                self.logger.info("video downloaded at " + file_path)
                if create_folder:
                    try:
                        folder_name = (
                            "".join(video_title.split("(NetNaija.com)")[0])
                            + "(NetNaija.com)"
                        )
                        os.mkdir(self.download_path + folder_name)
                        self.logger.info(
                            f"moving files {self.download_path}{folder_name}"
                        )
                        if with_subtitle:
                            shutil.move(
                                f"{self.download_path}{folder_name}.srt",
                                f"{self.download_path}{folder_name}/{folder_name}.srt",
                            )
                        shutil.move(
                            file_path,
                            f"{self.download_path}{folder_name}/{video_title}",
                        )
                        self.logger.info(
                            f"files moved to {self.download_path}{folder_name}"
                        )
                    except Exception as e:
                        self.logger.exception(e)
            else:
                raise ValueError("%s isn't a file!" % file_path)
        except NoSuchElementException:
            self.logger.warning("invalid video url...")
