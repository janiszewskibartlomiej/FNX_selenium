import inspect
import random
from datetime import date
import time
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ..test_data import Dev, Staging


class BasePage:
    """
    Base Page class that hold common elements
    and functionalities to all pages in app
    """

    def __init__(self, driver):
        self.driver = driver
        # self.base_url = Dev.ACCESS
        self.base_url = Staging.ACCESS

    def click_on(self, by_loctor):
        web_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_loctor))
        return web_element.click()

    def assert_element_text(self, by_locator, element_text):
        web_element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locator))
        assert web_element.text == element_text

    def assert_path_in_current_url(self, path):
        current_url = self.driver.current_url
        assert path in current_url

    def enter_text(self, by_locator, text):
        element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locator))
        element.clear()
        return element.send_keys(text)

    def enter_text_and_click_enter(self, by_locators, text):
        element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locators))
        element.clear()
        return element.send_keys(text + Keys.ENTER)

    def is_clickable(self, by_locator):
        element = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable(by_locator))
        return bool(element)

    def element_is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def get_element(self, by_locator):
        return WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locator))

    def hover_to(self, by_locator):
        element = WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(by_locator))
        return ActionChains(self.driver).move_to_element(element).perform()

    def choose(self, drop_down_select, name):
        drop_down = WebDriverWait(self, 50).until(EC.visibility_of_element_located(drop_down_select))
        drop_down.find_element(By.NAME(name)).click()

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def visit(self, location):
        url = self.base_url + location
        return self.driver.get(url)

    def open_new_tab_and_switch(self):
        tab = self.driver.execute_script("window.open('');")
        return self.driver.switch_to.window(tab[1])

    def get_current_url(self):
        return self.driver.current_url

    def get_random_number(self, today=False):
        if today:
            current_day = date.today()
            str_number = (str(current_day))[-2:]
        else:
            random_number = random.randint(1, 29)
            str_number = str(random_number)
            if len(str_number) < 2:
                str_number = '0' + str_number
        return str_number

    def get_month_number(self, add_number=0):
        month_number = date.today().month + add_number
        str_next_month = str(month_number)
        if len(str_next_month) < 2:
            str_next_month = '0' + str_next_month
        return str_next_month

    def do_screenshot(self, name, ie=False):
        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(required_width, required_height)

        current_date = date.today()
        current_date_template = str(current_date).replace('-', '')
        if not os.path.exists('reports/' + current_date_template):
            os.makedirs('reports/' + current_date_template)

        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"reports/{current_date_template}/screenshot_{name}{current_time}.png"
        if ie:
            # root_path = os.getcwd()  NOW IS NOT NESSERY BECAUSE I SET PYTHONPATH TO h_v9
            # root_path_slice = root_path.replace("tests", "")
            # root_path_rep = root_path_slice.replace("\\", "/")
            # path = f"{root_path_rep}reports/{current_date_template}/screenshot_{name}{current_time}.png"
            self.driver.get_screenshot_as_file(path)
        else:
            self.driver.find_element_by_tag_name('body').screenshot(path)
            self.driver.set_window_size(original_size['width'], original_size['height'])
