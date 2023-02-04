import time
import os.path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.logger import Logger
from utils.common import move_file


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
                self.logger.info("subtitle already exists, skipping download...")
            else:
                file_size = self.driver.find_element(
                    By.XPATH, "//span[@class='size-number']"
                ).get_attribute("innerHTML")
                download_btn = self.driver.find_element(
                    By.XPATH, "//button[@class='btn shadow-sm download mt-3 mt-sm-0']"
                )
                self.driver.execute_script("arguments[0].click();", download_btn)
                file_path = self.download_path + subtitle_title
                while not os.path.exists(file_path):
                    self.logger.info(
                        f"downloading {subtitle_title} with file size:{file_size}"
                    )
                    time.sleep(5)
                self.logger.info("subtitle Downloaded at " + file_path)
        except NoSuchElementException:
            self.logger.warning("invalid url...")

    def download_video(
        self, url, with_subtitle=False, create_folder=False, move_to=None
    ):
        try:
            if with_subtitle:
                self.download_subtitle(url)
            self.driver.get(url)
            self.logger.info("downloading video...")
            video_element = self.driver.find_element(
                By.XPATH, "//a[@title='Download Video']"
            )
            self.driver.execute_script("arguments[0].click();", video_element)
            time.sleep(3)
            video_title = self.driver.find_element(By.TAG_NAME, "h1").get_attribute(
                "innerText"
            )
            if os.path.isfile(self.download_path + video_title):
                self.logger.info("video already exists, skipping download...")
            else:
                file_size = self.driver.find_element(
                    By.XPATH, "//span[@class='size-number']"
                ).get_attribute("innerHTML")
                download_btn = self.driver.find_element(
                    By.XPATH, "//button[@class='btn shadow-sm download mt-3 mt-sm-0']"
                )
                self.driver.execute_script("arguments[0].click();", download_btn)
                file_path = self.download_path + video_title
                while not os.path.exists(file_path):
                    self.logger.info(
                        f"downloading {video_title} with file size:{file_size}"
                    )
                    time.sleep(5)
                self.logger.info("video downloaded at " + file_path)
            if os.path.isfile(self.download_path + video_title):
                folder_name = (
                    "".join(video_title.split("(NetNaija.com)")[0]) + "(NetNaija.com)"
                )
                if with_subtitle and create_folder and move_to:
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=move_to + folder_name + "/",
                        file_name=folder_name + ".srt",
                    )
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=move_to + folder_name + "/",
                        file_name=video_title,
                    )
                elif with_subtitle and create_folder:
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=self.download_path + folder_name + "/",
                        file_name=folder_name + ".srt",
                    )
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=self.download_path + folder_name + "/",
                        file_name=video_title,
                    )
                elif with_subtitle and move_to:
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=move_to,
                        file_name=folder_name + ".srt",
                    )
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=move_to,
                        file_name=video_title,
                    )
                elif create_folder:
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=self.download_path + folder_name + "/",
                        file_name=video_title,
                    )
                elif move_to:
                    move_file(
                        origin_folder=self.download_path,
                        destination_folder=move_to,
                        file_name=video_title,
                    )

            else:
                raise ValueError("%s isn't a file!" % self.download_path + video_title)
        except NoSuchElementException:
            self.logger.warning("invalid url...")

    def download_videos(
        self, urls, with_subtitles=False, create_folders=False, move_to=None
    ):
        self.logger.info(f"downloading {len(urls)} videos...")
        for url in urls:
            self.download_video(
                url,
                with_subtitle=with_subtitles,
                create_folder=create_folders,
                move_to=move_to,
            )
        return

    def download_season(
        self, url, with_subtitles=False, create_folder=False, move_to=None
    ):
        try:
            self.driver.get(url)
            season_title = self.driver.find_element(By.TAG_NAME, "h1").get_attribute(
                "innerText"
            )
            self.logger.info(f"downloading {season_title}...")
            episodes = self.driver.find_elements(By.XPATH, "//a[@class='anchor']")
            urls = [episode.get_attribute("href") for episode in episodes]
            self.logger.info(f"found {len(urls)} episodes...")
            if move_to and create_folder:
                move_to = move_to + season_title + "/"
            elif not move_to and create_folder:
                move_to = self.download_path + season_title + "/"
            self.download_videos(
                urls,
                with_subtitles=with_subtitles,
                move_to=move_to,
            )
            return
        except NoSuchElementException:
            self.logger.warning("invalid url...")

    def download_series(self, url, with_subtitles=False, create_folder=False):
        try:
            self.driver.get(url)
            series_title = self.driver.find_element(By.TAG_NAME, "h1").get_attribute(
                "innerText"
            )
            self.logger.info(f"downloading {series_title}...")
            seasons_elements = self.driver.find_elements(
                By.XPATH,
                "//article[@class='vs-many']/div[@class='vs-one']/h3[@class='title']/a",
            )
            self.logger.info(f"found {len(seasons_elements)} season(s)...")
            for season_element in seasons_elements:
                if create_folder:
                    self.download_season(
                        url=season_element.get_attribute("href"),
                        with_subtitles=with_subtitles,
                        create_folder=True,
                        move_to=self.download_path + series_title + "/",
                    )
                else:
                    self.download_season(
                        url=season_element.get_attribute("href"),
                        with_subtitles=with_subtitles,
                        create_folder=True,
                    )

        except NoSuchElementException:
            self.logger.warning("invalid url...")
