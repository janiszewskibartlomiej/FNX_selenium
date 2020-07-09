import time
import unittest
from selenium import webdriver
import inspect
from resources.test_data import CommonData
from resources.page_object.home_page import HomePage
from resources.page_object.login_page import LoginPage
from resources.locators import HomePageLocators, LoginPageLocators


class CaptchaTestCaseBase(unittest.TestCase):

    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(CommonData.CHROME_PATH, options=chrome_options)
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

    def setUp(self):
        super().setUp()
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)

    def test_TS02_TC001_captcha_is_visible_after_three_times_incorect_login(self):
        try:
            self.home_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.home_page.click_on(HomePageLocators.LOGIN_BUTTON)
            self.home_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            user = 'test@test.pl'
            password = 'Test1234!'
            self.login_page.login_as(username=user, password=password, submit=True)
            self.login_page.login_as(username=user, password=password, submit=True)
            self.login_page.login_as(username=user, password=password, submit=False)
            self.login_page.click_on(LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:24] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    @unittest.skip('I must search solution this test case')
    def test_TS02_TC002_captcha_is_visible_again_after_one_times_incorect_login(self):
        try:
            self.home_page.visit('klub/zaloguj-sie')
            self.home_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            user = 'test@wp.pl'
            password = '1234Test#'
            self.login_page = LoginPage(self.driver)
            self.login_page.login_as(username=user, password=password, submit=True)
            self.login_page.assert_path_in_current_url(path='/walidacja')
            captcha_text = 'reCAPTCHA'
            self.login_page.assert_elemnet_text(LoginPageLocators.CAPTCHA_SECTION, element_text=captcha_text)
            assert captcha_text in self.login_page.driver.page_source
            self.login_page.click_on(LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:24] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    def test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity(self):
        try:
            username = 'select@table.pl'
            password = 'Select1%'
            self.login_page.login_as(username=username, password=password)
            time.sleep(1)
            self.login_page.login_as(username=username, password=password)
            self.login_page.assert_elemnet_text(by_locator=LoginPageLocators.SUBMIT_BTN, element_text="Zaloguj")
            self.login_page.login_as(username=CommonData.USER_EMAIL, password=CommonData.PASSWORD)
            self.login_page.click_on(by_loctor=HomePageLocators.ICON_ACCOUNT)
            time.sleep(1)
            self.login_page.assert_elemnet_text(by_locator=LoginPageLocators.MY_PROFILE, element_text="Mój profil")
            self.login_page.click_on(by_loctor=LoginPageLocators.LOGOUT_BUTTON)
            time.sleep(1)
            self.login_page.login_as(username=username, password=password)
            self.login_page.click_on(by_loctor=LoginPageLocators.CAPTCHA_SECTION)

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:24] + inspect.stack()[0][1][-9:-3] + '_')
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
