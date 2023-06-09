import pytest

def pytest_addoption(parser):
  parser.addoption("--time", action="store_true")

@pytest.fixture()
def perf_time(request):
  time_value = request.config.option.time
  if not time_value:
    pytest.skip()
  return time_value
