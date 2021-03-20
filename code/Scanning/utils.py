import random
import time
import sys 
import os 

lowers = ['a','b','c','d','e','f','g','h','i','j',
		  'k','l','m','n','o','p','q','r','s','t',
		  'u','v','w','x','y','z']
uppers = ['A','B','C','D','E','F','G','H','I','J',
		  'K','L','M','N','O','P','Q','R','S','T',
		  'U','V','W','X','Y','Z']
alphas = ['0', '1','2','3','4','5','6','7','8','9']

PYVER = int(sys.version.split(' ')[0].split('.')[0])

def swap(filename, destroy):
	data = []
	for line in open(filename, 'rb').readlines():
		data.append(line.replace('\n', ''))
	if destroy:
		os.remove(filename)
	return data

def create_random_filename(ext):
	charpool = []
	for l in lowers: charpool.append(l)
	for u in uppers: charpool.append(u)
	for a in alphas: charpool.append(a)
	basename = ''.join(random.sample(charpool, 6))
	random_file = basename +ext
	return random_file

def cmd(command, verbose):
	tmp = create_random_filename('.sh')
	tmp2 = create_random_filename('.txt')
	data = '#!/bin/bash\n%s\n#EOF' % command
	open(tmp, 'w').write(data)
	os.system('bash %s >> %s' % (tmp,tmp2))
	os.remove(tmp)
	if verbose:	
		os.system('cat %s' % tmp2)
	return swap(tmp2, True)

def create_timestamp():
    date = time.localtime(time.time())
    mo = str(date.tm_mon)
    day = str(date.tm_mday)
    yr = str(date.tm_year)

    hr = str(date.tm_hour)
    min = str(date.tm_min)
    sec = str(date.tm_sec)

    date = mo + '/' + day + '/' + yr
    timestamp = hr + ':' + min + ':' + sec
    return date, timestamp
