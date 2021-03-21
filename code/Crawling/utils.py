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