from prettytable import PrettyTable
from time import sleep

def get_table(domains):
	table = PrettyTable(["NAME","IPv4","MAC","STATUS"])

	for domain in domains:
		table.add_row([domain['name'],domain['ip'],domain['mac'],domain['status']])

	return table

# print get_table()