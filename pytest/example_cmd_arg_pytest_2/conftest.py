''' Конфигурация тестовых сценариев'''

def pytest_addoption(parser):
  parser.addoption("--param_1", action="store", default="test_1")
  parser.addoption("--param_2", action="store", default="test_2")
  parser.addoption("--param_3", action="store", default="test_3")

def pytest_generate_tests(metafunc):
  # This is called for every test. Only get/set command line arguments
  # if the argument is specified in the list of test "fixturenames".
  option_value = metafunc.config.option.param1
  if 'param1' in metafunc.fixturenames and option_value is not None:
    param_list = option_value.split(',')
    metafunc.parametrize("param_1", param_list)

  option_value = metafunc.config.option.param2
  if 'param2' in metafunc.fixturenames and option_value is not None:
    param_list = option_value.split(',')
    metafunc.parametrize("param_2", param_list)

  option_value = metafunc.config.option.param3
  if 'param3' in metafunc.fixturenames and option_value is not None:
    metafunc.parametrize("param_3", (option_value, ))
