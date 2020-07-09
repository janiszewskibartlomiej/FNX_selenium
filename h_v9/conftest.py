import os
from datetime import datetime, date
from py.xml import html
import pytest

render_collapsed = True


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


def pytest_html_report_title(report):
    report.title = "pytest Hipp9 report on staging"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("foo: bar")])

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#
#     timestamp = datetime.now().strftime('%H-%M-%S')
#
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if report.when == 'call':
#
#         feature_request = item.funcargs['request']
#
#         current_date = date.today()
#         current_date_template = str(current_date).replace('-', '')
#
#         driver = feature_request.getfixturevalue('browser')
#         path = f"./reports/{current_date_template}/scr{timestamp}.png"
#         driver.save_screenshot(path)
#
#         root = os.getcwd().replace("\\", "/")
#         absolute_path_to_screenshot = root + path[1:]
#
#         extra.append(pytest_html.extras.image(absolute_path_to_screenshot))

        # always add url to report
        # extra.append(pytest_html.extras.url('http://www.example.com/'))
        # xfail = hasattr(report, 'wasxfail')
        # if (report.skipped and xfail) or (report.failed and not xfail):
        #     # only add additional html on failure
        #     extra.append(pytest_html.extras.image(absolute_path_to_screenshot))
        #     extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        # report.extra = extra