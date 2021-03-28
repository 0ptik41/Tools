import numpy as np
import time 
import cv2
import sys 
import os

def load_image(filename, datatype):
	if not os.path.isfile(filename):
		print('[!] Unable to find %s' % filename)
		exit()
	return np.array(cv2.imread(filename)).astype(datatype)

def gif2images(filename):
	if os.path.isdir('output'):
		print('\033[1m\033[31m[*] Removing old outputs\033[0m')
		os.system('rm -rf output/')
	os.mkdir('output')
	output_loc = 'output/frame%02d.png'
	os.system('ffmpeg -i %s -loglevel panic -vsync 0 %s' % (filename, output_loc))
	# Read them all
	rawframes = os.listdir('output')
	print('[*] Extracting %d images...' % len(rawframes))
	images = {}
	frames = list()
	for n in rawframes: 
		frames.append(int(n.replace('.png','').replace('frame','')))
	frames.sort()
	for i in frames:
		images[i] = load_image(os.getcwd()+'/output/frame%02d.png' % i, np.uint8)
	os.system('rm -rf output/')
	return images

