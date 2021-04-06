#!/usr/bin/python3

import sys


def example_exc_1():
    '''
	The exception the return code 0 to the operating system (echo $?) and the exception msg to the stdout
    '''
    try:
        print(1/0)
    except Exception as exc:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error:', exc)
        print('----- info -----')
        print('Type exc:', exc_type.__name__)
        print('Message exc:', exc_obj)
        print('File exc:', exc_traceback.tb_frame.f_code.co_filename)
        print('Component exc:', exc_traceback.tb_frame.f_code.co_name)
        print('line exc:', exc_traceback.tb_lineno)
        print('----------------')

def example_exc_2():
    '''
	The exception the return code 1 to the operating system (echo $?) and the exception body to the stderr
    '''
    try:
        print(1/0)
    except Exception as exc:
        _, _, exc_traceback = sys.exc_info()
        raise Exception('error:', exc).with_traceback(exc_traceback) from None

if __name__=='__main__':
    arg = sys.argv
    if len(arg) == 1:
        print('Run this script with the parameter: example.py 1|2')
    elif arg[1] == '1':
        print('example exception 1')
        example_exc_1()
    elif arg[1] == '2':
        print('example exception 2')
        example_exc_2()
    else:
        print('Incorrect parameter, use the one parameter as in the example: example.py 1|2')
