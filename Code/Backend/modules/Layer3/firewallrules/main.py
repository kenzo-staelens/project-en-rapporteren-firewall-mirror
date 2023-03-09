#!/usr/bin/python
import sqlite3 as sql
from ...Helper import ipparser

def initcon(firewallpath):
	con = sql.connect(f"{firewallpath}/firewalldb.db")
	#with open(f"{firewallpath}/createdb.sql","r") as script:
	#	con.executescript(script.read())
	def anon():
		return con
	return anon

#con = initcon("modules/Layer3/firewallrules")
con = None

def config(jsonconfig):
	global con
	con = initcon(jsonconfig["firewall_module_path"])
	

def run(direction="ingress",pkt=None):
	query="WITH filteredTable AS (SELECT * FROM firewallrules WHERE direction=? and src_ip=?&src_mask and dst_ip=?&dst_mask and (protocol=? or protocol is null) and port_start<=? and port_end>=?) SELECT * FROM filteredTable WHERE priority=(SELECT MIN(priority) FROM filteredTable)"
	#get packet parameters ip src, ip dst, protocol name, target port
	'''
	print(f"src: {pkt.src}")
	print(f"dst: {pkt.dst}")
	print(f"name: {pkt._name}")
	print(f"proto: {pkt.get_field('proto').i2s[pkt.proto].upper()}")
	try:
		print(f"port: {pkt.payload.dport}")
	except:
		print("no port")
	pkt.show2()
	print("---")
	print("---")
	'''
	ip_src = pkt.src
	ip_dst = pkt.dst
	protocol = pkt.get_field('proto').i2s[pkt.proto].upper()
	try:
		port=pkt.payload.dport
	except Exception as ex:
		port = 0 #gebruik port 0 voor packets zonder poort
	
	queryparams = (
		direction,
		ipparser.parse_to_int(ip_src),
		ipparser.parse_to_int(ip_dst),
		protocol,
		port, port
	) #port x2 omdat port range test op zelfde cijfer test
	try:
		matchedrules = con().execute(query, queryparams)
		for rule in matchedrules:
			print(rule)
			if(rule[2]==0):
				return False
		return True
	except Exception as ex:
		print("exception during sql operation\n\t" + str(ex))
	
