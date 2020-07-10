import inspect
import time
import unittest
import random
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.color import Color
from resources.page_object.add_baby_page import AddBabyPage
from resources.locators import HomePageLocators, LoginPageLocators, AddBabyLocators
from resources.test_data import CommonData, Staging


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

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_DAY) is True
            random_day = self.add_baby_page.get_random_number()
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_DAY))
            day_select.select_by_value(random_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_MONTH))
            next_month_number = self.add_baby_page.get_month_number(add_number=1)
            month_select.select_by_value(next_month_number)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_YEAR))
            year_select.select_by_value(self.current_year)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert 'Wyrażam zgodę na:' in self.add_baby_page.driver.page_source

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.ADD_BABY_BUTTON)
            time.sleep(3)
            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=AddBabyLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.NAME_UNKNOWN,
                                                   element_text='Imię nieznane')
            assert 'Imię nieznane' in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text='Potwierdź datę urodzenia dziecka')
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert 'Potwierdź datę urodzenia dziecka' in self.add_baby_page.driver.page_source

            date_of_birth = f"{random_day}.{next_month_number}.{self.current_year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=AddBabyLocators.DATE_OF_BIRTH).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.NO_GENDER_TEXT,
                                                   element_text='Płeć: Nieznana')
            assert 'Płeć: Nieznana' in self.add_baby_page.get_element(by_locator=AddBabyLocators.NO_GENDER_TEXT).text
            assert 'Nieznana' in self.add_baby_page.driver.page_source

            assert 'NIE' in self.add_baby_page.get_element(by_locator=AddBabyLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: NIE')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise

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

            no_gender_radio = Color.from_string(
                self.driver.find_element(*AddBabyLocators.FEMALE).value_of_css_property(
                    'color'))
            assert no_gender_radio.hex == '#ff0000'

            self.add_baby_page.click_on(by_loctor=AddBabyLocators.FEMALE)

            assert 'Pole jest wymagane' in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(AddBabyLocators.ALERT_MESSAGE) is True

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_DAY) is True
            current_day = self.add_baby_page.get_random_number(today=True)
            day_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_DAY))
            day_select.select_by_value(current_day)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_MONTH) is True
            month_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_MONTH))
            current_month = self.add_baby_page.get_month_number()
            month_select.select_by_value(current_month)

            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.BORN_YEAR) is True
            year_select = Select(self.add_baby_page.get_element(by_locator=AddBabyLocators.BORN_YEAR))
            year_select.select_by_value(self.current_year)

            assert self.add_baby_page.element_is_visible(
                by_locator=AddBabyLocators.SECTION_OF_REGISTRATION_GIFT) is True
            assert 'Wyrażam zgodę na:' in self.add_baby_page.driver.page_source

            name = 'Oliwia'
            self.add_baby_page.enter_text_and_click_enter(by_locators=AddBabyLocators.FIRST_NAME, text=name)
            time.sleep(3)

            self.add_baby_page.assert_path_in_current_url(path='/profil-uzytkownika/lista-dzieci')

            assert self.add_baby_page.element_is_visible(by_locator=AddBabyLocators.IMG_STORK) is True
            assert 'img alt="Ciąża' in self.add_baby_page.driver.page_source

            assert 'Imię nieznane' not in self.add_baby_page.driver.page_source

            assert name in self.add_baby_page.driver.page_source
            assert self.add_baby_page.element_is_visible(
                by_locator=(By.XPATH, f"//h2[contains(text(), '{name}')]")) is True

            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.CONFIRM_DATE_OF_BIRTH_LINK,
                                                   element_text='Potwierdź datę urodzenia dziecka')
            assert self.add_baby_page.is_clickable(by_locator=AddBabyLocators.CONFIRM_DATE_OF_BIRTH_LINK) is True
            assert 'Potwierdź datę urodzenia dziecka' in self.add_baby_page.driver.page_source

            date_of_birth = f"{current_day}.{current_month}.{self.current_year}"
            assert date_of_birth == self.add_baby_page.get_element(by_locator=AddBabyLocators.DATE_OF_BIRTH).text
            assert date_of_birth in self.add_baby_page.driver.page_source

            gender_text = 'Płeć: Dziewczynka'
            self.add_baby_page.assert_element_text(by_locator=(By.XPATH, f"//div[contains(text(), '{gender_text[6:]}')]"),
                                                   element_text=gender_text)
            assert gender_text[6:] in self.add_baby_page.driver.page_source
            assert 'Nieznana' not in self.add_baby_page.driver.page_source

            assert 'NIE' in self.add_baby_page.get_element(by_locator=AddBabyLocators.GIFT_FOR_CHILDBIRTH_INFO).text
            self.add_baby_page.assert_element_text(by_locator=AddBabyLocators.GIFT_FOR_CHILDBIRTH_INFO,
                                                   element_text='Paczka Narodziny: NIE')


        except:
            self.add_baby_page.do_screenshot(
                name=inspect.stack()[0][-3][:44] + inspect.stack()[0][1][-9:-3] + '_')
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
