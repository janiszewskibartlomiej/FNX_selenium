import inspect
import unittest

import pytest
from selenium import webdriver

from resources.test_data import CommonData
from resources.page_object.login_page import LoginPage
from resources.locators import HomePageLocators, LoginPageLocators


class LoginFailureTestCaseBase(unittest.TestCase):
    """
    Test of  Login functionality - login failure

    """


    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(CommonData.CHROME_PATH, options=chrome_options)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()


class LoginFailureTestCase(LoginFailureTestCaseBase):


    def setUp(self):
        super().setUp()
        self.login_page = LoginPage(self.driver)
        self.correct_email = CommonData.USER_EMAIL
        self.correct_password = CommonData.PASSWORD

    # @pytest.fixture(scope='session', autouse=True)
    # def browser(self):
    #     super(LoginFailureTestCase, self)
    #     return self.driver

    def test_TS01_TC004_failed_login_correct_email_and_incorrect_password(self):
        try:
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            password = CommonData.INCORRECT_PASSWORD_1
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
            self.login_page.login_as(username=self.correct_email, password=password, submit=True)
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.element_is_visible(HomePageLocators.LOGIN_BUTTON) is True
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")
            password = CommonData.INCORRECT_PASSWORD_2
            self.login_page.login_as(username=self.correct_email, password=password, submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:29] + inspect.stack()[0][1][-9:-3] + '_')
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
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:29] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    def test_TS01_TC006_failed_login_correct_email_and_password_with_space_key(self):
        try:
            self.login_page.login_as(username=' ' + self.correct_email, password=' ' + self.correct_password,
                                     submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_element_text(HomePageLocators.LOGIN_BUTTON, "Zaloguj")

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:29] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    def test_TS01_TC007_failed_login_email_and_password_are_left_blank(self):
        try:
            self.login_page.click_on(LoginPageLocators.USERNAME_FIELD)
            self.login_page.enter_text_and_click_enter(LoginPageLocators.PASSWORD_FIELD, "")
            self.login_page.assert_path_in_current_url("/klub/zaloguj-sie")
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:29] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    def test_TS01_TC008_failed_login_reverse_data_input(self):
        try:
            self.login_page.login_as(username=self.correct_password, password=self.correct_email, submit=False)
            assert "Zaloguj" in self.login_page.driver.page_source
            self.login_page.assert_element_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")

        except:
            self.login_page.do_screenshot(
                name=inspect.stack()[0][-3][:29] + inspect.stack()[0][1][-9:-3] + '_')
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
