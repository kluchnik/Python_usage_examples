#!/usr/bin/python3
'''
Генерация и отправка сетевого пакета с vlan
'''

from sys import argv
import argparse
import re
import scapy.all as scapy

def create_parser():
	''' Парсинг параметров запуска приложения '''
	parser = argparse.ArgumentParser(description='Sending IP-packet with a vlan.')
	parser.add_argument('-src', '--src', default='192.168.4.100', help='source ip-address (ex. 192.168.4.100)')
	parser.add_argument('-dst', '--dst', default='192.168.6.100', help='destination ip-address (ex. 192.168.6.100)')
	parser.add_argument('-iface', '--iface', default='ens3', help='package send interface (ex. ens3)')
	parser.add_argument('-vlan', '--vlan', default=1001, type=int, help='vlan id (ex. 1001)')
	parser.add_argument('-proto', '--proto', default=254, type=int, help='ip protocol dec (ex. 254)')
	return parser

def create_pkg_vlan(src, dst, vlan, proto):
	''' Генерация пакета с vlan id '''
	eth = scapy.Ether()
	eth.type = 0x8100
	vlan_pkg = scapy.Dot1Q()
	vlan_pkg.vlan = vlan
	ip = scapy.IP()
	ip.proto = int(proto)
	ip.src = src
	ip.dst = dst
	data = scapy.Raw(load='test vlan id: {}'.format(vlan))
	return eth/vlan_pkg/ip/data

def main():
	parser = create_parser()
	arg_space = parser.parse_args(argv[1:])
	try:
		package = create_pkg_mandatory_label(src=arg_space.src, dst=arg_space.dst, level=arg_space.vlan,
							proto=arg_space.proto)
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
