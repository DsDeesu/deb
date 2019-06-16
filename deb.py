#!/usr/bin/python3
#Version 0.95
import sys
import os
from time import sleep

import lib
from lib import settings

def help():
	print(f"Usage:")
	print(f" deb <action> [-r] <nodes>")
	print(f"     <action> - Should be one of folowing: create,delete,start,stop,restart,suspend,resume,status")
	print(f"     <nodes>  - Should be range/list of nodes to operate on")
	print(f"    -r/--range    - Run in range mode (e.g. 2-5)")
	print(f"    -l/--lock     - Only working with status. Lock print and wait for changes")
	print(f"    -s/--solaris  - Use solaris instead")
	print(f"    -c/--centos   - Use centos instead")
	print(f"    -m/--all      - Show all machines")
	print(f"    -d/--debug    - Print debug information")
	exit(0)

# check sys.argv for *args, and if remove=True, remove it from sys.argv.
def check_args(remove,*args):
	for arg in args:
		if arg in sys.argv:
			if remove:
				sys.argv.remove(arg)
			return True
	return False

#killers
if (
	(("-h" in sys.argv) or ("--help"  in sys.argv) or (len(sys.argv) == 1)) or # 0 args or help
	((("-r" in sys.argv) or ("--range" in sys.argv)) and (len(sys.argv) < 3)) or # -r without range
	((("-l" in sys.argv) or ("--lock"  in sys.argv)) and ("status" not in sys.argv)) # lock without status
	):
	help()
#end of killers

# initialize global variables
settings.init()

# check wheter debug mode should be active
if check_args(True,'-d','--debug'):
	settings.debug=True

# if agent, run agent - nothing more
if check_args(True,'-a','--agent'):
	lib.agent.agent()
	exit(0)

# check wheter solaris option is up, and remove them from sys.argv 
# (because later is hard to handle it - creating nodes list)
if check_args(True,'-s','--solaris'):
	settings.operating_system='sol'

# check wheter centos option is up, and remove them from sys.argv 
# (because later is hard to handle it - creating nodes list)
if check_args(True,'-c','--centos'):
	settings.operating_system='centos'

# check if all machines
if check_args(True,'-m','--all'):
	settings.operating_system='all'

# if interactive - start shell
# and clean sys.argv because of cmd2 wrongly handling it
if check_args(False,'-i','--interactive'):
	sys.argv = []
	lib.interactive.cmd().cmdloop()
	exit(0)


# if status then status and nothing else!
if check_args(True,'status'):
	if check_args(True,'-l','--lock'):
		os.system("clear")
		actual_table = lib.table.get_table(lib.domains.get_domain_dict(settings.operating_system))
		print(actual_table)
		try:
			while True:
				sleep(1)
				new_table = lib.table.get_table(lib.domains.get_domain_dict(settings.operating_system))
				if((str(new_table) != str(actual_table)) # casting to string because we need to comparise only string output
					and 'base' in str(new_table)):       # without checking PrettyTable metadata
					os.system("clear")
					print(new_table)
					actual_table = new_table
		except KeyboardInterrupt: # ctrl + C - handling (lazy)
			print(f"\nBye, bye")
			exit(0)
	else: # Without locking (without bash 'watch' like feature)
		print(lib.table.get_table(lib.domains.get_domain_dict(settings.operating_system)))
	exit(0)


# convert args into list of nodes
# thats why we are removing -s / --solaris
nodes = []
try:
	if check_args(True,'-r','--range'):
		for argument in sys.argv[2:]:
			if "-" in argument:
				user_range = argument.split("-")
				start = int(user_range[0])
				stop = int(user_range[1])
				for number in range(start,stop):
					nodes.append(number)
				nodes.append(stop)
			else:
				nodes.append(int(argument))
	elif check_args(True,'all'): #handle 'all' request
		for domain in lib.domains.get_domain_dict(settings.operating_system):
			if domain['name'] != "base_"+settings.operating_system:
				nodes.append(domain['name'][3:])
	elif check_args(True,'-n','--name'):
		nodes.append(''.join(sys.argv[2:]))
	else:
		for node in range(1,int(sys.argv[2])):
			nodes.append(node)
		nodes.append(int(sys.argv[2]))
except ValueError:
		print(f"Node must be a number!")
		exit(0)

# create management object
# remeber this class is taking from lib.config
vms = lib.vm.vms()

if "create" in sys.argv:
	vms.create(nodes)

elif "delete" in sys.argv:
	vms.delete(nodes)

elif "start" in sys.argv:
	vms.start(nodes)

elif "stop" in sys.argv:
	vms.stop(nodes)

elif "restart" in sys.argv:
	vms.restart(nodes)

elif "suspend" in sys.argv:
	vms.suspend(nodes)

elif "resume" in sys.argv:
	vms.resum(enodes)

elif "reset" in sys.argv:
	vms.restart(nodes)

else:
	help()