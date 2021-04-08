'''
-------------------- Модуль для выполнения ssh-команд --------------------
ver.2.1
Пример использования:
--------------------
import ssh

ssh_ = ssh.Commands()
ssh_parameters = {'ip':'127.0.0.1', 'port':'22', 'login':'user', 'password':'12345678'}
ssh_.set_parameters(**ssh_parameters)

command = 'for ((i=1;i<=3;i++)); do echo $i; sleep 1; done'

print('SSH status: {}'.format(ssh_.get_status_connect()))
_ = ssh_.connect()
print('SSH status: {}'.format(ssh_.get_status_connect()))
ssh_.command_daemon(command)
stdin, stdout, stderr = ssh_.get_line_stdin(), ssh_.get_line_stdout(), ssh_.get_line_stderr()
print('ssh-stdin:\\n{}\\nssh-stdout:\\n{}\\nssh-stderr:\\n{}'.format(stdin, stdout, stderr))
ssh_.command(command)
stdin, stdout, stderr = ssh_.get_line_stdin(), ssh_.get_line_stdout(), ssh_.get_line_stderr()
print('ssh-stdin:\\n{}\\nssh-stdout:\\n{}\\nssh-stderr:\\n{}'.format(stdin, stdout, stderr))
ssh_.disconnect()

result = ssh_.command_script(command, 'test script')
ssh_.get_status_connect()
print('SSH status: {}'.format(ssh_.get_status_connect()))
print(result)

command = 'date; whoami; pwd'
result = ssh_.command_script(command, 'test script')
print('SSH status: {}'.format(ssh_.get_status_connect()))
print(result)

command = ['date', 'whoami', 'pwd']
result = ssh_.command_script(command, 'test script')
print('SSH status: {}'.format(ssh_.get_status_connect()))
print(result)

command = \'\'\'
date
whoami
pwd
\'\'\'
result = ssh_.command_script(command, 'test script')
print('SSH status: {}'.format(ssh_.get_status_connect()))
print(result)
--------------------
'''

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

import paramiko


class Commands():
    ''' Удаленое выполнение ssh-команд '''
    def __init__(self):
        self.__ssh = paramiko.SSHClient()
        self.__parameters = {
            'ip': '127.0.0.1',
            'port': '22',
            'username': 'user',
            'password': '12345678'}
        self.__status_connect = None
        self.__line_stdin = None
        self.__line_stdout = None
        self.__line_stderr = None

    def set_password(self, password):
        ''' Задать пароль '''
        self.__parameters['password'] = password

    def set_username(self, username):
        ''' Вернуть пароль '''
        self.__parameters['username'] = username

    def set_ip(self, ip):
        ''' Задать ip-адрес '''
        self.__parameters['ip'] = ip

    def set_port(self, port):
        ''' Задать ssh-порт '''
        self.__parameters['port'] = port

    def set_parameters(self, **kwarg):
        '''
        Задать новое значение параметрам подключения:
        example-1: <class>.set_parameters(ip='192.168.1.11', login='root', password='12345678')
        example-2: <class>.set_parameters(**{'ip':'192.168.1.11', 'login':'root', 'password':'12345678'})
        '''
        for item in kwarg.keys():
            self.__parameters[item] = kwarg[item]

    def get_parameters(self):
        ''' Вернуть параметры '''
        return self.__parameters

    def get_status_connect(self):
        ''' Вернуть статус соединения '''
        return self.__status_connect

    def get_password(self):
        ''' Вернуть пароль '''
        return self.__parameters['password']

    def get_username(self):
        ''' Вернуть имя пользователя '''
        return self.__parameters['username']

    def get_ip(self):
        ''' Вернуть ip-адрес '''
        return self.__parameters['ip']

    def get_port(self):
        ''' Вернуть ssh-порт '''
        return self.__parameters['port']

    def get_line_stdin(self):
        ''' Вернуть ввод команды через ssh '''
        return self.__line_stdin

    def get_line_stdout(self):
        ''' Вернуть вывод команды через ssh '''
        return self.__line_stdout

    def get_line_stderr(self):
        ''' Вернуть ошибки команды через ssh '''
        return self.__line_stderr

    def set_line_stdin(self, ssh_stdin):
        ''' Задать значение ввода команды ssh '''
        try:
            self.__line_stdin = ssh_stdin.read().decode('utf-8').split('\n')
        except:
            pass

    def set_line_stdout(self, ssh_stdout):
        ''' Задать значение вывода команды через ssh '''
        try:
            self.__line_stdout = ssh_stdout.read().decode('utf-8').split('\n')
        except:
            pass

    def set_line_stderr(self, ssh_stderr):
        ''' Задать значение ошибки команды через ssh '''
        try:
            self.__line_stderr = ssh_stderr.read().decode('utf-8').split('\n')
        except:
            pass

    def connect(self):
        ''' Соединение по ssh '''
        try:
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(hostname=self.__parameters['ip'], port=int(self.__parameters['port']),
                               username=self.__parameters['username'], password=self.__parameters['password'])
            self.__status_connect = 'Ок'
            return True
        except Exception as exc:
            self.__status_connect = 'Ошибка подключения по ssh: {}'.format(exc)
            return False

    def disconnect(self):
        ''' Разрыв соединения по ssh '''
        if self.__ssh:
            self.__ssh.close()

    def command_daemon(self, cmd):
        ''' Выполнение ssh-команды без вывода '''
        _, _, _ = self.__ssh.exec_command(cmd)

    def command(self, cmd):
        ''' Выполнение ssh-команды '''
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(cmd)
            self.set_line_stdin(ssh_stdin)
            self.set_line_stdout(ssh_stdout)
            self.set_line_stderr(ssh_stderr)
        except Exception as exc:
            self.set_line_stdin([''])
            self.set_line_stdout([''])
            self.set_line_stderr(['Ошибка {}, при выполнении ssh-команды: {}'.format(exc, cmd)])

    def command_script(self, script, name='description'):
        messange = '--------------\n{}:\n--------------'.format(name)
        if isinstance(script, str):
            if self.connect():
                self.command(script)
                messange += '\n#: {}'.format(script)
                messange += '\n> out:\n{}'.format('\n'.join(self.__line_stdout))
                messange += '> error:\n{}'.format('\n'.join(self.__line_stderr))
                self.disconnect()
        elif isinstance(script, tuple) or isinstance(script, list):
            if self.connect():
                for item in script:
                    self.command(item)
                    messange += '\n#: {}'.format(item)
                    messange += '\n> out:\n{}'.format('\n'.join(self.__line_stdout))
                    messange += '> error:\n{}'.format('\n'.join(self.__line_stderr))
                self.disconnect()
        else:
            messange += ('\nОшибка выполнения сценария:\n{}'.format(script))
        return messange

if __name__ == '__main__':
    print('Даннный файл представляет собой модуль для использования в python')
    parameters = globals()
    print(parameters['__doc__'])
