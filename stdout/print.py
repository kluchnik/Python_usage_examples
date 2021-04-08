#!/usr/bin/python3
'''
-------------------- Пример использования ключей для вывода в stdout --------------------
ver.1.1
--------------------
'''
import sys

def print_example(name, syntax, txt):
    print('name:\t{}'.format(name))
    print('syntax:\t{}'.format(syntax))
    print('result:\n{}'.format(txt))
    print('--------------------')

def example_1_newline():
    name = 'Newline'
    syntax = '\'test-1\\ntest-2\\ntest-3\''
    txt = 'test-1\ntest-2\ntest-3'
    print_example(name, syntax, txt)

def example_2_htab():
    name = 'Horizontal tab'
    syntax = '\'test-1\\ttest-2\\ttest-3\''
    txt = 'test-1\ttest-2\ttest-3'
    print_example(name, syntax, txt)

def example_3_vtab():
    name = 'Vertical tab'
    syntax = '\'test-1\\vtest-2\\vtest-3\''
    txt = 'test-1\vtest-2\vtest-3'
    print_example(name, syntax, txt)

def example_4_backspace():
    name = 'Backspace'
    syntax = '\'test-1\\b2\''
    txt = 'test-1\b2'
    print_example(name, syntax, txt)

def example_5_carriage_return():
    name = 'Carriage return'
    syntax = '\'test-1\\rtest-2\\rtest-3\''
    txt = 'test-1\rtest-2\rtest-3'
    print_example(name, syntax, txt)

if __name__ == '__main__':
    parameters = globals()
    print(parameters['__doc__'])
    for item in dir(sys.modules[__name__]):
        if 'example_' in item:
            exec('{}{}'.format(item, '()'))
