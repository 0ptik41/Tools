from threading import Thread
import socket
import utils
import time
import sys 
import os 

class BasicAPI:
	inbound = 54123
	served = []
	start = 0.0

	def __init__(self):
		self.start = time.time()
		self.actions = {'UPTIME': self.uptime}
		self.run()

	def run(self):
		running = True
		start_day, start_time = utils.create_timestamp()
		print('[*] Starting Server [%s - %s]' % (start_day, start_time))
		srv = self.create_listener()
		while running: 
			try:
				# Wait for client 
				c, ci = srv.accept()
				# Pass client to handler thread
				Thread(target=self.client_hander, args=(self, c, ci)).start()
			except KeyboardInterrupt:
				running = False
				pass
		# close the server 
		end_day, end_time = utils.create_timestamp()
		print('[*] Shutting Down Server [%s - %s]' % (end_day, end_time))
		srv.close()

	def create_listener(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('0.0.0.0', self.inbound))
			s.listen(5)
		except socket.error:
			print('[!] Unable to create socket')
			exit()
		return s

	def uptime(self, c, i, r):
		c.send('UPTIME: %s' % str(time.time() - self.start))
		return c


	def client_hander(self, api, csock, caddr):
		raw_request = csock.recv(2048)
		print('[*] Connection Accepted from %s' % caddr[0])
		if len(raw_request.split(' ??? ')) >= 2:
			api_req = raw_request.split(' ??? ')[0]
			payload = raw_request.split(' ??? ')[1]
			if api_req in self.actions.keys():
				print(' - making %s request\n' % api_req)
				csock = self.actions[api_req](csock, caddr, payload)
		else:
			try:
				csock.send('[!] Invalid API Request.\nUse: "Method ??? Request"')
			except socket.error:
				pass
		# finally close connection to client
		csock.close()



def main():
	simple_server = BasicAPI()

if __name__ == '__main__':
	main()

