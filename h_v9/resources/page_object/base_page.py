from datetime import date
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from test_data import Dev, Staging


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
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_loctor)).click()

    def assert_elemnet_text(self, by_locator, element_text):
        web_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        assert web_element.text == element_text

    def assert_path_in_current_url(self, path):
        current_url = self.driver.current_url
        assert path in current_url

    def enter_text(self, by_locator, text):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        element.clear()
        return element.send_keys(text)

    def enter_text_and_click_enter(self, by_locators, text):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locators))
        element.clear()
        return element.send_keys(text + Keys.ENTER)

    def element_is_enable(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))

    def elemnt_is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def hover_to(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return ActionChains(self.driver).move_to_element(element).perform()

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

    def do_screenshot(self, name):
        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(required_width, required_height)
        current_date = date.today()
        current_date_template = str(current_date).replace('-', '')
        t = time.localtime()
        current_time = time.strftime("%H-%M-%S", t)
        path = f"../reports/{current_date_template}/screenshot_{name}{current_time}.png"
        self.driver.find_element_by_tag_name('body').screenshot(path)
        self.driver.set_window_size(original_size['width'], original_size['height'])
