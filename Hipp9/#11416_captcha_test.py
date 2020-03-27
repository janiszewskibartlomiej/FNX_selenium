# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

from selenium.webdriver.support.wait import WebDriverWait

from Auth import Url, Login, Password


class CaptchaTestCase(unittest.TestCase):
    """
    Test chaecked  captch functionality

    Steps:

    1. Go to login page
    2. Try to login - first time
    3. Try to login - second time
    4. Try to login - third time
    5. Verifying is captcha show
    6. Try accept captcha
    7. Try to go login page
    8. Verifying is captcha show after one incorect login
    9. Try accept captcha
    10. Try to go login page
    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # self.driver = webdriver.Chrome('C:/Users/janis/PycharmProjects/FNX_selenium/Driver/chromedriver.exe',
        #                                chrome_options=options)
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
        driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("test" + Keys.ENTER)

        # try to login
        try:
            driver.find_element_by_name("login").click()
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # check is captcha visible
        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='g-recaptcha]'")))
            # print(driver.find_element_by_xpath("//div[@class='g-recaptcha']"))
            self.assertEqual("reCAPTCHA", driver.find_element_by_xpath("//div[@class='g-recaptcha']"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # verifying current url
        try:
            current_url = driver.current_url
            self.assertEqual(current_url, Url.HIPP_VAL)
            # print(current_url)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # click on checkbox in captcha
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//div[@class='g-recaptcha']").click()
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
            self.assertEqual("reCAPTCHA", driver.findElement(By.xpath("//div[@class='content_element']//img")))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # click on checkbox in captcha
        try:
            # WebDriverWait(driver, DELAY).until(CAPTCHA_ELEMENT)
            driver.findElement(By.xpath("//div[@class='content_element']//img").click())
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        time.sleep(2)
        # click on 'login' button
        try:
            self.driver.find_element_by_name("login").click()
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
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
