import base64
import zlib
import json
import time
import sys 
import os 

def usage():
	print('Usage: $ python %s [mode] user@ip:/path/to/file')

def merge_logs(fileA, fileB):
	data1 = json.loads(open(fileA,'r').read())
	data2 = json.loads(open(fileB,'r').read())
	data3 = data1
	for k in data2.keys():	data3[k] = data2[k]
	return data3
	 
if 'add' in sys.argv and len(sys.argv) >= 3:
	try:
		data_add = sys.argv[-1]
		user = data_add.split(':')[0]
		fin = data_add.split(':')[1]
	except IndexError:
		pass
		usage()
		exit()
	if user.split('@')[1] == '127.0.0.1':
		print('[*] Loading Local file %s' % fin)
		if os.path.isfile(fin):
			raw_data = json.loads(open(fin, 'r').read())
			print(len(raw_data.keys()))
	else:
		print('[*] Loading Remote file %s' % fin)
		lcopy = fin.split('/')[-1]
		if os.path.isfile(lcopy):
			print('[!] A local copy of %s exists. Backing it up...' % fin)
			os.system('mv %s %s' % (lcopy, 'backup_'+lcopy))
		cmd = "sftp %s:%s <<< $'get %s'"  % (user, fin, 'data.json')
		print(cmd)
		os.system('echo "%s" | /bin/bash' % cmd)
		raw_data = json.loads(open(lcopy, 'r').read())
		print(len(raw_data.keys()))

if 'combine' in sys.argv:
	if '*' in sys.argv and len(sys.argv)== 3:
		print('[*] Combining all %s files' % sys.argv[2])
		exit()
	elif len(sys.argv) == 4:
		print('[*] Combining %s and %s into one file' % (sys.argv[2],sys.argv[3]))
		master = merge_logs(sys.argv[2], sys.argv[3])
		open('combined.json', 'w').write(json.dumps(master))
		print('[*] %d Total Entries in Combined JSON' % len(master.keys()))