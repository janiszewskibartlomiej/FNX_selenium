import sys
import time
import unittest

from selenium import webdriver

from resources.automation_methods import AutomationMethods
from resources.locators import HomePageLocators, LoginPageLocators
from resources.page_object.login_page import LoginPage


class LoginSuccessTestCaseBase(unittest.TestCase):
    """
        Test of  Login functionality -  Success login

        User should success login with correct username or e-mail address and password.

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
        # self.driver = webdriver.Remote(command_executor='http://192.168.8.103:5000/wd/hub', desired_capabilities= firefox_options.to_capabilities())
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()
        # self.driver.stop_client()


class LoginSuccessTestCase(LoginSuccessTestCaseBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        automation_methods = AutomationMethods()
        common_data = automation_methods.get_section_from_config(section_name="CommonData")
        staging_data = automation_methods.get_section_from_config(section_name="Staging")
        self.password = common_data["password"]
        self.email = common_data["user_email"]
        self.username = staging_data["user_name"]
        self.facebook_email = common_data["facebook_email"]
        self.facebook_password = common_data["facebook_password"]
        self.logout_text = "Wyloguj"
        self.login_text = "Zaloguj"
        self.my_children_link_text = "Moje dzieci"
        self.text_in_dropdown = "Jesteś zalogowana/y jako"
        self.login_url = '/klub/zaloguj-sie'
        self.after_login_url = '/klub-logged-in/moj-klub-maluszka'
        self.input_tag = "input"

    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)

    def test_TS01_TC001_successful_login_with_username(self):
        try:
            self.login_page.assert_path_in_current_url(path=self.login_url)
            self.login_page.login_as(username=self.username, password=self.password, submit=True)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.element_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
            self.login_page.assert_element_text(LoginPageLocators.LOGOUT_BUTTON, self.logout_text)
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            time.sleep(3)
            assert self.login_page.element_is_visible(LoginPageLocators.SUBMIT_BTN) is True
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, self.login_text)
        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC002_successful_login_with_email(self):
        try:
            self.login_page.assert_path_in_current_url(path=self.login_url)
            username_input = self.login_page.get_element(by_locator=LoginPageLocators.USERNAME_FIELD)
            self.assertEqual(username_input.tag_name, self.input_tag)
            password_input = self.login_page.get_element(by_locator=LoginPageLocators.PASSWORD_FIELD)
            self.assertEqual(password_input.tag_name, self.input_tag)
            self.login_page.login_as(username=self.email, password=self.password, submit=False)
            time.sleep(3)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(LoginPageLocators.LOGOUT_BUTTON, self.logout_text)
            self.assertTrue(self.logout_text in self.login_page.driver.page_source)
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, self.login_text)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC003_successful_login_with_email_capitalizer(self):
        try:
            self.login_page.login_as(username=self.email.capitalize(), password=self.password, submit=False)
            time.sleep(2)
            self.login_page.is_clickable(by_locator=HomePageLocators.ICON_ACCOUNT)
            time.sleep(3)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            time.sleep(3)
            drop_down = self.login_page.get_element(by_locator=LoginPageLocators.DROP_DOWN_SECTION)
            assert self.text_in_dropdown in drop_down.get_attribute("innerHTML")
            assert self.text_in_dropdown in self.login_page.driver.page_source

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS01_TC009_successful_login_with_facebook(self):
        try:
            self.login_page.click_on(by_loctor=LoginPageLocators.LOGIN_BY_FACEBOOK)
            self.login_page.enter_text(by_locator=LoginPageLocators.FACEBOOK_EMAIL, text=self.facebook_email)
            self.login_page.enter_text(by_locator=LoginPageLocators.FACEBOOK_PASSWORD,
                                       text=self.facebook_password)
            self.login_page.click_on(by_loctor=LoginPageLocators.FACEBOOK_LOGIN_BTN)
            time.sleep(3)
            self.login_page.click_on(by_loctor=LoginPageLocators.ICON_ACCOUNT)
            assert self.my_children_link_text in self.login_page.driver.page_source
            self.login_page.assert_element_text(by_locator=LoginPageLocators.MY_CHILDREN_LINK_TEXT,
                                                element_text=self.my_children_link_text)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
