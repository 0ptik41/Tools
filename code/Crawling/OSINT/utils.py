import random
import base64
import time 
import json
import os 

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
		   'n','o','p','q','r','s','t','u','v','w','x','y','z']

def read(f, d):
	out = []
	for line in open(f,'r').readlines():
		ln = line.replace('\n','')
		if len(ln) > 0:
			out.append(ln)
	if d:
		os.remove(f)
	return out 

def create_random_filename(ext):
	pool = []
	for l in letters: pool.append(l)
	for L in letters: pool.append(l.upper())
	for n in range(9): pool.append(str(n))
	random.shuffle(pool)
	return ''.join(random.sample(pool, 6)) + ext


def execute(cmd,show):
	f = create_random_filename('.txt')
	os.system('%s >> %s;' % (cmd, f))
	result = read(f,True)
	if show:
		for ln in result:
			print(ln)
	return result


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

def merge_logs(fileA, fileB):
	data1 = json.loads(open(fileA,'r').read())
	data2 = json.loads(open(fileB,'r').read())
	data3 = data1
	for k in data2.keys():	data3[k] = data2[k]
	return data3

