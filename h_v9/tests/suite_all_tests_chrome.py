import unittest

from resources.automation_methods import AutomationMethods
from tests.test_11419_add_baby_successful_chrome import AddBabySuccessTestCase
from tests.test_1412_login_failure_chrome import LoginFailureTestCase
from tests.test_1412_login_successful_chrome import LoginSuccessTestCase
from tests.test_1416_captcha_chrome import CaptchaTestCase as CaptchaChrome


# root_path = os.path.abspath("../resources")
# root_path2 = os.path.abspath("../resources/page_object")
#
# print(sys.path)
# sys.path.append(root_path)
# sys.path.append(root_path2)
# print(sys.path)


def suite():
    suite = unittest.TestSuite()

    # Login page tests
    suite.addTest(LoginSuccessTestCase("test_TS01_TC001_successful_login_with_username"))
    suite.addTest(LoginSuccessTestCase("test_TS01_TC002_successful_login_with_email"))
    suite.addTest(LoginSuccessTestCase("test_TS01_TC003_successful_login_with_email_capitalizer"))
    suite.addTest(LoginSuccessTestCase("test_TS01_TC009_successful_login_with_facebook"))

    suite.addTest(LoginFailureTestCase("test_TS01_TC004_failed_login_correct_email_and_incorrect_password"))
    suite.addTest(LoginFailureTestCase("test_TS01_TC005_failed_login_incorrect_email_and_correct_password"))
    suite.addTest(LoginFailureTestCase("test_TS01_TC006_failed_login_correct_email_and_password_with_space_key"))
    suite.addTest(LoginFailureTestCase("test_TS01_TC007_failed_login_email_and_password_are_left_blank"))
    suite.addTest(LoginFailureTestCase("test_TS01_TC008_failed_login_reverse_data_input"))

    # Captcha tests
    suite.addTest(CaptchaChrome("test_TS02_TC001_captcha_is_visible_after_three_times_incorect_login"))
    suite.addTest(CaptchaChrome("test_TS02_TC002_captcha_is_visible_again_after_one_times_incorect_login"))
    suite.addTest(
        CaptchaChrome("test_TS02_TC003_captcha_is_visible_after_three_times_incorrect_login_total_quantity"))

    # Add baby
    suite.addTest(AddBabySuccessTestCase("test_TS03_TC001_successful_adding_pregnancy_with_no_gender"))
    suite.addTest(AddBabySuccessTestCase("test_TS03_TC002_successful_adding_pregnancy_with_female"))
    suite.addTest(AddBabySuccessTestCase("test_TS03_TC003_successful_adding_pregnancy_with_male"))
    suite.addTest(AddBabySuccessTestCase("test_TS03_TC004_successful_adding_baby_born_with_male"))
    suite.addTest(AddBabySuccessTestCase("test_TS03_TC005_successful_adding_baby_born_with_female"))

    return suite


if __name__ == '__main__':
    automation_of_tests = AutomationMethods()
    automation_of_tests.removing_directories_in_reports_by_number_of_day(n_day=7)

    suite = suite()

    runner = automation_of_tests.html_test_runner_report()
    runner.run(suite)
