import unittest

import tests.suite_all_tests_chrome as suiteAllTestsChrome
import tests.suite_all_tests_firefox as suiteAllTestsFireFox
import tests.suite_all_tests_ie as suiteAllTests_IE
from resources.automation_methods import AutomationMethods

if __name__ == '__main__':
    automation_of_tests = AutomationMethods()

    suite = unittest.TestSuite()
    suite_chrome = suiteAllTestsChrome.suite()
    suite_firefox = suiteAllTestsFireFox.suite()
    suite_ie = suiteAllTests_IE.suite()
    suite.addTests(suite_chrome)
    suite.addTests(suite_firefox)
    suite.addTests(suite_ie)

    runner = automation_of_tests.html_test_runner_report()
    runner.run(suite)
