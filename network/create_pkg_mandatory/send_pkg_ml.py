#!/usr/bin/python3
'''
Генерация и отправка сетевого пакета с мандатной метокой
'''

from sys import argv
import argparse
import re
import scapy.all as scapy

def create_parser():
	''' Парсинг параметров запуска приложения '''
	parser = argparse.ArgumentParser(description='Sending IP-packet with a mandatory label.')
	parser.add_argument('-src', '--src', default='192.168.4.100', help='source ip-address (ex. 192.168.4.100)')
	parser.add_argument('-dst', '--dst', default='192.168.6.100', help='destination ip-address (ex. 192.168.6.100)')
	parser.add_argument('-iface', '--iface', default='ens3', help='package send interface (ex. ens3)')
	parser.add_argument('-level', '--level', default=1, type=int, help='mandatory level dec (ex. 1)')
	parser.add_argument('-category', '--category', default='00000100', type=str, help='mandatory category bin (ex. 00000100)')
	parser.add_argument('-proto', '--proto', default=254, type=int, help='ip protocol dec (ex. 254)')
	return parser

def create_pkg_mandatory_label(src, dst, level, category, proto):
	'''
	Генерация пакета с мандатной меткой
	CLASSIFICATION LEVEL (Unclassiﬁed) = 0b1010101100000111 (0xab)
	Level = 1 => 0b00000011 (0x03)
	Level = 2 => 0b00000101 (0x05)
	Level = 3 => 0b00000111 (0x07)
	category = 1 => 0b00000100 (0x04)
	category = 2 => 0b00001000 (0x08)
	'''
	eth = scapy.Ether()
	eth.type = 0x800
	ip = scapy.IP()
	ip.proto = int(proto)
	ip.src = src
	ip.dst = dst
	security = scapy.IPOption_Security()
	security.copy_flag = 0b1
	security.optclass = 0b00
	security.option = 0b00010
	security.length = 0b00000101
	security.security = int('0b1010101100000000', 2) + 2*int(level) + 1
	security.compartment = int('0b' + re.search(r'[0,1]+', str(category)).group(0) + '00000000', 2)
	ip.options = security
	data = scapy.Raw(load='test messange level: {} category: {}'.format(level, category))
	return eth/ip/data

def main():
	parser = create_parser()
	arg_space = parser.parse_args(argv[1:])
	try:
		package = create_pkg_mandatory_label(src=arg_space.src, dst=arg_space.dst, level=arg_space.level,
							category=arg_space.category, proto=arg_space.proto)
		print(package.show())
	except Exception as e:
		print('-> packet formation error: {}'.format(e))
		exit(1)
	try:
		scapy.sendp(package, iface=arg_space.iface)
	except Exception as e:
		print('-> packet sending error: {}'.format(e))
		exit(1)

if __name__ == '__main__':
	main()
