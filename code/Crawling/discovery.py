from tqdm import tqdm
import multiprocessing 
import random
import utils
import json
import time 
import sys 
import os

def query_thread(ip):
	fout = utils.create_random_filename('.txt')
	c = 'dig -x %s >> %s' % (ip, fout)
	os.system(c)
	return fout

def usage():
	print('Usage: %s ip_list.txt' % sys.argv[0])

def parse_dig(fin):
	found = []
	for line in utils.read(fin,True):
		# print(line)
		if len(line.split('SOA')) > 1:
			for item in line.split('SOA')[-1].split(' '):
				if len(item.split('.'))==4:
					found.append(item.replace('\t',''))
	return found

def run_scan(n_threads, file_in):
	pool = multiprocessing.Pool(n_threads)
	hosts = utils.read(file_in, False)
	random.shuffle(hosts)
	print('[*] Digging...')
	open('scan_result.json','w').write('')
	domains_found = {}; completed = 0
	try:
		for address in tqdm(hosts):
			completed += 1
			try:
				query = pool.apply_async(query_thread, (address,))
				fname = query.get(timeout=2)
				domains_found[address] = parse_dig(fname)
				if completed % 100:
					open('scan_result.json','w').write(json.dumps(domains_found))
			except multiprocessing.TimeoutError:
				pass
	except KeyboardInterrupt:
		print('[X] Stopping the Digging...')
		pass


def main():
	N = 15
	start = time.time()
	if len(sys.argv) > 1:
		# load file of addresses to dig
		input_file = sys.argv[1]
		# run the scan
		run_scan(N, input_file)
	else:
		usage()
	print('[*] FINISHED [%ss Elapsed]' % str(time.time() - start))

if __name__ == '__main__':
	main()