import inspect
import time
import unittest
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.select import Select

from resources.locators import AddBabyLocators, ListOfChildrenLocators
from resources.page_object.add_baby_page import AddBabyPage
from resources.test_data import CommonData


class AddBabySuccessTestCaseBase(unittest.TestCase):
    """
        Test of  Add baby functionality -  Success

        """

    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(CommonData.CHROME_PATH, options=chrome_options)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()


class AddBabySuccessTestCase(AddBabySuccessTestCaseBase):

    def setUp(self):
        super().setUp()
        self.add_baby_page = AddBabyPage(self.driver)
        self.add_baby_url = '/profil-uzytkownika/dodaj-dziecko'
        self.current_year = date.today().year.__str__()

    @unittest.skip('I must creating method to delete children in my user')
    def test_TS03_TC001_successful_adding_pregnancy_with_no_gender(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)
            pregnant_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.I_AM_PREGNANT).value_of_css_property('color'))
            assert pregnant_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            no_gender_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.NO_GENDER_RADIO).value_of_css_property(
                    'color'))
            assert no_gender_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.NO_GENDER_RADIO)

            assert 'Pole jest wymagane' in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            future_date = self.add_baby_page.get_date_from_delta_n_day(add_days=60)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            future_day = future_date["day"]
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_DAY))
            day_select.select_by_value(future_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_MONTH))
            future_month = future_date["month"]
            month_select.select_by_value(future_month)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_YEAR))
            year = future_date["year"]
            year_select.select_by_value(year)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert 'Wyrażam zgodę na:' in self.add_baby_page.driver.page_source

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            alert_text = 'Prawidłowo dodano nowe dziecko'
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' in self.add_baby_page.driver.page_source

            first_name = 'Imię nieznane'
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER,
                                                   element_text=first_name)
            assert first_name in self.add_baby_page.driver.page_source
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text='Potwierdź datę urodzenia dziecka')
            assert self.add_baby_page.is_clickable(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert 'Potwierdź datę urodzenia dziecka' in self.add_baby_page.driver.page_source

            date_of_birth = f"{future_day}.{future_month}.{year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION,
                                                   element_text='Płeć: Nieznana')
            assert 'Płeć: Nieznana' in self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.GENDER_SECTION).text
            assert 'Nieznana' in self.add_baby_page.driver.page_source

            assert 'NIE' in self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: NIE')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise


    @unittest.skip('I must creating method to delete children in my user')
    def test_TS03_TC002_successful_adding_pregnancy_with_female(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)
            pregnant_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.I_AM_PREGNANT).value_of_css_property('color'))
            assert pregnant_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            gender_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.FEMALE).value_of_css_property(
                    'color'))
            assert gender_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.FEMALE)

            assert 'Pole jest wymagane' in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            current_day = self.add_baby_page.get_random_number(today=True)
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_DAY))
            day_select.select_by_value(current_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_MONTH))
            current_month = self.add_baby_page.get_month_number()
            month_select.select_by_value(current_month)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_YEAR))
            year_select.select_by_value(self.current_year)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert 'Wyrażam zgodę na:' in self.add_baby_page.driver.page_source

            path = self.add_baby_page.get_path_from_name(file_name='imiona_polskie.csv')
            name = self.add_baby_page.get_random_firstname_from_csv(path=path)
            self.add_baby_page.enter_text_and_click_enter(by_locators=AddBabyLocators.FIRST_NAME_INPUT, text=name)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            alert_text = 'Prawidłowo dodano nowe dziecko'
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' in self.add_baby_page.driver.page_source

            assert 'Imię nieznane' not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER, element_text=name)

            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text='Potwierdź datę urodzenia dziecka')
            assert self.add_baby_page.is_clickable(by_locator=ListOfChildrenLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert 'Potwierdź datę urodzenia dziecka' in self.add_baby_page.driver.page_source

            date_of_birth = f"{current_day}.{current_month}.{self.current_year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            gender_text = 'Płeć: Dziewczynka'
            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION, element_text=gender_text)
            assert gender_text[6:] in self.add_baby_page.driver.page_source
            assert 'Nieznana' not in self.add_baby_page.driver.page_source

            assert 'NIE' in self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: NIE')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise

    @unittest.skip
    def test_TS03_TC003_successful_adding_pregnancy_with_male(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)
            pregnant_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.I_AM_PREGNANT).value_of_css_property('color'))
            assert pregnant_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_AM_PREGNANT)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            gender_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.MALE).value_of_css_property(
                    'color'))
            assert gender_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.MALE)

            assert 'Pole jest wymagane' in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            future_date = self.add_baby_page.get_date_from_delta_n_day(add_days=270)
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_DAY) is True
            future_day = future_date["day"]
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_DAY))
            day_select.select_by_value(future_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_MONTH))
            future_month = future_date["month"]
            month_select.select_by_value(future_month)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.PREGNANT_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.PREGNANT_YEAR))
            future_year = future_date["year"]
            year_select.select_by_value(future_year)

            path = self.add_baby_page.get_path_from_name(file_name='imiona_polskie.csv')
            name = self.add_baby_page.get_random_firstname_from_csv(path=path)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.FIRST_NAME_INPUT, text=name)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            gift_section = self.add_baby_page.get_element(by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT)
            assert 'Wyrażam zgodę na:' in gift_section.get_attribute('innerText')
            assert '/klub-maluszka/moj-klub-maluszka/' in gift_section.get_attribute('innerHTML')
            self.add_baby_page.click_on(by_loctor=AddBabyLocators.CHECKBOX_GIFT_TEXT)
            time.sleep(3)

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.NAME_IN_TRIANGLE, element_text=name)

            post_code_and_town_name = self.add_baby_page.get_random_post_code_and_town_name_from_csv()
            path_street = self.add_baby_page.get_path_from_name(file_name='spis-ulic-w-gdansku.csv')
            street_name = self.add_baby_page.get_random_street_name_from_csv(path=path_street)
            street_number = self.add_baby_page.get_random_street_number()
            phone_nunber = self.add_baby_page.get_random_phone_number()

            self.add_baby_page.enter_text(by_locator=AddBabyLocators.TOWN_NAME,
                                          text=post_code_and_town_name['town_name'])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.STREET_NAME, text=street_name)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.NUMBER_OF_STREET, text=street_number)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.POST_CODE,
                                          text=post_code_and_town_name['post_code'])
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.PHONE_NUMBER, text=phone_nunber)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            alert_text = 'Prawidłowo dodano nowe dziecko'
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT,
                                                   element_text=alert_text)

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' in self.add_baby_page.driver.page_source

            assert 'Imię nieznane' not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert name == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER).text
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.NAME_IN_TRIANGLE, element_text=name)

            assert 'Potwierdź datę urodzenia dziecka' not in self.add_baby_page.driver.page_source

            date_of_birth = f"{future_day}.{future_month}.{future_year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_REGULAR).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            gender_text = 'Płeć: Chłopiec'
            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION, element_text=gender_text)
            assert gender_text[6:] in self.add_baby_page.driver.page_source
            assert 'Nieznana' not in self.add_baby_page.driver.page_source

            assert 'TAK' in self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: TAK')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise


    def test_TS03_TC004_successful_adding_baby_born_with_male(self):
        try:
            self.add_baby_page.assert_path_in_current_url(path=self.add_baby_url)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)
            pregnant_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.I_HAVE_BABY).value_of_css_property('color'))
            assert pregnant_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.I_HAVE_BABY)
            time.sleep(3)

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            gender_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.MALE).value_of_css_property(
                    'color'))
            assert gender_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.MALE)

            assert 'Pole jest wymagane' in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            past_date = self.add_baby_page.get_date_from_delta_n_day(add_days=-1095)
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_DAY) is True
            past_day = past_date["day"]
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_DAY))
            day_select.select_by_value(past_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_MONTH))
            past_month = past_date["month"]
            month_select.select_by_value(past_month)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_YEAR))
            past_year = past_date["year"]
            year_select.select_by_value(past_year)

            path = self.add_baby_page.get_path_from_name(file_name='imiona_polskie.csv')
            name = self.add_baby_page.get_random_firstname_from_csv(path=path)
            self.add_baby_page.enter_text(by_locator=AddBabyLocators.FIRST_NAME_INPUT, text=name)

            assert self.add_baby_page.element_is_not_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_ICON) is True
            assert self.add_baby_page.element_is_visible(by_locator=ListOfChildrenLocators.ALERT_CONTENT) is True
            alert_text = 'Prawidłowo dodano nowe dziecko'
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.ALERT_CONTENT, element_text=alert_text)

            assert self.add_baby_page.element_is_not_visible(by_locator=ListOfChildrenLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' not in self.add_baby_page.driver.page_source

            assert 'Imię nieznane' not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert name == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.FIRST_NAME_RENDER).text
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True

            assert 'Potwierdź datę urodzenia dziecka' not in self.add_baby_page.driver.page_source

            date_of_birth = f"{past_day}.{past_month}.{past_year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_BOLD).text
            assert date_of_birth in self.add_baby_page.driver.page_source
            date_of_birth_element = self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.DATE_OF_BIRTH_BOLD)
            font_weight = date_of_birth_element.value_of_css_property('font-weight')
            assert font_weight == '700'

            gender_text = 'Płeć: Chłopiec'
            self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//div[contains(text(), '{gender_text[6:]}')]"))
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GENDER_SECTION, element_text=gender_text)
            assert gender_text[6:] in self.add_baby_page.driver.page_source
            assert 'Nieznana' not in self.add_baby_page.driver.page_source

            assert 'NIE' in self.add_baby_page.get_element(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=ListOfChildrenLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: NIE')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
