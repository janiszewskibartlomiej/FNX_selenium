# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import unittest, time, re

from Auth import Url, Login, Password


BY_FB_LOGIN = expected_conditions.presence_of_element_located((By.CLASS_NAME, "loginBtn--facebook"))


class CaptchaTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.fullscreen_window()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled_test_case(self):
        driver = self.driver
        driver.get(f'https://{Login.HIPP_U}:{Password.HIPP_P}@{Url.HIPP_DEV}')

        try:
            driver.find_element_by_xpath("//span[contains(@class,'kkicon kkicon-account')]").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(1)
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

        try:
            driver.find_element_by_xpath("//button[@name='login']").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try third type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("ktq@da.pl")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("test")

        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # browser = webdriver.Firefox()
        # browser.get("url")
        # print(driver.get("url"))
        # driver.get("https://hipp.fnx.group/logowanie/")
        try:
            CAPTCHA_ELEMENT = expected_conditions.presence_of_element_located((By.ID, "recaptcha-anchor-label"))
            DELAY = 3
            WebDriverWait(driver, DELAY).until(CAPTCHA_ELEMENT)
            self.assertEqual("Nie jestem robotem", driver.find_element_by_id("recaptcha-anchor-label").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # try again type of login and password
        time.sleep(1)
        driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
        driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("fnx@gmail.com")

        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("ktqG")

        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        print(driver.get("url"))
        driver.get()
        try:
            WebDriverWait(driver, DELAY).until(CAPTCHA_ELEMENT)
            self.assertEqual("Nie jestem robotem", driver.find_element_by_id("recaptcha-anchor-label").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            WebDriverWait(driver, DELAY).until(BY_FB_LOGIN)
            self.assertEqual("Logowanie", driver.find_element_by_class_name("loginBtn--facebook").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        print(self.verificationErrors)

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
