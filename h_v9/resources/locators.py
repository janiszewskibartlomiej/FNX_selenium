from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='Login']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Hasło']")
    SUBMIT_BTN = (By.NAME, 'login')
    CAPTCHA_SECTION = (By.XPATH, "//div[@class='g-recaptcha']")


class HomePageLocators(object):
    ICON_ACCOUNT = (By.XPATH, "//span[contains(@class,'kkicon kkicon-account')]")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='btn btn--brand']")
    LOGOUT_BUTTON = (By.LINK_TEXT, "Wyloguj")
