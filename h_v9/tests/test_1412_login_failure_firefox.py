import sys
import unittest

from selenium import webdriver

from resources.automation_methods import AutomationMethods
from resources.locators import HomePageLocators, LoginPageLocators
from resources.page_object.login_page import LoginPage


class LoginFailureTestCaseBase(unittest.TestCase):
    """
    Test of  Login functionality - login failure

    """

    def setUp(self) -> None:
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference('browser.cache.disk.enable', False)
        profile.set_preference('browser.cache.memory.enable', False)
        profile.set_preference('browser.cache.offline.enable', False)
        profile.set_preference('network.http.use-cache', False)
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        firefox_path = AutomationMethods().get_path_from_name(file_name="geckodriver.exe")
        self.driver = webdriver.Firefox(executable_path=firefox_path, firefox_profile=profile,
                                        options=firefox_options)
        self.driver.set_page_load_timeout(30)
        # self.driver = webdriver.Remote(command_executor='http://192.168.8.103:5000/wd/hub', desired_capabilities= firefox_options.to_capabilities())
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()
        # self.driver.stop_client()


class LoginFailureTestCase(LoginFailureTestCaseBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_btn_text = "Zaloguj"
        self.login_path = '/klub/zaloguj-sie'
        self.logout_btn_text = "Wyloguj"
        common_data = AutomationMethods().get_section_from_config(section_name="CommonData")
        self.correct_email = common_data["user_email"]
        self.correct_password = common_data["password"]
        self.incorrect_email_1 = common_data["incorrect_email_1"]
        self.incorrect_email_2 = common_data["incorrect_email_2"]
        self.incorrect_password_1 = common_data["incorrect_password_1"]
        self.incorrect_password_2 = common_data["incorrect_password_2"]

    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)

    def test_TS01_TC004_failed_login_correct_email_and_incorrect_password(self):
        try:
            self.login_page.assert_path_in_current_url(path=self.login_path)
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, self.login_btn_text)
            self.login_page.incorrect_login_as(username=self.correct_email, password=self.incorrect_password_1, submit=True)
            self.login_page.assert_path_in_current_url(path=self.login_path)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.element_is_visible(HomePageLocators.LOGIN_BUTTON) is True
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, self.login_btn_text)
            self.login_page.incorrect_login_as(username=self.correct_email, password=self.incorrect_password_2, submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, self.login_btn_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC005_failed_login_incorrect_email_and_correct_password(self):
        try:
            self.login_page.assert_path_in_current_url(path=self.login_path)
            self.login_page.login_as(username=self.incorrect_email_1,
                                     password=self.correct_password, submit=True)
            self.login_page.incorrect_login_as(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.get_element(HomePageLocators.LOGIN_BUTTON).text != self.logout_btn_text
            self.login_page.login_as(username=self.incorrect_email_2,
                                     password=self.correct_password, submit=False)
            self.login_page.incorrect_login_as(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, self.login_btn_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC006_failed_login_correct_email_and_password_with_space_key(self):
        try:
            self.login_page.login_as(username=' ' + self.correct_email, password=' ' + self.correct_password,
                                     submit=False)
            self.login_page.incorrect_login_as(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, self.login_btn_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC007_failed_login_email_and_password_are_left_blank(self):
        try:
            self.login_page.click_on(LoginPageLocators.USERNAME_FIELD)
            self.login_page.enter_text_and_click_enter(LoginPageLocators.PASSWORD_FIELD, "")
            self.login_page.assert_path_in_current_url(self.login_path)
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, self.login_btn_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC008_failed_login_reverse_data_input(self):
        try:
            self.login_page.incorrect_login_as(username=self.correct_password, password=self.correct_email, submit=False)
            assert self.login_btn_text in self.login_page.driver.page_source
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, self.login_btn_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
