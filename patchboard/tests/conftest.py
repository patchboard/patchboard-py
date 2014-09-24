import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default='localhost', help="specify the url of test host (scheme is optional and defaults to http, port is optional and defaults to 80)")

@pytest.fixture(scope=u'session')
def api_url(request):
    url = request.config.getoption('--host')
    return u'http://' + url if u'://' not in url else url
