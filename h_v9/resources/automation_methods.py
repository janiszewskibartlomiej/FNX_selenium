import os
import shutil
import sys
import time
from configparser import ConfigParser
from datetime import date
from pathlib import Path

import HtmlTestRunner
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class AutomationMethods:

    def __init__(self):
        self.config = ConfigParser()
        self.config_path = self.get_path_from_name(file_name="config.cfg")

    # template of date example >> 20200715
    def current_date_str_from_number(self) -> str:
        current_date = date.today()
        current_date_template = str(current_date).replace("-", "")
        return current_date_template

    def removing_directories_in_reports_by_number_of_day(self, n_day: int) -> str:
        list_remove_directory = []
        current_date_sub_days = int(self.current_date_str_from_number()) - n_day

        entries = Path('./reports')
        for entry in entries.iterdir():
            try:
                if int(entry.name) <= current_date_sub_days:
                    shutil.rmtree(f"./reports/{entry.name}")
                    list_remove_directory.append(entry.name)
            except ValueError:
                continue
        message = f"\nRemoved directory: {list_remove_directory}\n"
        return message

    def html_test_runner_report(self) -> HtmlTestRunner:
        current_date_template = self.current_date_str_from_number()

        domain = self.get_section_from_config(section_name="Staging")["domain"]
        report_title = f"Test Results of {domain}"

        domain_strip = domain[:14]
        if domain_strip[-1] == "-":
            domain_strip = domain_strip[:13]

        file = sys.argv[0].split("_")
        browser = file[-1][:-3]

        output = "../reports/"

        if browser == "tests":
            browser = "all_browsers"
            report_title = report_title + " in Chrome & FireFox & IE"
            output = output[1:]

        report_name = f"{domain_strip}-{browser}"

        runner = HtmlTestRunner.HTMLTestRunner(output=output + current_date_template, combine_reports=True,
                                               report_title=report_title, report_name=report_name, verbosity=2,
                                               failfast=False, descriptions=True, buffer=False)
        return runner

    def get_path_from_name(self, file_name: str) -> str:
        path = sys.path[1]
        if path[-3:] == "zip":
            path = sys.path[0]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == file_name:
                    abs_path = os.path.join(root, file)
                    return abs_path

    def get_section_from_config(self, section_name: str) -> dict:
        self.config.read(self.config_path)
        data = self.config.items(section_name)
        return dict(data)

    def get_set_from_links_file(self, file_name: str) -> set:
        file_path = self.get_path_from_name(file_name)
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            list_of_links = file.readlines()
            slice_links = set()
            for element in list_of_links:
                element = element[:-2]
                slice_links.add(element)
        return slice_links

    def get_chrome_driver(self) -> webdriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_path = self.get_path_from_name(file_name="chromedriver.exe")
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        return driver

    def get_ie_driver(self) -> webdriver:
        caps = DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        ie_path = AutomationMethods().get_path_from_name(file_name="IEDriverServer.exe")
        driver = webdriver.Ie(executable_path=ie_path, capabilities=caps)
        return driver

    def get_screenshot(self, name: str, driver: webdriver, dictionary_path: str) -> None:
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)

        if not os.path.exists(dictionary_path):
            os.makedirs(dictionary_path)

        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"{dictionary_path}/screenshot_{name}_{current_time}.png"
        time.sleep(1)
        driver.get_screenshot_as_file(path)
        time.sleep(1)
        driver.set_window_size(original_size['width'], original_size['height'])

    def get_screenshot_documentation_from_links(self, set_of_links: set, domain: str, driver: webdriver,
                                                dictionary_path: str) -> dict:
        driver = driver
        incorrect_status_code = {}
        for link in set_of_links:
            response = requests.get(link)
            time.sleep(1)
            status = str(response.status_code)
            print("Link: ", link, "\t\t\t\t\tStatus code: ", status)
            driver.get(link)
            time.sleep(2)
            driver.set_page_load_timeout(8)
            name = link.replace(str(domain), "").replace("/", "_")
            time.sleep(1)
            self.get_screenshot(name=name, driver=driver, dictionary_path=dictionary_path)
            if status[0] in ["4", "3", "5"]:
                incorrect_status_code[link] = status
        return incorrect_status_code

    def send_report_by_email(self):
        pass


if __name__ == '__main__':
    print(sys.path)
    set_of_link = AutomationMethods().get_set_from_links_file(
        file_name="links.csv")
    driver = AutomationMethods().get_ie_driver()
    AutomationMethods().get_screenshot_documentation_from_links(set_of_links=set_of_link,
                                                                domain="",
                                                                driver=driver,
                                                                dictionary_path="../reports/ie_screen_every_page")
