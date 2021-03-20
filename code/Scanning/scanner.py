#!/bin/python
# This tool is designed purely from an educational standpoint. 
# Port scanning can be used to study the internet, and help security
# researchers identify machines on the internet that are vulnerable 
# to ongoing attacks or already compromised by one. 
from threading import Thread 
import multiprocessing
import socket 
import utils
import time 
import sys 
import os 


def check_args():
	options = {'targets': [],
	}
	if len(sys.argv)<2:
		print('Usage: python scanner.py ip/hostname options')
		exit()
	if 3 > len(sys.argv) >= 2:
		# check if user gave an IP Address
		if len(sys.argv[1].split('.'))>=4 and int(sys.argv[1].split('.')[0]):
			ip = sys.argv[1]
			options['targets'].append(ip)
		else: # User has given a hostname (ex. google.com)
			c = "host %s | grep 'has address' | cut -d ' ' -f 4" % sys.argv[1]
			addr = utils.cmd(c, False)
			if len(addr) == 1:
				options['targets'].append(addr.pop(0))
			else:
				for a in addr:
					options['targets'].append(addr.pop())	
	elif len(sys.argv) > 2 and '-file' in sys.argv:
		for addr in utils.swap(sys.argv[-1], False):
			options['targets'].append(addr)
	# remove any duplicate addresses
	options['targets'] = list(set(options['targets']))
	return options


def scan_thread(target, port, verbose):
	results = {}
	results['target'] = target
	ports = {'ftp': 21, 'ssh': 22, 'smtp': 25, 
			 'dns': 53, 'http': 80, 'http-proxy':8080,
			 'rdp': 3389, 'socks': 1080} # Add more, just a quick list
	TIMEOUT = 5; n_open = 0
	for proto in ports.keys():
		port = ports[proto]
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				s.connect((target, port))
				results[proto] = 'OPEN'
				n_open += 1
			except socket.error:	 # closed or filtered
				results['state'] = 'CLOSED'
				pass
			s.close()
		except socket.error:
			print('[!] Unable to create socket')
			return False, {}
	results['ports_open'] = n_open
	return results

def parse_scan(results):
	head = '- %s has %d ports open |' % (results['target'], results['ports_open'])
	for i in results.keys():
		if results[i] == 'OPEN':
			head += '%s|' % i.upper()
	print(head)

def main():
	# Get the addresses to be scanned
	opts = check_args()
	# Start Scanning
	start_date, start_time = utils.create_timestamp()
	banner = '[*] Starting Scan of %d Hosts    %s - %s'
	print(banner % (len(opts['targets']), start_date, start_time))
	verbosity = False
	
	for ip in opts['targets']:
		pool = multiprocessing.Pool(5)
		scan = pool.apply_async(scan_thread, (ip, 22, False))
		try:
			ports = scan.get(timeout=3)
			parse_scan(ports)
		except multiprocessing.TimeoutError:
			pass


if __name__ == '__main__':
	main()
