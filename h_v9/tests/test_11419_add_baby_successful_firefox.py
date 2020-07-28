import sys
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

from resources.automation_methods import AutomationMethods
from resources.locators import AddBabyLocators, ListOfChildrenLocators
from resources.page_object.add_baby_page import AddBabyPage


class AddBabySuccessTestCaseBase(unittest.TestCase):
    """
        Test of  Add baby functionality -  Success

        """

    def setUp(self) -> None:
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference('browser.cache.disk.enable', False)
        profile.set_preference('browser.cache.memory.enable', False)
        profile.set_preference('browser.cache.offline.enable', False)
        profile.set_preference('network.http.use-cache', False)
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')
        firefox_path = AutomationMethods().get_path_from_name(file_name="geckodriver.exe")
        self.driver = webdriver.Firefox(executable_path=firefox_path, firefox_profile=profile,
                                        options=firefox_options)
        # self.driver = webdriver.Remote(command_executor='http://192.168.8.103:5000/wd/hub', desired_capabilities= firefox_options.to_capabilities())
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()


class AddBabySuccessTestCase(AddBabySuccessTestCaseBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.automation_methods = AutomationMethods()
        self.add_baby_url = '/profil-uzytkownika/dodaj-dziecko'
        self.children_list_url = '/profil-uzytkownika/lista-dzieci'
        self.my_baby_club_url = '/klub-maluszka/moj-klub-maluszka/'
        self.alert_color = '#ff0000'
        self.required_field_text = "Pole jest wymagane"
        self.accept_text = "Wyrażam zgodę na:"
        self.correct_added_baby_alert_text = "Prawidłowo dodano nowe dziecko"
        self.img_stork = 'img alt="Ciąża"'
        self.no_name_text = "Imię nieznane"
        self.confirm_baby_born_date_text = "Potwierdź datę urodzenia dziecka"
        self.no_gender_text = "Płeć: Nieznana"
        self.female_gender_text = "Płeć: Dziewczynka"
        self.male_gender_text = "Płeć: Chłopiec"
        self.born_gift_text_no = "Paczka Narodziny: NIE"
        self.born_gift_text_yes = "Paczka Narodziny: TAK"

    def setUp(self):
        super().setUp()
        self.add_baby_page = AddBabyPage(self.driver)

    @unittest.skip("I must creating method to delete children in my user")
    def test_TS03_TC001_successful_adding_pregnancy_with_no_gender(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.I_AM_PREGNANT,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.NO_GENDER_RADIO,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.NO_GENDER_RADIO)

            assert self.required_field_text in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True

            future_date = self.add_baby_page.get_date_from_delta_n_day(add_days=60)
            future_day = future_date["day"]
            future_month = future_date["month"]
            year = future_date["year"]
            self.add_baby_page.select_date(day=future_day, month=future_month, year=year, pregnant=True)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert self.accept_text in self.add_baby_page.driver.page_source

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path=self.children_list_url)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=self.correct_added_baby_alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert self.img_stork in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER,
                                                   element_text=self.no_name_text)
            assert self.no_name_text in self.add_baby_page.driver.page_source
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text=self.confirm_baby_born_date_text)
            assert self.add_baby_page.is_clickable(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert self.confirm_baby_born_date_text in self.add_baby_page.driver.page_source

            date_of_birth = f"{future_day}.{future_month}.{year}"
            assert date_of_birth == self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text=self.no_gender_text)
            assert self.no_gender_text in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GENDER_SECTION).text
            assert self.no_gender_text[-8:] in self.add_baby_page.driver.page_source
            assert self.born_gift_text_no[-3:] in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text=self.born_gift_text_no)


        except:
            self.add_baby_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    @unittest.skip("I must creating method to delete children in my user")
    def test_TS03_TC002_successful_adding_pregnancy_with_female(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.I_AM_PREGNANT,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.FEMALE, color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.FEMALE)

            assert self.required_field_text in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True

            current_data = self.add_baby_page.get_date_from_delta_n_day(add_days=0)
            current_day = current_data["day"]
            current_month = current_data["month"]
            current_year = current_data["year"]
            self.add_baby_page.select_date(day=current_day, month=current_month, year=current_year, pregnant=True)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert self.accept_text in self.add_baby_page.driver.page_source

            path = self.automation_methods.get_path_from_name(file_name="imiona_polskie.csv")
            name = self.add_baby_page.get_random_firstname_from_csv(path=path)
            self.add_baby_page.enter_text_and_click_enter(by_locators=AddBabyLocators.FIRST_NAME_INPUT, text=name)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path=self.children_list_url)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=self.correct_added_baby_alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert self.img_stork in self.add_baby_page.driver.page_source

            assert self.no_name_text not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER,
                                                   element_text=name)

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text=self.confirm_baby_born_date_text)
            assert self.add_baby_page.is_clickable(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert self.confirm_baby_born_date_text in self.add_baby_page.driver.page_source

            date_of_birth = f"{current_day}.{current_month}.{current_year}"
            assert date_of_birth == self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{self.female_gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text=self.female_gender_text)
            assert self.female_gender_text[6:] in self.add_baby_page.driver.page_source
            assert self.no_gender_text[-8:] not in self.add_baby_page.driver.page_source

            assert self.born_gift_text_no[-3:] in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text=self.born_gift_text_no)


        except:
            self.add_baby_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    @unittest.skip("I must creating method to delete children in my user")
    def test_TS03_TC003_successful_adding_pregnancy_with_male(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.I_AM_PREGNANT,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.MALE, color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.MALE)

            assert self.required_field_text in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            # W dniu wprowadzania daty, data musi się znajdować się w przedziale od  1 do 270 dni
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True

            future_date = self.add_baby_page.get_date_from_delta_n_day(add_days=270)
            future_day = future_date["day"]
            future_month = future_date["month"]
            future_year = future_date["year"]
            self.add_baby_page.select_date(day=future_day, month=future_month, year=future_year, pregnant=True)

            path_of_name = self.automation_methods.get_path_from_name(file_name="imiona_polskie.csv")
            name = self.add_baby_page.get_random_firstname_from_csv(path=path_of_name)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.FIRST_NAME_INPUT, text=name)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            gift_section = self.add_baby_page.get_element(by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT)
            assert self.accept_text in gift_section.get_attribute('innerText')
            assert self.my_baby_club_url in gift_section.get_attribute('innerHTML')
            self.add_baby_page.click_on(by_loctor=AddBabyLocators.CHECKBOX_GIFT_TEXT)
            time.sleep(3)

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.NAME_IN_TRIANGLE, element_text=name)

            path_of_post_code_and_town_name = self.automation_methods.get_path_from_name(file_name="kody.csv")
            post_code_and_town_name = self.add_baby_page.get_random_post_code_and_town_name_from_csv(
                path=path_of_post_code_and_town_name)
            path_street = self.automation_methods.get_path_from_name(file_name="spis-ulic-w-gdansku.csv")
            street_name = self.add_baby_page.get_random_street_name_from_csv(path=path_street)
            street_number = self.add_baby_page.get_random_street_number()
            phone_nunber = self.add_baby_page.get_random_phone_number()

            self.add_baby_page.enter_text(by_locator=AddBabyLocators.TOWN_NAME,
                                          text=post_code_and_town_name["town_name"])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.STREET_NAME, text=street_name)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.NUMBER_OF_STREET, text=street_number)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.POST_CODE,
                                          text=post_code_and_town_name["post_code"])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.PHONE_NUMBER, text=phone_nunber)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path=self.children_list_url)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=self.correct_added_baby_alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert self.img_stork in self.add_baby_page.driver.page_source

            assert self.no_name_text not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert name == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER).text
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.NAME_IN_TRIANGLE,
                                                   element_text=name)

            assert self.confirm_baby_born_date_text not in self.add_baby_page.driver.page_source

            date_of_birth = f"{future_day}.{future_month}.{future_year}"
            assert date_of_birth == self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{self.male_gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text=self.male_gender_text)
            assert self.male_gender_text[6:] in self.add_baby_page.driver.page_source
            assert self.no_gender_text[-8:] not in self.add_baby_page.driver.page_source

            assert self.born_gift_text_yes[-3:] in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text=self.born_gift_text_yes)


        except:
            self.add_baby_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    @unittest.skip("I must creating method to delete children in my user")
    def test_TS03_TC004_successful_adding_baby_born_with_male(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)
            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.I_HAVE_BABY,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_HAVE_BABY)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.MALE, color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.MALE)

            assert self.required_field_text in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            # Data nie może być z przyszłości oraz nie może być starsza niż 1093 dni
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_DAY) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_YEAR) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_MONTH) is True

            past_date = self.add_baby_page.get_date_from_delta_n_day(add_days=-1095)
            past_day = past_date["day"]
            past_month = past_date["month"]
            past_year = past_date["year"]
            self.add_baby_page.select_date(day=past_day, month=past_month, year=past_year, pregnant=False)

            name_path = self.automation_methods.get_path_from_name(file_name="imiona_polskie.csv")
            name = self.add_baby_page.get_random_firstname_from_csv(path=name_path)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.FIRST_NAME_INPUT, text=name)

            assert self.add_baby_page.element_is_not_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path=self.children_list_url)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=self.correct_added_baby_alert_text)

            assert self.add_baby_page.element_is_not_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert self.img_stork not in self.add_baby_page.driver.page_source

            assert self.no_name_text not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert name == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER).text
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True

            assert self.confirm_baby_born_date_text not in self.add_baby_page.driver.page_source

            date_of_birth = f"{past_day}.{past_month}.{past_year}"
            assert date_of_birth == self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_BOLD).text
            assert date_of_birth in self.add_baby_page.driver.page_source
            date_of_birth_element = self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_BOLD)
            font_weight = date_of_birth_element.value_of_css_property('font-weight')
            assert font_weight == '700'

            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{self.male_gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text=self.male_gender_text)
            assert self.male_gender_text[6:] in self.add_baby_page.driver.page_source
            assert self.no_gender_text[-8:] not in self.add_baby_page.driver.page_source

            assert self.born_gift_text_no[-3] in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text=self.born_gift_text_no)


        except:
            self.add_baby_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise

    def test_TS03_TC005_successful_adding_baby_born_with_female(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.I_HAVE_BABY,
                                                        color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_HAVE_BABY)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            self.add_baby_page.assert_element_color_hex(by_locator=AddBabyLocators.FEMALE, color_hex=self.alert_color)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.FEMALE)

            assert self.required_field_text in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            # Paczkę narodzin mogą otrzymać dzieci < 46 dni oraz każda ciążą
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_DAY) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_MONTH) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_YEAR) is True

            past_date_sub_47 = self.add_baby_page.get_date_from_delta_n_day(add_days=-47)
            past_day_sub_47 = past_date_sub_47["day"]
            past_month_sub_47 = past_date_sub_47["month"]
            past_year_sub_47 = past_date_sub_47["year"]
            self.add_baby_page.select_date(day=past_day_sub_47, month=past_month_sub_47, year=past_year_sub_47,
                                           pregnant=False)

            assert self.add_baby_page.element_is_not_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True

            past_date_sub_46 = self.add_baby_page.get_date_from_delta_n_day(add_days=-46)
            past_day_sub_46 = past_date_sub_46["day"]
            past_month_sub_46 = past_date_sub_46["month"]
            past_year_sub_46 = past_date_sub_46["year"]
            self.add_baby_page.select_date(day=past_day_sub_46, month=past_month_sub_46, year=past_year_sub_46,
                                           pregnant=False)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            gift_section = self.add_baby_page.get_element(by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT)
            assert self.accept_text in gift_section.get_attribute('innerText')
            assert self.my_baby_club_url in gift_section.get_attribute('innerHTML')
            self.add_baby_page.click_on(by_loctor=AddBabyLocators.CHECKBOX_GIFT_TEXT)
            time.sleep(3)

            name_path = self.automation_methods.get_path_from_name(file_name="imiona_polskie.csv")
            name = self.add_baby_page.get_random_firstname_from_csv(path=name_path)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.FIRST_NAME_INPUT, text=name)

            post_code_and_town_name_path = self.automation_methods.get_path_from_name("kody.csv")
            post_code_and_town_name = self.add_baby_page.get_random_post_code_and_town_name_from_csv(
                path=post_code_and_town_name_path)
            street_path = self.automation_methods.get_path_from_name(file_name="spis-ulic-w-gdansku.csv")
            street_name = self.add_baby_page.get_random_street_name_from_csv(path=street_path)
            street_number = self.add_baby_page.get_random_street_number()
            phone_nunber = self.add_baby_page.get_random_phone_number()

            self.add_baby_page.enter_text(by_locator=AddBabyLocators.TOWN_NAME,
                                          text=post_code_and_town_name["town_name"])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.STREET_NAME, text=street_name)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.NUMBER_OF_STREET, text=street_number)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.POST_CODE,
                                          text=post_code_and_town_name["post_code"])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.PHONE_NUMBER, text=phone_nunber)

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.NAME_IN_TRIANGLE, element_text=name)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path=self.children_list_url)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=self.correct_added_baby_alert_text)

            assert self.add_baby_page.element_is_not_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert self.img_stork not in self.add_baby_page.driver.page_source

            assert self.no_name_text not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert name == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER).text
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.NAME_IN_TRIANGLE,
                                                   element_text=name)

            date_of_birth = f"{past_day_sub_46}.{past_month_sub_46}.{past_year_sub_46}"
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_BOLD,
                                                   element_text=date_of_birth)
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text=self.female_gender_text)
            assert self.female_gender_text[6:] in self.add_baby_page.driver.page_source
            assert self.no_gender_text[-8:] not in self.add_baby_page.driver.page_source

            assert self.born_gift_text_yes[-3:] in self.add_baby_page.get_element(
                by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text=self.born_gift_text_yes)


        except:
            self.add_baby_page.do_screenshot(name=sys._getframe(0).f_code.co_name + __file__[-11:-3] + "_")
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
