import subprocess
import os

import lib.settings as settings

class vms:
	# output to /dev/null
	output=open(os.devnull,'wb')

	# if debug then debug!
	def __init__(self):
		if settings.debug:
			self.output=None
			print("Running in debug mode")

	def start(self,nodes):
		self.create(nodes)
		for node in nodes:
			virshcmd = ["virsh","start",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)
	
	def stop(self,nodes):
		for node in nodes:
			virshcmd = ["virsh","destroy",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)
	
	def restart(self,nodes):
		for node in nodes:
			virshcmd = ["virsh","reset",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)	

	def suspend(self,nodes):
		for node in nodes:
			virshcmd = ["virsh","suspend",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)	

	def resume(self,nodes):
		for node in nodes:
			virshcmd = ["virsh","resume",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)
	
	def create(self,nodes):
		for node in nodes:
			qemucmd=[
			"qemu-img",
			"create",
			"-f",
			"qcow2",
			"-b",
			settings.diskpath+settings.operating_system+'/'+"base_"+settings.operating_system+".qcow2",
			settings.diskpath+settings.operating_system+'/'+settings.operating_system+str(node)+".qcow2"
			]
	
			virtcmd=[
			"virt-clone",
			"-o",
			"base_"+settings.operating_system,
			"-n",
			settings.operating_system+str(node),
			"-f",
			settings.diskpath+settings.operating_system+'/'+settings.operating_system+str(node)+".qcow2",
			"--check",
			"path_exists=off",
			"--preserve-data"
			]

			subprocess.call(qemucmd,stdout=self.output,stderr=self.output)
			subprocess.call(virtcmd,stdout=self.output,stderr=self.output)
	
	def delete(self,nodes):
		self.stop(nodes)
		for node in nodes:
			virshcmd = ["virsh","undefine","--remove-all-storage",settings.operating_system+str(node)]
			subprocess.call(virshcmd,stdout=self.output,stderr=self.output)	