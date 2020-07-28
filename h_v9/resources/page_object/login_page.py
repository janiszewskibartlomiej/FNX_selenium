from .base_page import BasePage
from ..locators import LoginPageLocators


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        url = f'{self.base_url}//klub/zaloguj-sie'
        self.driver.get(url)

    def login_as(self, username: str, password: str, submit=True):

        self.enter_text(LoginPageLocators.USERNAME_FIELD, username)

        if submit == False:
            self.enter_text_and_click_enter(LoginPageLocators.PASSWORD_FIELD, password)
        else:
            self.enter_text(LoginPageLocators.PASSWORD_FIELD, password)
            self.click_on(LoginPageLocators.SUBMIT_BTN)
