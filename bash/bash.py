'''
--------------------
Модуль для выполнения bash команд в консоли:
--------------------
import bash

bash_c = bash.Commands()
command = 'for ((i=1;i<=3;i++)); do echo $i; sleep 1; done'

bash_c.process(command)

bash_c.command(command)
stdin, stdout, stderr = bash_c.get_line_stdin(), bash_c.get_line_stdout(), bash_c.get_line_stderr()
print('stdin:\\n{}\\nstdout:\\n{}\\nstderr:\\n{}'.format(stdin, stdout, stderr))

result = bash_c.command_script(command, 'test script')
print(result)

command = 'date; whoami; pwd'
result = bash_c.command_script(command, 'test script')
print(result)

command = ['date', 'whoami', 'pwd']
result = bash_c.command_script(command, 'test script')
print(result)

command = \'\'\'
date
whoami
pwd
\'\'\'
result = bash_c.command_script(command, 'test script')
print(result)
--------------------
'''
import subprocess


class Commands():
    ''' Выполнение bash-команд '''
    def __init__(self):
        self.__line_stdin = None
        self.__line_stdout = None
        self.__line_stderr = None

    def get_line_stdin(self):
        ''' Вернуть bash-ввод sdtin '''
        return self.__line_stdin

    def get_line_stdout(self):
        ''' Вернуть bash-вывод stdout '''
        return self.__line_stdout

    def get_line_stderr(self):
        ''' Вернуть bash-ошибка sterr '''
        return self.__line_stderr

    def process(self, command):
        ''' Выполнение bash-команды с выводом в консоль '''
        try:
            proc = subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(proc.stdout.readline, b''):
                print(">>>", line.rstrip().decode('utf-8'))
        except:
            print ('error run bash.process command: %s' %(command))

    def command(self, cmd):
        ''' Выполнение bash-команды '''
        try:
            dialog = subprocess.Popen(['/bin/bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = dialog.communicate()
            self.__line_stdin = cmd
            self.__line_stdout = out.decode('utf-8')
            self.__line_stderr = error.decode('utf-8')
        except:
            self.__line_stdin = cmd
            self.__line_stdout = ''
            self.__line_stderr = 'ошибка выполнения'

    def command_script(self, script, name='description'):
        ''' Выполнение bash-команд с выводом '''
        messange = '--------------\n{}:\n--------------'.format(name)
        if isinstance(script, str):
            self.command(script)
            messange += '\n#: {}'.format(script)
            messange += '\n> out:\n{}'.format(self.__line_stdout)
            messange += '> error:\n{}'.format(self.__line_stderr)
        elif isinstance(script, tuple) or isinstance(script, list):
            for item in script:
                self.command(item)
                messange += '\n#: {}'.format(item)
                messange += '\n> out:\n{}'.format(self.__line_stdout)
                messange += '> error:\n{}'.format(self.__line_stderr)
        else:
            messange += ('\nОшибка выполнения сценария:\n{}'.format(script))
        return messange
