import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.logger import Logger


class Drivers:
    def __init__(self):
        self.logger = Logger.logger(name=__name__)

    def chrome_driver(self, headless=False, download_path=None, driver_path=None):
        self.logger.info("initializing chrome driver...")
        service = Service(ChromeDriverManager().install())
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            self.logger.info('using headless mode...')
        if download_path:
            prefs = {}
            os.makedirs(download_path, exist_ok=True)
            prefs["profile.default_content_settings.popups"] = 0
            prefs["download.default_directory"] = download_path
            options.add_experimental_option("prefs", prefs)
            self.logger.info(f"set download folder to '{download_path}'")
        driver = webdriver.Chrome(service=service, chrome_options=options, executable_path=driver_path)
        self.logger.info("chrome driver initialized successfully")
        return driver, download_path

    def gecko_driver(self, headless=False, download_path=None, driver_path=None):
        self.logger.info("initializing gecko driver...")
        service = Service(GeckoDriverManager().install())
        options = FirefoxOptions()
        if headless:
            options.headless = True
            self.logger.info('using headless mode...')
        if download_path:
            os.makedirs(download_path, exist_ok=True)
            options.set_preference("browser.download.dir", download_path)
            options.set_preference("browser.download.folderList", 2)
            self.logger.info(f"set download folder to '{download_path}'")
        driver = webdriver.Firefox(service=service, options=options, executable_path=driver_path)

        self.logger.info("gecko driver initialized successfully")
        return driver, download_path
