import sys
import os
import unittest
from datetime import date
import HtmlTestRunner
from tests.test_1412LoginSuccessfulFireFox import LoginSuccessTestCase as  LoginSuccessFireFox
from tests.test_1412LoginFailureFireFox import LoginFailureTestCase as LoginFailureFireFox
from tests.test_1416CaptchaFireFox import CaptchaTestCase as CaptchaFireFox
from resources.test_data import Dev, Staging


def suite():
    suite = unittest.TestSuite()

    # Login page tests
    suite.addTest(LoginSuccessFireFox('test_TS01_TC001_successful_login_with_username'))
    suite.addTest(LoginSuccessFireFox('test_TS01_TC002_successful_login_with_email'))
    suite.addTest(LoginSuccessFireFox('test_TS01_TC003_successful_login_with_email_capitalizer'))
    suite.addTest(LoginSuccessFireFox('test_TS01_TC009_successful_login_with_facebook'))

    suite.addTest(LoginFailureFireFox('test_TS01_TC004_failed_login_correct_email_and_incorrect_password'))
    suite.addTest(LoginFailureFireFox('test_TS01_TC005_failed_login_incorrect_email_and_correct_password'))
    suite.addTest(LoginFailureFireFox('test_TS01_TC006_failed_login_correct_email_and_password_with_space_key'))
    suite.addTest(LoginFailureFireFox('test_TS01_TC007_failed_login_email_and_password_are_left_blank'))
    suite.addTest(LoginFailureFireFox('test_TS01_TC008_failed_login_reverse_data_input'))

    # Captcha tests
    suite.addTest(CaptchaFireFox('test_TS02_TC001_captcha_is_visible_after_three_times_incorect_login'))
    suite.addTest(CaptchaFireFox('test_TS02_TC002_captcha_is_visible_again_after_one_times_incorect_login'))
    suite.addTest(CaptchaFireFox('test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity'))

    return suite


if __name__ == '__main__':
    current_date = date.today()
    current_date_template = str(current_date).replace('-', '')

    suite = suite()

    domain = Staging.DOMAIN

    report_title = f'Test Results of {domain}'

    domain_strip = domain[:14]
    if domain_strip[-1] == '-':
        domain_strip = domain_strip[:13]
    report_name = domain_strip + "-FireFox"

    runner = HtmlTestRunner.HTMLTestRunner(output='../reports/' + current_date_template, combine_reports=True,
                                           report_title=report_title, report_name=report_name, verbosity=2,
                                           failfast=False, descriptions=True, buffer=False)
    runner.run(suite)
