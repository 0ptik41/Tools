#!/bin/python
# SSH_ENUM.py
import multiprocessing
import socket 
import json
import time 
import sys 
import os

def load_targets(fname):
	targets = []
	for ln in open(fname, 'r').readlines():
		targets.append(ln.replace('\n',''))
	return targets


def usage():
	print('$ %s target_list' % sys.argv[0])
	exit()

def scan(host):
	sshOpen = False
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, 22))
		s.close()
		sshOpen = True
	except socket.error:
		pass
		return sshOpen
	return sshOpen


def main():
	# check args 
	if len(sys.argv)<2:
		usage()

	# Load Host IPs for Scanning
	hosts = load_targets(sys.argv[1])
	print('[*] Scanning %d Hosts' % len(hosts))

	start = time.time()
	thread_pool = multiprocessing.Pool(15)
	try:
		for host in hosts:
			scan_thread = thread_pool.apply_async(scan, (host,))
			try:
				isOpen = scan_thread.get(timeout=2)
				if isOpen:
					print('\033[1m\033[32m[*] %s is running SSH \033[0m' % host)
				else:
					print('\033[1m\033[31m[*] %s is not running SSH \033[0m' % host)
			except multiprocessing.TimeoutError:
				pass
			
			
	except KeyboardInterrupt:
		print('[!] Killing Scan [%ss elapsed]'% str(time.time() - start))
		exit()
	print('[*] Scan Finished [%ss elapsed]' % str(time.time() - start))


if __name__ == '__main__':
	main()