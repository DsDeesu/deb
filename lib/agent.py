import socket
import time
import errno

import lib.domains as domains
import lib.settings as settings

# agent is waiting for connection from vms, and after providing base system deb/sol and mac address - return hostname

def agent():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(('10.10.0.1',1234))
	sock.listen(5)

	try:
		while True:
			conn,addr = sock.accept()
			print("connection from: ", addr[0])
			hostname = conn.recv(1024).rstrip()
			macaddr = conn.recv(1024).rstrip()


			if hostname == 'exit\n':
				break
		
			reply = 'UNKNOWN'
		
			if settings.debug: print("debug: hostname: %s, macaddr: %s" % (hostname, macaddr))
		
			# Checking received hostname for similiar in hypervisor
			for domain in domains.get_domain_dict(hostname):
				if settings.debug: print('Checking: ',domain['name'])
				if settings.debug: print("if |",domain['mac'],'| is equal to |',macaddr,'|')
				if str(domain['mac']) == str(macaddr):
					if settings.debug: print('true it is!')
					reply = domain['name']
		
			conn.sendall(reply)
			conn.close()

	except KeyboardInterrupt:
		conn.close()
		sock.close()
		if settings.debug: print("closing")
	sock.close()