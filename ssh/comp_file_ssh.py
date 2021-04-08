'''
-------------------- Модуль для удаленного сравнения файлов через ssh --------------------
ver.2.1
Пример использования:
--------------------
import comp_file_ssh

comp_file_ssh_ = comp_file_ssh.Comparison()
comp_file_ssh_.get_parameters()
comp_file_ssh_.delete_pc_parameters('pc2')
comp_file_ssh_.get_parameters()
comp_file_ssh_.clear_parameters()
comp_file_ssh_.get_parameters()

parameters_pc1 = {'ip': '192.168.1.11', 'port': '22', 'username': 'root', 'password': '12345678', 'directory': '/tmp'}
parameters_pc2 = {'ip': '192.168.1.12', 'port': '22', 'username': 'root', 'password': '12345678', 'directory': '/tmp'}
parameters_pc1 = {'ip': '127.0.0.1', 'port': '22', 'username': 'user', 'password': '12345678', 'directory': '/tmp/test1'}
parameters_pc2 = {'ip': '127.0.0.1', 'port': '22', 'username': 'user', 'password': '12345678', 'directory': '/tmp/test2'}
parameters = {'pc1': parameters_pc1, 'pc2': parameters_pc2}
comp_file_ssh_.set_parameters(**parameters)
comp_file_ssh_.get_parameters()

comp_file_ssh_.get_report()

--------------------
'''
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

import paramiko

class Comparison():
    ''' Удаленое сравнение файлов на компьютерах по ssh '''
    def __init__(self):
        self.__ssh = paramiko.SSHClient()
        self.__parameters = {
            'pc1': {
                'ip': '127.0.0.1',
                'port': '22',
                'username': 'user',
                'password': '12345678',
                'directory': '/tmp'},
            'pc2': {
                'ip': '127.0.0.1',
                'port': '22',
                'username': 'user',
                'password': '12345678',
                'directory': '/tmp'}
            }
        self.__status_connect = {}
        self.__line_stdout = {}
        self.__line_stderr = {}
        self.__extra_param = ''
        self.__check_md5sum = False
        self.__file_list = {'out': {}, 'error': {}}

    def clear_parameters(self):
        ''' Очистка параметров для удаленного подключения  '''
        self.__parameters = {}

    def delete_pc_parameters(self, name_pc):
        ''' Удаление всех параметров для удаленного компьютера '''
        _ = self.__parameters.pop(name_pc, None)

    def set_parameters(self, **kwarg):
        '''
        Задать новое значение параметрам подключения:
        parameters_pc1 = {'ip': '192.168.1.11', 'port': '22', 'username': 'root', 'password': '12345678', 'directory': '/tmp'}
        parameters_pc2 = {'ip': '192.168.1.12', 'port': '22', 'username': 'root', 'password': '12345678', 'directory': '/tmp'}
        example-1: <object>.set_parameters(pc1 = parameters_pc1, pc2 = parameters_pc2)
        example-2: <object>.set_parameters(**{'pc1': parameters_pc1, 'pc2': parameters_pc2})
        '''
        for name_pc in kwarg.keys():
            for item in kwarg[name_pc].keys():
                if name_pc not in self.__parameters.keys():
                    self.__parameters[name_pc] = {}
                self.__parameters[name_pc][item] = kwarg[name_pc][item]

    def get_parameters(self):
        ''' Вернуть параметры '''
        return self.__parameters

    def get_status_connect(self):
        ''' Вернуть статус соединения '''
        return self.__status_connect

    def set_line_stdout(self, name_pc, ssh_stdout):
        ''' Задать значения вывода ssh-команды '''
        try:
            self.__line_stdout[name_pc] = ssh_stdout.read().decode('utf-8')
        except:
            pass

    def set_line_stderr(self, name_pc, ssh_stderr):
        ''' Задать значения ошибки ssh-команды '''
        try:
            self.__line_stderr[number_pc] = ssh_stderr.read().decode('utf-8')
        except:
            pass

    def get_line_stdout(self):
        ''' Вернуть вывод выолнение ssh-команды '''
        return self.__line_stdout

    def get_line_stderr(self):
        ''' Вернуть ошибку выполнение ssh-команды '''
        return self.__line_stderr

    def set_extra_param(self, param=''):
        '''
           Установить дополнительные параметры для поиска файлов
           Например для изменения глубины поиска можно использовать параметр <object>.set_extra_param('-maxdepth 1')
        '''
        self.__extra_param = param

    def get_extra_param(self):
        ''' Вернуть дополнительный параметр для поиска файлов '''
        return self.__extra_param

    def set_check_md5sum(self, status=False):
        ''' Установить провеку КС для файлов по алгоритму md5 '''
        self.__check_md5sum = status

    def get_check_md5sum(self):
        ''' Вернуть статус провеку КС для файлов по алгоритму md5 '''
        return self.__check_md5sum

    def check_connect_param(self, pc_name):
        ''' Проверка наличие всех параметов для соединения к компьютеру '''
        check_list = ['ip', 'port', 'username', 'password', 'directory']
        for item in check_list:
            if item not in self.__parameters[pc_name].keys():
                self.__status_connect[pc_name] = 'Не хватает параметров для подключения по ssh: {}'.format(self.__parameters[pc_name])
                return False
        return True

    def connect(self, pc_name):
        ''' Соединение по ssh '''
        if self.check_connect_param(pc_name):
            try:
                pc_parameters = self.__parameters[pc_name]
                self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.__ssh.connect(hostname=pc_parameters['ip'], port=int(pc_parameters['port']),
                                   username=pc_parameters['username'], password=pc_parameters['password'])
                self.__status_connect[pc_name] = 'Ок'
                return True
            except Exception as exc:
                self.__status_connect[pc_name] = 'Ошибка подключения по ssh: {}'.format(exc)
                return False

    def disconnect(self):
        ''' Разрыв соединения по ssh '''
        if self.__ssh:
            self.__ssh.close()

    def command(self, pc_name, cmd):
        ''' Выполнение ssh-команды '''
        try:
            ssh_stdin, ssh_stdout, ssh_stderr = self.__ssh.exec_command(cmd)
            self.set_line_stdout(pc_name, ssh_stdout)
            self.set_line_stderr(pc_name, ssh_stderr)
        except Exception as exc:
            self.set_line_stdout(pc_name, [''])
            self.set_line_stderr(pc_name,['Ошибка {}, при выполнении ssh-команды: {}'.format(exc, cmd)])

    def get_file_status(self):
        ''' Подключение по ssh и сбор информации о файлах '''
        if self.__check_md5sum:
            cmd = '''
                echo -e 'File:\tSize:\tModify:\tMD5sum:'
                find {0} {1} -type f -not -name ".*" -exec bash -c '
                    stat --printf="%N\t%s\t%y\t" "$1";
                    md5=($(md5sum -b "$1"));
                    echo -ne "$md5\n";
                ' excec-sh {{}} ';'
            '''
        else:
            cmd = '''
                echo -e 'File:\tSize:\tModify:\tMD5sum:'
                find {0} {1} -type f -not -name ".*" -exec bash -c '
                    stat --printf="%N\t%s\t%y\t" "$1";
                    echo -ne "-\n";
                ' excec-sh {{}} ';'
            '''
        # Подключение к компьютерам для сбора информации
        for pc_name in self.__parameters.keys():
            if self.connect(pc_name):
                directory = self.__parameters[pc_name]['directory']
                self.command(pc_name, cmd.format(directory, self.__extra_param))
                self.disconnect()

    def create_file_list(self):
        ''' Создать таблицу сравнения файлов '''
        pc_name_list = self.__line_stdout.keys()
        # Проходим по всем компьютерам с которых собрали информацию о файлах
        for pc_name in pc_name_list:
            # Структурируем информацию
            for item in self.__line_stdout[pc_name].split('\n')[1:-1]:
                data = item.split('\t')
                try:
                    file_name = data[0][1:-1]
                    if file_name:
                        # Если в отчете отсутсвует ключ с именм файла, то мы его создаем
                        if file_name not in self.__file_list['out'].keys():
                            self.__file_list['out'][file_name] = {}
                        # Если для компьютеров не задано значения параметор файла, то мы зполняем его пустым значением
                        for pc_name_check in pc_name_list:
                            if pc_name_check not in self.__file_list['out'][file_name].keys():
                                self.__file_list['out'][file_name][pc_name_check] = ('-', '-', '-')
                        # Обновляем значения параметров для заданного файла расположенного на конкретном компьютере
                        self.__file_list['out'][file_name][pc_name] = (data[1], data[2], data[3])
                except Exception as exc:
                    self.__file_list['error']['parsing'] += 'pc: {}, data: {}, msg_error: {}\n'.format(pc_name, data, exc)
            if pc_name in self.__file_list['error'].keys():
                self.__file_list['error'][pc_name] = self.__line_stderr[pc_name]

    def get_report(self, mode='all'):
        '''
           Сгенерировать итоговый отчет
           :parm mode - вывод отчета, допустимые значения 'all'|'match'|'diff'
               all - все файлы
               match - тоько совпадающие файлы
               diff - только отличающиеся файлы
        '''
        if mode == 'all':
            mode_txt = 'все файлы'
        elif mode == 'match':
            mode_txt = 'тоько совпадающие файлы'
        elif mode == 'diff':
            mode_txt = 'тоько совпадающие файлы'
        else:
            mode_txt = "Не корректно задан режим проверки файлов, используйте один из параметров <object>.get_report(mode='all'|'match'|'diff')"
        self.get_file_status()
        self.create_file_list()
        try:
            messange = '---------------------------------\n'
            messange += 'Статус соединения по ssh:\n'
            for pc_name in self.__status_connect.keys():
                messange += '\t{}: {}\n'.format(pc_name, self.__status_connect[pc_name])
            messange += '---------------------------------\n'
            messange += 'Сравнение файлов на двух компьютерах\n'
            messange += '({})\n'.format(mode_txt)
            messange += '-------------- out --------------\n'
            for file_name in self.__file_list['out'].keys():
                data = self.__file_list['out'][file_name]
                if mode == 'all':
                    messange += 'File: {}\n'.format(file_name)
                    for pc_name in data.keys():
                        messange += '\t{}: {}\t{}\t{}\n'.format(pc_name, data[pc_name][0], data[pc_name][1], data[pc_name][2])
                elif mode == 'match':
                    size = ()
                    md5sum = ()
                    for pc_name in data.keys():
                        size += (data[pc_name][1], )
                        md5sum += (data[pc_name][2], )
                    if len(set(size)) == 1 and len(set(md5sum)) == 1:
                        messange += 'File: {}\n'.format(file_name)
                        for name_pc in data.keys():
                            messange += '\t{}: {}\t{}\t{}\n'.format(pc_name, data[pc_name][0], data[pc_name][1], data[pc_name][2])
                elif mode == 'diff':
                    size = ()
                    md5sum = ()
                    for pc_name in data.keys():
                        size += (data[pc_name][1], )
                        md5sum += (data[pc_name][2], )
                    if len(set(size)) != 1 or len(set(md5sum)) != 1:
                        messange += 'File: {}\n'.format(file_name)
                        for name_pc in data.keys():
                            messange += '\t{}: {}\t{}\t{}\n'.format(pc_name, data[pc_name][0], data[pc_name][1], data[pc_name][2])
            messange += '------------- error -------------\n'
            for item in self.__file_list['error'].keys():
                messange += '\t{}:\n{}'.format(item, '\n'.join(self.__file_list['error'][item]))
            messange += '---------------------------------\n'
        except Exception as exc:
            messange += '---------------------------------\n'
            messange = 'Ошибка генерации отчета: {}'.format(exc)
            messange += '---------------------------------\n'
            messange = 'Ошибка генерации для данных:\n{}'.format(self.__file_list)
            messange += '---------------------------------\n'
        return messange

if __name__ == '__main__':
    print('Даннный файл представляет собой модуль для использования в python')
    parameters = globals()
    print(parameters['__doc__'])
