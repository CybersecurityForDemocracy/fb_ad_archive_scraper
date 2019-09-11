""" This class downloads facebook ad archive reports """
# Webdriver code generated using Selenium IDE

import os
import time
import json
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

FB_COUNTRY_SELECTOR_CSS_CLASS = ".\\_7vg0"
FB_DOWNLOAD_BUTTON_CSS_CLASS = ".\\_7vio"
time_frames_to_css_selectors = {
    "1_DAY": ".\\_101b:nth-child(1) > .label",
    "7_DAYS": ".\\_101b:nth-child(2) > .label",
    "30_DAYS": ".\\_101b:nth-child(3) > .label",
    "90_DAYS": ".\\_101b:nth-child(4) > .label",
    "ALL_TIME": ".\\_101b:nth-child(5) > .label", }

CHROME_DRIVER_PATH = "/home/divam/projects/fb_report_collector/chromedriver"

class FacebookArchiveReportDownloader():
    def __init__(self, download_dir):
        self.base_url = "https://www.facebook.com/ads/archive/report/"
        self.download_dir = download_dir
        self.driver = self.get_headless_driver_with_downloads(download_dir, CHROME_DRIVER_PATH)
        self.driver.get(self.base_url)

    def quit_driver(self):
        self.driver.quit()

    def set_country(self, country):
        self.driver.find_element(
            By.CSS_SELECTOR, FB_COUNTRY_SELECTOR_CSS_CLASS).click()
        self.driver.find_element(By.LINK_TEXT, country).click()

    def download_all_reports(self):
        for time_span, css_selector in time_frames_to_css_selectors.items():
            try:
                self.driver.find_element(By.CSS_SELECTOR, css_selector).click()
                time.sleep(1)
                self.driver.find_element(
                    By.CSS_SELECTOR, FB_DOWNLOAD_BUTTON_CSS_CLASS).click()
                time.sleep(1)
            except ElementClickInterceptedException:
                driver.save_screenshot(os.path.join(
                    self.download_dir, f'{time_span}_Error.png'))
                print(f"Could not download data for time span: {time_span}")


    def get_headless_driver_with_downloads(self, path, webdriver_executable_path):
        # This works around https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        # Using https://github.com/shawnbutton/PythonHeadlessChrome as a reference
        download_dir = path or os.getcwd()
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True}
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(
            executable_path=webdriver_executable_path, chrome_options=chrome_options)
        driver.command_executor._commands["send_command"] = (
            "POST", "/session/$sessionId/chromium/send_command")

        params = {"cmd": "Page.setDownloadBehavior", "params": {
            "behavior": "allow", "downloadPath": download_dir}}
        driver.execute("send_command", params)
        return driver


if __name__ == "__main__":
    download_dir = "/home/divam/projects/fb_report_collector/"
    archive_downloader = FacebookArchiveReportDownloader(download_dir)
    # Country must match the string on the webpage drop down.
    archive_downloader.set_country("Canada")
    archive_downloader.download_all_reports()
    archive_downloader.quit_driver()
