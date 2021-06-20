import sys
import os 

def trim_file(fname,nlines):
	data = open(fname,'r').read().split('\n')
	open(fname,'w').write('\n'.join(data[-1*nlines:]))