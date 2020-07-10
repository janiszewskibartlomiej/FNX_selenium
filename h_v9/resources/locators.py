from selenium.webdriver.common.by import By


class LoginPageLocators:
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


class HomePageLocators:
    ICON_ACCOUNT = (By.XPATH, "//span[contains(@class,'kkicon kkicon-account')]")
    LOGIN_BUTTON = (By.XPATH, "//a[@class='btn btn--brand']")


class AddBabyLocators:
    I_AM_PREGNANT = (By.XPATH, "//label[@for='notBornChild']")
    I_HAVE_BABY = (By.XPATH, "//label[@for='bornChild']")
    FEMALE = (By.XPATH, "//label[@for='childNotBornGenderF']")
    MALE = (By.XPATH, "//label[@for='childNotBornGenderM']")
    NO_GENDER_RADIO = (By.XPATH, "//label[@for='childNotBornGenderNone']")
    BORN_DAY = (By.XPATH, "//select[@name='borndate_[day]']")
    BORN_MONTH = (By.XPATH, "//select[@name='borndate_[month]']")
    BORN_YEAR = (By.XPATH, "//select[@name='borndate_[year]']")
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder, 'Imię dziecka')]")
    ADD_BABY_BUTTON = (By.NAME, "submit")
    IMG_STORK = (By.XPATH, "//img[@alt='Ciąża']")
    NAME_UNKNOWN = (By.XPATH, "//h2[contains(text(), 'Imię nieznane')]")
    CONFIRM_DATE_OF_BIRTH_LINK = (By.LINK_TEXT, "Potwierdź datę urodzenia dziecka")
    DATE_OF_BIRTH = (By.XPATH, "//span[@class='font-weight-regular']")
    NO_GENDER_TEXT = (By.XPATH, "//div[contains(text(), 'Nieznana')]")
    GIFT_FOR_CHILDBIRTH_INFO = (By.XPATH, "//div[contains(text(), 'Paczka Narodzin')]")
    ALERT_MESSAGE = (By.XPATH, "//p[contains(text(),'Pole jest wymagane')]")
    SECTION_OF_REGISTRATION_GIFT = (By.XPATH, "//div[@class='form-group registrationGiftsWrapper'] ")