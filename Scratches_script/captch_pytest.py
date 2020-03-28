# -*- coding: utf-8 -*-
import pytest
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


#
# class CaptchaTestCase(unittest.TestCase):
#     """
#     Test chaecked  captch functionality
#
#     """
@pytest.fixture(autouse=True, name='driver')
def setUp():
    driver = webdriver.Firefox()
    driver.fullscreen_window()
    # self.driver.maximize_window()
    driver.implicitly_wait(30)
    # self.base_url = "https://www.google.com/"
    verificationErrors = []
    accept_next_alert = True
    driver.get(f'https://{Login.HIPP_U}:{Password.HIPP_P}@{Url.HIPP_DEV}')


# @pytest.fixture()
# def setup_driver(setUp):
# driver = self.driver


# def test_go_to_page(self):
#
#     # start browser and go to hipp
#
def test_click_icon_account(driver):
    # click on icon account
    try:
        driver.find_element_by_xpath("//span[contains(@class,'kkicon kkicon-account')]").click()
    except AssertionError as e:
        driver.verificationErrors.append(str(e))


time.sleep(1)

#
# def test_click_zaloguj(self):
#     # click on 'Zaloguj' button
#     try:
#         driver.find_element_by_link_text("Zaloguj").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# time.sleep(1)
#
#
# def test_try_first_time_to_login(self):
#     # try first type of login and password
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("Pah@dla.pl")
#
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("t")
#
#     # try to login
#     try:
#         self.driver.find_element_by_xpath("//button[@name='login']").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# time.sleep(1)
#
#
# def test_try_second_time_to_login(self):
#     # try second type of login and password
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("ddd@ss.pl")
#
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("testfnx")
#
#     # try to login
#     try:
#         self.driver.find_element_by_xpath("//button[@name='login']").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     time.sleep(1)
#
#
# def test_try_third_time_to_login(self):
#     # try third type of login and password
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("ktq@da.pl")
#
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("test" + Keys.ENTER)
#
#     # try to login
#     try:
#         self.driver.find_element_by_name("login").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     time.sleep(2)
#
#
# def test_captcha_first_time(self):
#     # check is captcha visible
#     try:
#         self.assertEqual("Nie jestem robotem", self.driver.find_element_by_id("recaptcha-anchor-label").text)
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     # click on checkbox in captcha
#     try:
#         # WebDriverWait(self.driver, DELAY).until(CAPTCHA_ELEMENT)
#         self.driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     time.sleep(2)
#
#     # click on 'login' button
#     try:
#         self.driver.find_element_by_name("login").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# def test_login_page_is_visible_after_captcha_use(self):
#     # check is login facebook button is visible => login page is visible
#     try:
#         self.assertEqual("Zaloguj się przez facebook",
#                          self.driver.find_element_by_class_name("loginBtn--facebook").text)
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     time.sleep(1)
#
#
# def test_try_to_login_after_captach_use(self):
#     # try again type of login and password
#
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").clear()
#     self.driver.find_element_by_xpath("//input[@placeholder='Login']").send_keys("fnx@gmail.com")
#
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").clear()
#     self.driver.find_element_by_xpath(u"//input[@placeholder='Hasło']").send_keys("ktqG")
#
#     # try to login
#     try:
#         self.driver.find_element_by_name("login").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# time.sleep(2)
#
#
# def test_captcha_second_time_after_incorect_login(self):
#     # check is captcha visible
#     try:
#         self.assertEqual("Nie jestem robotem", self.driver.find_element_by_id("recaptcha-anchor-label").text)
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     # click on checkbox in captcha
#     try:
#         self.driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#     time.sleep(2)
#
#     # click on 'login' button
#     try:
#         self.driver.find_element_by_name("login").click()
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# def test_login_page_is_visible_after_captcha_use_second_time(self):
#     # check is login facebook button is visible => login page is visible
#     try:
#         self.assertEqual("Zaloguj się przez facebook",
#                          self.driver.find_element_by_class_name("loginBtn--facebook").text)
#     except AssertionError as e:
#         self.verificationErrors.append(str(e))
#
#
# def is_element_present(self, how, what):
#     try:
#         self.driver.find_element(by=how, value=what)
#     except NoSuchElementException as e:
#         return False
#     return True
#
#
# def tearDown(self):
#     self.driver.close()
#
#
# if __name__ == "__main__":
#     unittest.main()
