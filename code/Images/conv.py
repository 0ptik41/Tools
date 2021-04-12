import matplotlib.pyplot as plt
import os, sys, ppm
import numpy as np
import string


def color2bw(imarr):
	dims = imarr.shape
	imout = np.zeros((dims[0],dims[1]))
	print(dims[0],dims[1])
	for x in range(dims[0]):
		for y in range(dims[1]):
			r = imarr[x,y,0] 
			g = imarr[x,y,1] 
			b = imarr[x,y,2]
			imout[x,y] = ((r & g & b))
	return imout

def ascii_art(fname):
	ascii = list(string.printable.replace('\n'))
	ascii.remove('\n')
	ascii.remove('\r')
	ascii.remove('\t')
	ext = fname[2].split('.')[1]
	if ext == 'ppm':
		arr = ppm.ppm2arr(fname)
	else:
		arr = np.array(plt.imread(fname))
	bw = color2bw(arr)
	vals = [ord(n) for n in ascii]
	mapping = np.linspace(min(vals),max(vals),len(vals))
	maps = {}
	for i in range(len(mapping)): maps[i] = mapping[i]



if '-c2k' in sys.argv and len(sys.argv)>1:
	ext = sys.argv[2].split('.')[1]
	if ext == 'ppm':
		arr = ppm.ppm2arr(sys.argv[-1])
	else:
		arr = np.array(plt.imread(sys.argv[2]))
	bw = color2bw(arr)
	plt.imshow(bw)
	plt.show()
