# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

from selenium.webdriver.support.wait import WebDriverWait

from Auth import Url, Login, Password

CAPTCHA_ELEMENT = expected_conditions.presence_of_element_located((By.ID, "recaptcha-anchor-label"))
DELAY = 3

class CaptchaTestCase(unittest.TestCase):
    """
    Test chaecked  captch functionality

    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.fullscreen_window()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled_test_case(self):

        # start browser and got to hipp
        driver = self.driver
        driver.get(f'https://{Login.HIPP_U}:{Password.HIPP_P}@{Url.HIPP_DEV}')

        # click on icon account
        try:
            driver.find_element_by_xpath("//span[contains(@class,'kkicon kkicon-account')]").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(1)
        # click on 'Zaloguj' button
        try:
            driver.find_element_by_link_text("Zaloguj").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try first type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("Pah@dla.pl")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("t")

        # try to login
        try:
            driver.find_element_by_xpath("//button[@name='login']").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try second type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("ddd@ss.pl")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("testfnx")

        # try to login
        try:
            driver.find_element_by_xpath("//button[@name='login']").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try third type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("ktq@da.pl")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("test"+Keys.ENTER)

        # try to login
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # check is captcha visible
        try:
            self.assertEqual("Nie jestem robotem", driver.find_element_by_id("recaptcha-anchor-label").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # click on checkbox in captcha
        try:
            WebDriverWait(driver, DELAY).until(CAPTCHA_ELEMENT)
            driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # click on 'login' button
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # check is login facebook button is visible
        try:
            self.assertEqual("Zaloguj się przez facebook", driver.find_element_by_class_name("loginBtn--facebook").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try again type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("fnx@gmail.com")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("ktqG")

        # try to login
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # check is captcha visible
        try:
            self.assertEqual("Nie jestem robotem", driver.find_element_by_id("recaptcha-anchor-label").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # click on checkbox in captcha
        try:
            driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # click on 'login' button
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # check is login facebook button is visible
        try:
            self.assertEqual("Zaloguj się przez facebook", driver.find_element_by_class_name("loginBtn--facebook").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
