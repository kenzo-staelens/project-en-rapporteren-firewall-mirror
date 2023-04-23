#!/usr/bin/python
import sqlite3 as sql
from ...Helper import ipparser

def initcon(firewallpath):
    con = sql.connect(f"{firewallpath}/firewalldb.db")
    #with open(f"{firewallpath}/createdb.sql","r") as script:
    #    con.executescript(script.read())
    def anon():
        return con
    return anon

#con = initcon("modules/Layer3/firewallrules")
con = None

def config(jsonconfig):
    global con
    con = initcon(jsonconfig["firewall_module_path"])

def addEntry(allow, priority, direction, src, src_mask, dst, dst_mask, port_start, port_end, protocol):
    query = "insert into firewallrules(allow, priority, direction,src_ip,src_mask,dst_ip,dst_mask,protocol, port_start, port_end) values(?,?,?,?,?,?,?,?,?,?)"
    params = (allow, priority, direction, ipparser.mask_ip(src, src_mask),
    ipparser.parse_to_int(src_mask), ipparser.mask_ip(dst, dst_mask), ipparser.parse_to_int(dst_mask), protocol, port_start, port_end)
    try:
        con().execute(query,params)
        con().commit()
    except:#threading issues
        extracon = initcon("Backend/modules/Layer3/firewallrules")
        rules = extracon().execute(query,params)
        extracon().commit()
        
    
def postconfig(rules):
    usable = []
    for rule in rules:
        #initial verification and conversion to usable format
        if rule["behaviour"].lower()!="allow" and rule["behaviour"].lower()!="deny":
            return 400
        try:
            allowed = True if rule["behaviour"].lower()=="allow" else False
            prio = int(rule["priority"])
            (src_ip, src_mask) = rule["source"].split(" : ")
            (dst_ip, dst_mask) = rule["destination"].split(" : ")
            proto = None if rule["protocol"].lower()=="any" else rule["protocol"]
            if "-" in rule["ports"]:
                (port_s, port_e) = (int(x) for x in rule["ports"].split("-"))        
            else:
                port_s= port_e = int(rule["ports"])
            
            if not ipparser.verifyQuads(src_ip, src_mask, dst_ip, dst_mask):
                return 400
            #have to fix direction, "ingress" now as placeholder
            merged = (allowed, prio, "ingress", src_ip, src_mask, dst_ip, dst_mask, port_s, port_e, proto)
            usable.append(merged)
        except Exception as e:
            print(e)
            return 400
    for entry in usable:
        addEntry(*entry)
    return 200

def getconfig():
    global con
    configresult = []
    query = "select * from firewallrules"
    try:
        rules = con().execute("select * from firewallrules").fetchall()
    except:#threading issues
        extracon = initcon("Backend/modules/Layer3/firewallrules")
        rules = extracon().execute("select * from firewallrules").fetchall()
    
    try:
        for rule in rules:
            configresult.append({
                "behaviour":"allow" if rule[2] else "deny",
                "priority":f"{rule[3]}",
                "source":f"{ipparser.parse_to_quad(rule[4])} : {ipparser.parse_to_quad(rule[5])}",
                "destination":f"{ipparser.parse_to_quad(rule[6])} : {ipparser.parse_to_quad(rule[7])}",
                "protocol":"any" if rule[8]==None else rule[8],
                "ports":f"{rule[9]}-{rule[10]}" if rule[9]!=rule[10] else f"{rule[9]}"
            })
    except Exception as e:
        print(e)
        pass
    return configresult

def run(direction="ingress",pkt=None):
    #query="WITH filteredTable AS (SELECT * FROM firewallrules WHERE direction=? and src_ip=?&src_mask and dst_ip=?&dst_mask and (protocol=? or protocol is null) and port_start<=? and port_end>=?) SELECT * FROM filteredTable WHERE priority=(SELECT MIN(priority) FROM filteredTable)"
    query="WITH filteredTable AS (SELECT * FROM firewallrules WHERE src_ip=?&src_mask and dst_ip=?&dst_mask and (protocol=? or protocol is null) and port_start<=? and port_end>=?) SELECT * FROM filteredTable WHERE priority=(SELECT MIN(priority) FROM filteredTable)"
    ip_src = pkt.src
    ip_dst = pkt.dst
    protocol = pkt.get_field('proto').i2s[pkt.proto].upper()
    try:
        port=pkt.payload.dport
    except Exception as ex:
        port = 0 #gebruik port 0 voor packets zonder poort
    
    queryparams = (
        #direction,
        ipparser.parse_to_int(ip_src),
        ipparser.parse_to_int(ip_dst),
        protocol,
        port, port
    ) #port x2 omdat port range test op zelfde cijfer test
    try:
        matchedrules = con().execute(query, queryparams)
        for rule in matchedrules:
            if(rule[2]==0):
                return False
        return True
    except Exception as ex:
        print("exception during sql operation\n\t" + str(ex))
    
