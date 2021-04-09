#!/bin/bash

echo --------------------------------
echo Пример передачи параметров при запуске pytest
echo --------------------------------
echo ----- Запуск по умолчанию ------
pytest test_sample.py -vs
sleep 1
echo --------------------------------
list_arg='type1 type2 type3'
for item in $list_arg; do
    echo -- Запуск с параметром: $item --
    pytest test_sample.py --cmdopt=$item -vs
    sleep 1
done
