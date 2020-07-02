import unittest
from selenium import webdriver

from resources.test_data import CommonData
from resources.page_object.login_page import LoginPage
from resources.locators import HomePageLocators, LoginPageLocators


class LoginFailureTestCaseBase(unittest.TestCase):
    """
    Test of  Login functionality - login failure

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


class LoginFailureTestCase(LoginFailureTestCaseBase):

    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)
        self.correct_email = CommonData.USER_EMAIL
        self.correct_password = CommonData.PASSWORD

    def test_TS01_TC004_failed_login_correct_email_and_incorrect_password(self):
        try:
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            password = CommonData.INCORRECT_PASSWORD_1
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
            self.login_page.login_as(username=self.correct_email, password=password, submit=True)
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.element_is_visible(HomePageLocators.LOGIN_BUTTON) is True
            self.login_page.assert_elemnet_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")
            password = CommonData.INCORRECT_PASSWORD_2
            self.login_page.login_as(username=self.correct_email, password=password, submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC004_")
            raise

    def test_TS01_TC005_failed_login_incorrect_email_and_correct_password(self):
        try:
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            self.login_page.login_as(username=CommonData.INCORRECT_EMAIL_1, password=self.correct_password, submit=True)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.get_element(HomePageLocators.LOGIN_BUTTON).text != "Wyloguj"
            self.login_page.login_as(username=CommonData.INCORRECT_EMAIL_2, password=self.correct_password,
                                     submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC005_")
            raise

    def test_TS01_TC006_failed_login_correct_email_and_password_with_space_key(self):
        try:
            self.login_page.login_as(username=' ' + self.correct_email, password=' ' + self.correct_password,
                                     submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC006_")
            raise

    def test_TS01_TC007_failed_login_email_and_password_are_left_blank(self):
        try:
            self.login_page.click_on(LoginPageLocators.USERNAME_FIELD)
            self.login_page.enter_text_and_click_enter(LoginPageLocators.PASSWORD_FIELD, "")
            self.login_page.assert_path_in_current_url("/klub/zaloguj-sie")
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC007_")
            raise

    def test_TS01_TC008_failed_login_reverse_data_input(self):
        try:
            self.login_page.login_as(username=self.correct_password, password=self.correct_email, submit=False)
            assert "Zaloguj" in self.login_page.driver.page_source
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC008_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
