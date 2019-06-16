def init():
	# can be changed to sol by -s/--solaris option
	global operating_system
	operating_system='deb'

	global diskpath
	diskpath='/home/dees/vms/'

	# can be changed with -d/--debug option
	global debug
	debug=False
