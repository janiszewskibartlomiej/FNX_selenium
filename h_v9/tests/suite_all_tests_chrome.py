import unittest
from datetime import date
import unittest
from datetime import date

import HtmlTestRunner

from resources.test_data import Staging
from tests.test_11419Add_babySuccessfulChrome import AddBabySuccessTestCase
from tests.test_1412_login_failure_chrome import LoginFailureTestCase
from tests.test_1412_login_successful_chrome import LoginSuccessTestCase
from tests.test_1416_captcha_chrome import CaptchaTestCase


# root_path = os.path.abspath('../resources')
# root_path2 = os.path.abspath('../resources/page_object')
#
# print(sys.path)
# sys.path.append(root_path)
# sys.path.append(root_path2)
# print(sys.path)


def suite():
    suite = unittest.TestSuite()

    # Login page tests
    suite.addTest(LoginSuccessTestCase('test_TS01_TC001_successful_login_with_username'))
    suite.addTest(LoginSuccessTestCase('test_TS01_TC002_successful_login_with_email'))
    suite.addTest(LoginSuccessTestCase('test_TS01_TC003_successful_login_with_email_capitalizer'))
    suite.addTest(LoginSuccessTestCase('test_TS01_TC009_successful_login_with_facebook'))

    suite.addTest(LoginFailureTestCase('test_TS01_TC004_failed_login_correct_email_and_incorrect_password'))
    suite.addTest(LoginFailureTestCase('test_TS01_TC005_failed_login_incorrect_email_and_correct_password'))
    suite.addTest(LoginFailureTestCase('test_TS01_TC006_failed_login_correct_email_and_password_with_space_key'))
    suite.addTest(LoginFailureTestCase('test_TS01_TC007_failed_login_email_and_password_are_left_blank'))
    suite.addTest(LoginFailureTestCase('test_TS01_TC008_failed_login_reverse_data_input'))

    # Captcha tests
    suite.addTest(CaptchaTestCase('test_TS02_TC001_captcha_is_visible_after_three_times_incorect_login'))
    suite.addTest(CaptchaTestCase('test_TS02_TC002_captcha_is_visible_again_after_one_times_incorect_login'))
    suite.addTest(CaptchaTestCase('test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity'))

    # Add baby
    suite.addTest(AddBabySuccessTestCase('test_TS03_TC001_successful_adding_pregnancy_with_no_gender'))
    suite.addTest(AddBabySuccessTestCase('test_TS03_TC002_successful_adding_pregnancy_with_female'))

    return suite


if __name__ == '__main__':
    current_date = date.today()
    current_date_template = str(current_date).replace('-', '')

    suite = suite()

    # domain = Dev.DOMAIN
    domain = Staging.DOMAIN

    report_title = f'Test Results of {domain}'

    domain_strip = domain[:14]
    if domain_strip[-1] == '-':
        domain_strip = domain_strip[:13]
    report_name = domain_strip + "-Chrome"

    runner = HtmlTestRunner.HTMLTestRunner(output='../reports/' + current_date_template, combine_reports=True,
                                           report_title=report_title, report_name=report_name, verbosity=2,
                                           failfast=False, descriptions=True, buffer=False)
    runner.run(suite)

    # concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(2))
    # runner.run(concurrent_suite)