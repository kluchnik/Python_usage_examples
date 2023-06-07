# Передача параметров в тестовую функцию

## Сценарий по умолчанию
```
pytest test_my.py -s
```
```
================================================ test session starts ================================================
platform linux -- Python 3.7.3, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/test
collected 1 item

test_my.py
start test function
test_1
test_2
test_3
stop test function
```
## Сценарий с одним параметром
```
pytest test_my.py -s --param_1 test_11,test_12
```
```
================================================ test session starts ================================================
platform linux -- Python 3.7.3, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/test
collected 2 items

test_my.py
start test function
test_11
test_2
test_3
stop test function
.
start test function
test_12
test_2
test_3
stop test function
.
```
## Сценарий с двумя параметрами
```
pytest test_my.py -s --param_1 test_11,test_12 --param_2 test_21,test_22
```
```
================================================ test session starts ================================================
platform linux -- Python 3.7.3, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/test
collected 4 items

test_my.py
start test function
test_11
test_21
test_3
stop test function
.
start test function
test_11
test_22
test_3
stop test function
.
start test function
test_12
test_21
test_3
stop test function
.
start test function
test_12
test_22
test_3
stop test function
.
```
