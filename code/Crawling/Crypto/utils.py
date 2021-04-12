import os, string, time, random, base64

alphas = list(string.lowercase + string.uppercase)

def create_random_filename(ext):
	return ''.join(random.sample(alphas,8))+ext

def shellc(cmd, verbose):
	rf = create_random_file('.txt')
	os.system('%s >> %s;' % (cmd,rf))
	result =[]
	for line in open(rf,'r').readlines():
		result.append(line.replace('\n','').replace('\r',''))
	os.remove(rf)
	if verbose:
		print(result)
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

def swap(filename, destroy):
	data = []
	for line in open(filename, 'rb').readlines():
		data.append(line.decode().replace('\n', ''))
	if destroy:
		os.remove(filename)
	return data
