import unittest
from selenium import webdriver
# from resource.test_data import Dev
# from login_page import LoginPage
# from locators import HomePageLocators, LoginPageLocators
from test_data import CommonData, Staging
from resources.page_object.login_page import LoginPage
from resources.locators import HomePageLocators, LoginPageLocators


class LoginSuccessTestCaseBase(unittest.TestCase):
    """
        Test of  Login functionality -  Success login

        User should success login with correct username or e-mail address and password.

        """

    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(CommonData.CHROME_PATH, options=chrome_options)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()


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
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            assert self.login_page.elemnt_is_visible(LoginPageLocators.LOGOUT_BUTTON) is True
            self.login_page.assert_elemnet_text(LoginPageLocators.LOGOUT_BUTTON, "Wyloguj")
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            assert self.login_page.elemnt_is_visible(LoginPageLocators.SUBMIT_BTN) is True
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC001_")
            raise

    def test_TS01_TC002_successful_login_with_email(self):
        try:
            self.login_page.assert_path_in_current_url(path='/klub/zaloguj-sie')
            username = CommonData.USER_EMAIL
            self.login_page.login_as(username=username, password=self.password, submit=False)
            self.login_page.assert_path_in_current_url(path=self.after_login_url)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(LoginPageLocators.LOGOUT_BUTTON, "Wyloguj")
            self.login_page.click_on(LoginPageLocators.LOGOUT_BUTTON)
            self.login_page.assert_elemnet_text(LoginPageLocators.SUBMIT_BTN, "Zaloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC002_")
            raise

    def test_TS01_TC003_successful_login_with_email_capitalizer(self):
        try:
            username = CommonData.USER_EMAIL_CAPITALIZER
            self.login_page.login_as(username=username, password=self.password, submit=False)
            self.login_page.click_on(HomePageLocators.ICON_ACCOUNT)
            self.login_page.assert_elemnet_text(LoginPageLocators.LOGOUT_BUTTON, "Wyloguj")
        except:
            self.login_page.do_screenshot(
                name="test_TS01_TC003_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
