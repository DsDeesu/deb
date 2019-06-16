import libvirt
import xml.etree.ElementTree as ET
from isc_dhcp_leases import IscDhcpLeases

def get_domain_dict(operating_system):
	connection = libvirt.open("qemu:///system")
	vms_dict = [] # list of dictionaries of vms..
	defined_vms = []

	# 0 for take every state of machine. More states are available on the bottom of this script
	domains = connection.listAllDomains(0)

	# if connection returned domains, then add them to list with machine names
	if len(domains) != 0:
		for domain in domains:
			defined_vms.append(domain.name())

	for vm in defined_vms:
		#get name of the vm and check if it starts with 'deb', if not - skip this vm
		name = vm
		# if not name.startswith("deb"):
		if (operating_system not in name) and (operating_system is not 'all'):
			continue

		#get mac of the vm
		xml = connection.lookupByName(vm).XMLDesc()
		rootxml = ET.fromstring(xml)
		ifaces = rootxml.findall("./devices/interface/mac")
		for iface in ifaces:
			mac = iface.attrib["address"]

		#get ipv4 of the vm
		leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
		try:
			ip = leases.get_current().get(mac).ip
		except AttributeError:
			ip = "UNKNOWN"

		#get status
		status = "UNKNOWN"
		state = connection.lookupByName(name).state()[0] 
		if state == libvirt.VIR_DOMAIN_NOSTATE:
		    status = "NOSTATE"
		elif state == libvirt.VIR_DOMAIN_RUNNING:
		    status = "RUNNING"
		elif state == libvirt.VIR_DOMAIN_BLOCKED:
		    status = "BLOCKED"
		elif state == libvirt.VIR_DOMAIN_PAUSED:
		    status = "PAUSED"
		elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
		    status = "OFFLINE"
		elif state == libvirt.VIR_DOMAIN_SHUTOFF:
		    status = "OFFLINE"
		elif state == libvirt.VIR_DOMAIN_CRASHED:
		    status = "CRASHED"
		elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
		    status = "PMSUSPENDED"

		#add domain to list of dictionaries of vms
		vms_dict.append({
			'name':name,
			'mac':mac,
			'ip':ip,
			'status':status
			})

	connection.close()
	return sorted(vms_dict, key=lambda k: k['name'])

# print get_domain_dict('deb')


# Vhe listAllDomains method takes a single parameter which is a flag specifying a filter for the domains to be listed. If a value of 0 is specified then all domains will be listed. Otherwise any or all of the following constants can be added together to create a filter for the domains to be listed.
# VIR_CONNECT_LIST_DOMAINS_ACTIVE
# VIR_CONNECT_LIST_DOMAINS_INACTIVE
# VIR_CONNECT_LIST_DOMAINS_PERSISTENT
# VIR_CONNECT_LIST_DOMAINS_TRANSIENT
# VIR_CONNECT_LIST_DOMAINS_RUNNING
# VIR_CONNECT_LIST_DOMAINS_PAUSED
# VIR_CONNECT_LIST_DOMAINS_SHUTOFF
# VIR_CONNECT_LIST_DOMAINS_OTHER
# VIR_CONNECT_LIST_DOMAINS_MANAGEDSAVE
# VIR_CONNECT_LIST_DOMAINS_NO_MANAGEDSAVE
# VIR_CONNECT_LIST_DOMAINS_AUTOSTART
# VIR_CONNECT_LIST_DOMAINS_NO_AUTOSTART
# VIR_CONNECT_LIST_DOMAINS_HAS_SNAPSHOT
# VIR_CONNECT_LIST_DOMAINS_NO_SNAPSHOT