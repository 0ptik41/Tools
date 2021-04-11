import matplotlib.pyplot as plt
import numpy as np
import os, sys

ppm_magic = '\x50\x33 %d %d %d\n'

def flat2d(array):
	arr = ''
	for row in array:
		for col in row:
			arr += str(int(col)) + ' '
		arr += '\n'
	return arr

def flat3d(array):
	arr = ''
	for row in array:
		for pxl in row:
			for ch in pxl:
				arr += str(int(ch)) + ' '
		if len(row):
			arr += '\n'
	return arr

def img2ppm(fpath):
	imarr = np.array(plt.imread(fpath))
	data = flat3d(imarr)
	w = int(imarr.shape[0])
	h = int(imarr.shape[1])
	m = int(imarr.max())
	magic = ppm_magic % (w,h,m)
	new_name = fpath.split('/')[-1].split('.')[0]+'.ppm'
	open(new_name,'w').write(magic+data)



if '-to' in sys.argv and len(sys.argv) > 2:
	img2ppm(sys.argv[2])

