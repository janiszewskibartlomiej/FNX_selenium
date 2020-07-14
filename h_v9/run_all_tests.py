import sys
import unittest
from datetime import date
import HtmlTestRunner

import tests.suite_all_tests_chrome as suiteAllTestsChrome
import tests.suite_all_tests_firefox as suiteAllTestsFireFox
import tests.suite_all_tests_ie as suiteAllTests_IE
from resources.test_data import Staging

if __name__ == '__main__':
    current_date = date.today()
    current_date_template = str(current_date).replace('-', '')

    suite = unittest.TestSuite()
    suite_chrome = suiteAllTestsChrome.suite()
    suite_firefox = suiteAllTestsFireFox.suite()
    suite_ie = suiteAllTests_IE.suite()
    suite.addTests(suite_chrome)
    suite.addTests(suite_firefox)
    suite.addTests(suite_ie)

    domain = Staging.DOMAIN

    report_title = f'Test Results of {domain} in Chrome & FF & IE'

    domain_strip = domain[:14]
    if domain_strip[-1] == '-':
        domain_strip = domain_strip[:13]
    report_name = domain_strip + "-AllBrowsers"

    runner = HtmlTestRunner.HTMLTestRunner(output='reports/' + current_date_template, combine_reports=True,
                                           report_title=report_title, report_name=report_name, verbosity=2,
                                           failfast=False, descriptions=True, buffer=False)
    runner.run(suite)
