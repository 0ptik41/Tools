import multiprocessing
import requests
import random
import time 
import sys 
import os

resources = {'pages':  '/usr/share/wfuzz/wordlist/general/common.txt',
			 'ext':	   '/usr/share/wfuzz/wordlist/webservices/ws-files.txt',
			 'unames': '/usr/share/wfuzz/wordlist/others/names.txt',
			 'passwd': '/usr/share/wfuzz/wordlist/others/common_pass.txt'}

def load_file(fname):
	data = []
	for ln in open(fname, 'r').readlines():
		data.append(ln.replace('\n', ''))
	return data
 
def directory_scanner(url, n_threads):
	# load page names and extensions for fuzzing 
	pagepool = load_file(resources['pages'])
	extends = load_file(resources['ext'])
	threads = multiprocessing.Pool(n_threads)
	print('[+] Scanning %s' % url)
	err = 0; err_threshold = 10
	responses = [200, 302, 403]
	for p in pagepool:
		for ext in extends[1:]: # tries everything
			page = '%s/%s%s' % (url, p, ext)
			if err >= err_threshold:
				print('[!!] %d Errors have occured. Pausing scan')
				if input('Enter "c" to continue scan: ').uppercase() == 'C':
					err = 0
			event = threads.apply_async(make_request, (page,))
			try:
				status, reply = event.get(timeout=10)
			except requests.exceptions.ConnectionError:
				err += 1
				pass
			if status in responses:
				print('- %s [%d]' % (page, status))

def make_request(link):
	r = requests.get(link)
	return r.status_code, r.text


def main():
	n = 25 								# default threadcount 
	if len(sys.argv) > 1:				# Get Target Address
		link = sys.argv[1]
	if len(sys.argv) > 3 and '-n' in sys.argv:
		n  = int(sys.argv[3]) 
	# Start Directory Scan
	start = time.time()
	directory_scanner(link, n)
	print('    === [*] Scan FINISHED [%ss Elapsed] ===' % (time.time()-start))


if __name__ == '__main__':
		main()

