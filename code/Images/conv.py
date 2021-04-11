import matplotlib.pyplot as plt
import os, sys, ppm
import numpy as np


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

if '-c2k' in sys.argv and len(sys.argv)>1:
	ext = sys.argv[2].split('.')[1]
	if ext == 'ppm':
		arr = ppm.ppm2arr(sys.argv[-1])
	else:
		arr = np.array(plt.imread(sys.argv[2]))
	bw = color2bw(arr)
	plt.imshow(bw)
	plt.show()