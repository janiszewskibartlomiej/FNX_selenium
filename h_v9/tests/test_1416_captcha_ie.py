import sys
import unittest

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from resources.automation_methods import AutomationMethods
from resources.locators import HomePageLocators, LoginPageLocators
from resources.page_object.home_page import HomePage
from resources.page_object.login_page import LoginPage


class CaptchaTestCaseBase(unittest.TestCase):

    def setUp(self) -> None:
        caps = DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        ie_path = AutomationMethods().get_path_from_file_name(file_name="IEDriverServer.exe")
        self.driver = webdriver.Ie(executable_path=ie_path, capabilities=caps)
        self.driver.set_page_load_timeout(30)
        # self.driver = webdriver.Remote(command_executor='http://192.168.8.103:5000/wd/hub', desired_capabilities= chrome_options.to_capabilities())
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()
        self.driver.stop_client()

    """
    Test of  captcha functionality

    Captcha should displayed when user incorect login three times
    and next times when user incorect login is displayed everytimes.

    """


class CaptchaTestCase(CaptchaTestCaseBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_data = AutomationMethods().get_section_from_config(section_name="CommonData")
        self.email_1 = "test@test.pl"
        self.password_1 = "Test1234!"
        self.login_url = 'klub/zaloguj-sie'
        self.email_2 = "test@wp.pl"
        self.password_2 = "1234Test#"
        self.validation_path = '/walidacja'
        self.captcha_text = "reCAPTCHA"
        self.email_3 = "select@table.pl"
        self.password_3 = "Select1%"
        self.login_text = "Zaloguj"
        self.my_profile_text = "Mój profil"
        self.correct_email = common_data["user_email"]
        self.correct_password = common_data["password"]

    def setUp(self):
        super().setUp()
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)

    def test_TS02_TC001_captcha_is_visible_after_three_times_incorect_login(self):
        try:
            self.home_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.home_page.click_on(HomePageLocators.LOGIN_BUTTON)
            self.home_page.assert_path_in_current_url(path=self.login_url)
            self.login_page.incorrect_login_as(username=self.email_1, password=self.password_1, submit=True)
            self.login_page.incorrect_login_as(username=self.email_1, password=self.password_2, submit=True)
            self.login_page.incorrect_login_as(username=self.email_1, password=self.password_1, submit=False)
            self.login_page.click_on(LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-6:-3] + "_")
            raise

    @unittest.skip("I must search solution this test case")
    def test_TS02_TC002_captcha_is_visible_again_after_one_times_incorect_login(self):
        try:
            self.home_page.visit(self.login_url)
            self.home_page.assert_path_in_current_url(path=self.login_url)
            self.login_page = LoginPage(self.driver)
            self.login_page.incorrect_login_as(username=self.email_2, password=self.password_2, submit=True)
            self.login_page.assert_path_in_current_url(path=self.validation_path)
            self.login_page.assert_element_text(LoginPageLocators.CAPTCHA_SECTION, element_text=self.captcha_text)
            assert self.captcha_text in self.login_page.driver.page_source
            self.login_page.click_on(LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-6:-3] + "_")
            raise

    def test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity(self):
        try:
            self.login_page.incorrect_login_as(username=self.email_3, password=self.password_3)
            self.login_page.incorrect_login_as(username=self.email_2, password=self.password_3)
            self.login_page.assert_element_text(by_locator=LoginPageLocators.SUBMIT_BTN, element_text=self.login_text)
            self.login_page.login_as(username=self.correct_email, password=self.correct_password)
            self.login_page.click_on(by_loctor=HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(by_locator=LoginPageLocators.MY_PROFILE,
                                                element_text=self.my_profile_text)
            self.login_page.click_on(by_loctor=LoginPageLocators.LOGOUT_BUTTON)
            self.login_page.incorrect_login_as(username=self.email_2, password=self.password_1)
            self.login_page.click_on(by_loctor=LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-6:-3] + "_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
