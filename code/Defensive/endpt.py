from threading import Thread
import utils
import json
import time 
import sys 
import os 


def check_connections():
	# Check local tcp/udp connections coming from this machine
	# based on various TCP/IP connection states 
	connections = {"ESTABLISHED":{'tcp':[], 'udp':[]},
				   "TIME_WAIT": {'tcp':[], 'udp':[]},
				   "CLOSE_WAIT": {'tcp':[], 'udp':[]},
				   "LISTEN": {'tcp':[], 'udp':[]}}
	for line in utils.cmd('netstat -antup',False):
		# Find connections by state 
		for STATE in connections.keys():
			if len(line.split(STATE))>1:
				items = filter(len, line.split(STATE)[0].split(' '))
				if items[0] not in connections[STATE].keys():
					print('[!] Unrecognized Protocol %s' % items[0])
				else:
					connections[STATE][items[0]].append([items[-2],items[-1]])
	return connections

class Monitor:
	def __init__(self, timeout=10):
		self.sdate, self.stime = utils.create_timestamp()
		self.log = self.create_log()
		self.start = time.time()
		self.interval = timeout
		self.running = True
	
	def create_log(self):
		if not os.path.isdir('.logs'):
			os.mkdir('.logs')
		header = '[+] System Monitor Started [%s -%s]\n'%(self.sdate,self.stime)
		fn = os.getcwd()+'/.logs/'+self.sdate.replace('/','')+'_'+self.stime.replace(':','')+'.log'
		open(fn,'w').write(header)
		print(header)
		return fn
	
	def shutdown(self):
		lt, ld = utils.create_timestamp()
		msg = '[!] Shutting Down [%s - %s]\n' % (lt,ld)
		print(msg); self.running = False
		open(self.log,'a').write(msg)
	
	def add_connection_data(self, connections):
		ld, lt = utils.create_timestamp()
		msg = '='*80+'\n'+'[+] Connection Data [%s - %s]:'%(ld,lt)
		open(self.log,'a').write(msg)
		open(self.log,'a').write(json.dumps(connections))
		open(self.log,'a').write('\n'+'='*80+'\n')
		
	def run(self):
		try:
			while self.running:
				# Log Connections 
				self.add_connection_data(check_connections())
				# Back up file if it gets too large?
				
				# Sleep 
				time.sleep(self.interval)
		except KeyboardInterrupt:
			self.shutdown()
			pass

if __name__ == '__main__':
	logger = Monitor()
	logger.run()

