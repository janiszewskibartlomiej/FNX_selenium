import time
import unittest
from selenium import webdriver

from resources.test_data import CommonData, Staging
from resources.page_object.login_page import LoginPage
from resources.locators import HomePageLocators, LoginPageLocators


class LoginSuccessTestCaseBase(unittest.TestCase):
    """
        Test of  Login functionality -  Success login

        User should success login with correct username or e-mail address and password.

        """

    def setUp(self) -> None:
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        self.driver = webdriver.Firefox(executable_path=CommonData.FIREFOX_PATH, firefox_profile=profile,
                                        options=firefox_options)
        # self.driver = webdriver.Remote(command_executor='http://192.168.8.103:5000/wd/hub', desired_capabilities= firefox_options.to_capabilities())
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()
        # self.driver.stop_client()


class LoginSuccessTestCase(LoginSuccessTestCaseBase):

    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)
        self.password = CommonData.PASSWORD
        self.after_login_url = '/klub-logged-in/moj-klub-maluszka'

    def test_TS01_TC001_successful_login_with_username(self):
        try:
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            username = Staging.USER_NAME
            self.login_page.login_as(username=username, password=self.password, submit=True)
            time.sleep(3)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.element_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
            self.login_page.assert_elemnet_text(LoginPageLocators.LOGOUT_BUTTON, "Wyloguj")
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            assert self.login_page.element_is_visible(LoginPageLocators.SUBMIT_BTN) is True
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC001_")
            raise

    def test_TS01_TC002_successful_login_with_email(self):
        try:
            input_tag = "input"
            logout_text = "Wyloguj"
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            username = CommonData.USER_EMAIL
            username_input = self.login_page.get_element(by_locator=LoginPageLocators.USERNAME_FIELD)
            self.assertEqual(username_input.tag_name, input_tag)
            password_input = self.login_page.get_element(by_locator=LoginPageLocators.PASSWORD_FIELD)
            self.assertEqual(password_input.tag_name, input_tag)
            self.login_page.login_as(username=username, password=self.password, submit=False)
            time.sleep(3)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(LoginPageLocators.LOGOUT_BUTTON, logout_text)
            self.assertTrue(logout_text in self.login_page.driver.page_source)
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            time.sleep(1)
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC002_")
            raise

    def test_TS01_TC003_successful_login_with_email_capitalizer(self):
        try:
            text_in_dropdown = "Jesteś zalogowana/y jako"
            username = CommonData.USER_EMAIL_CAPITALIZER
            self.login_page.login_as(username=username, password=self.password, submit=False)
            self.login_page.is_clickable(by_locator=HomePageLocators.ICON_ACCOUNT)
            time.sleep(3)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            drop_down = self.login_page.get_element(by_locator=LoginPageLocators.DROP_DOWN_SECTION)
            assert text_in_dropdown in drop_down.get_attribute("innerHTML")
            assert text_in_dropdown in self.login_page.driver.page_source
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC003_")
            raise

    def test_TS01_TC009_successful_login_with_facebook(self):
        try:
            link_text = "Moje dzieci"
            self.login_page.click_on(by_loctor=LoginPageLocators.LOGIN_BY_FACEBOOK)
            self.login_page.enter_text(by_locator=LoginPageLocators.FACEBOOK_EMAIL, text=CommonData.FACEBOOK_EMAIL)
            self.login_page.enter_text(by_locator=LoginPageLocators.FACEBOOK_PASSWORD,
                                       text=CommonData.FACEBOOK_PASSWORD)
            self.login_page.click_on(by_loctor=LoginPageLocators.FACEBOOK_LOGIN_BTN)
            assert link_text in self.login_page.driver.page_source
            self.login_page.click_on(by_loctor=LoginPageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(by_locator=LoginPageLocators.MY_CHILDREN_LINK_TEXT,
                                                       element_text=link_text)
            self.login_page.assert_path_in_current_url(path="klub-logged-in/moj-klub-maluszka/")
        except:
            self.login_page.do_screenshot(name="test_TS01_TC009_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
