import os, sys, ppm

# convert folder of images to gif, 1st str is input video, 2nd is out gif fmt
vid2gif = 'ffmpeg -i %s -vf "fps=10,scale=%d:-1:flags=lanczos,'\
		 'split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 1 %s'
# convert video to images, 1st str is input video, 2nd is output im fmt 
vid2img = 'mkdir frames; cd frames; ffmpeg -i ../%s '
v2i_end = '-vf fps=20 out%03d.jpg'
# convert images to gif,1st string is output gif name
img2gif = 'ffmpeg -i frames/%03d.ppm -vf fps=20,scale=720:-1 %s'

if '-in' in sys.argv and len(sys.argv) > 1:
	# so can I make a gif out of PPMs?
	g = sys.argv[2]
	gif = g.split('/')[-1]
	os.system('cp %s %s' % (g, gif))
	print(vid2img%gif+v2i_end)
	os.system(vid2img%gif+v2i_end)
	for f in os.listdir('frames'):
		ppm.img2ppm('frames/'+f)
	fin = 'ffmpeg -i out%03d.ppm -vf fps=20,scale=720:-1 fin.gif'
	os.system(fin+'; rm -rf frames; rm *.ppm')