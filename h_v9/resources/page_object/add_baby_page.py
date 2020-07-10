from .base_page import BasePage
from .login_page import LoginPage
from ..test_data import CommonData


class AddBabyPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        LoginPage(self.driver).login_as(username=CommonData.USER_EMAIL, password=CommonData.PASSWORD)
        url = f"{self.base_url}/profil-uzytkownika/dodaj-dziecko"
        self.driver.get(url)

