import os, string, random, base64

alphas = list(string.lowercase + string.uppercase)

def create_random_file(ext):
	return ''.join(random.sample(alphas,8))+ext

def xor(data, n):
	return base64.b64encode(''.join([chr(ord(l)^n) for l in list(data)]))

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



if __name__ == '__main__':
	main()

