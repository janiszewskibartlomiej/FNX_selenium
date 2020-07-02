from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    ICON_ACCOUNT = (By.XPATH, "//span[contains(@class,'kkicon kkicon-account')]")
    MY_CHILDREN_LINK_TEXT = (By.XPATH, "//a[contains(text(),'Moje')]")
    DROP_DOWN_SECTION = (By.ID, "header-account")
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='Login']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Hasło']")
    SUBMIT_BTN = (By.NAME, 'login')
    CAPTCHA_SECTION = (By.XPATH, "//div[@class='g-recaptcha']")
    LOGOUT_BUTTON = (By.LINK_TEXT, "Wyloguj")
    MY_PROFILE = (By.XPATH, "//a[contains(text(),'Mój')]")
    LOGIN_BY_FACEBOOK = (By.XPATH, "//a[@class='loginBtn--facebook']")
    FACEBOOK_EMAIL = (By.XPATH, "//input[@id='email']")
    FACEBOOK_PASSWORD = (By.XPATH, "//input[@id='pass']")
    FACEBOOK_LOGIN_BTN = (By.XPATH, "//button[@id='loginbutton']")

class HomePageLocators(object):
    ICON_ACCOUNT = (By.XPATH, "//span[contains(@class,'kkicon kkicon-account')]")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='btn btn--brand']")
