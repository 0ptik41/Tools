import os, sys, string, random, base64

alphas = list(string.lowercase + string.uppercase)

def create_random_file(ext):
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

def xor(data, n):
	return ''.join([chr(ord(l)^n) for l in list(data)])


if __name__ == '__main__':
	main()

