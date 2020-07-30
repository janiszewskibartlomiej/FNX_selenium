import sys
import os
import unittest
import tests.suite_all_tests_chrome as suiteAllTestsChrome
import tests.suite_all_tests_firefox as suiteAllTestsFireFox
import tests.suite_all_tests_ie as suiteAllTests_IE
from resources.automation_methods import AutomationMethods

if __name__ == '__main__':
    automation_of_tests = AutomationMethods()
    automation_of_tests.removing_directories_in_reports_by_number_of_day(n_day=7)
    os.system("pytest --alluredir ./reports/allure_json -v")
    os.system("cd ./reports/HTML_reports")
    os.system("allure generate ./allure_json --clean")


    # suite = unittest.TestSuite()
    # suite_chrome = suiteAllTestsChrome.suite()
    # suite_firefox = suiteAllTestsFireFox.suite()
    # suite_ie = suiteAllTests_IE.suite()
    # suite.addTests(suite_chrome)
    # suite.addTests(suite_firefox)
    # suite.addTests(suite_ie)
    #
    # runner = automation_of_tests.html_test_runner_report()
    # runner.run(suite)
