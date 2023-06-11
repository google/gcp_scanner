"""The module to parse and save params"""

import pytest

def pytest_addoption(parser):
  # TODO: add adoption for all command-line params
  parser.addoption("--time", action="store_true")

@pytest.fixture()
def perf_time(request):
  time_value = request.config.option.time
  if not time_value:
    pytest.skip()
  return time_value
