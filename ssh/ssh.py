'''
--------------------
Модуль для выполнения ssh-команд:
--------------------
import ssh

ssh_c = ssh.Commands()
ssh_parameters = {'ip':'127.0.0.1', 'port':'22', 'login':'user', 'password':'12345678'}
ssh_c.set_parameters(**ssh_parameters)

command = 'for ((i=1;i<=3;i++)); do echo $i; sleep 1; done'

_ = ssh_c.connect()
ssh_c.command_daemon(command)
stdin, stdout, stderr = ssh_c.get_line_stdin(), ssh_c.get_line_stdout(), ssh_c.get_line_stderr()
print('ssh-stdin:\\n{}\\nssh-stdout:\\n{}\\nssh-stderr:\\n{}'.format(stdin, stdout, stderr))
ssh_c.command(command)
stdin, stdout, stderr = ssh_c.get_line_stdin(), ssh_c.get_line_stdout(), ssh_c.get_line_stderr()
print('ssh-stdin:\\n{}\\nssh-stdout:\\n{}\\nssh-stderr:\\n{}'.format(stdin, stdout, stderr))
_ = ssh_c.disconnect()

result = ssh_c.command_script(command, 'test script')
print(result)

command = 'date; whoami; pwd'
result = ssh_c.command_script(command, 'test script')
print(result)

command = ['date', 'whoami', 'pwd']
result = ssh_c.command_script(command, 'test script')
print(result)

command = \'\'\'
date
whoami
pwd
\'\'\'
result = ssh_c.command_script(command, 'test script')
print(result)
--------------------
'''

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

import paramiko


class Commands():
    ''' Удаленое выполнение ssh-команд'''
    def __init__(self):
        self.__ssh = paramiko.SSHClient()
        self.__parameters = {
            'ip': '127.0.0.1',
            'port': '22',
            'username': 'user',
            'password': '12345678'}
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
            self.__ssh.connect(self.__parameters['ip'], username=self.__parameters['username'], password=self.__parameters['password'])
            return True
        except:
            return False

    def disconnect(self):
        ''' Обрыв соединения по ssh '''
        if self.__ssh:
            self.__ssh.close()

    def command_daemon(self, cmd):
        ''' Выполнение команды без вывода '''
        _, _, _ = self.__ssh.exec_command(cmd)

    def command(self, cmd):
        ''' Выполнение команды '''
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(cmd)
            self.set_line_stdin(ssh_stdin)
            self.set_line_stdout(ssh_stdout)
            self.set_line_stderr(ssh_stderr)
        except:
            self.set_line_stdin([''])
            self.set_line_stdout([''])
            self.set_line_stderr(['ошибка подключения'])

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
