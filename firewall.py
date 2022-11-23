#!/usr/bin/python
from netfilterqueue import NetfilterQueue
from scapy.all import IP
from multiprocessing import Process
from time import sleep
from json import load

#import configs
try:
    with open("config.json","r") as f:
        fdata = load(f)
        if("logging" in fdata):
            logging=bool(fdata["logging"])
        else:
            logging=False
        if("logfile" in fdata):
            logfile=fdata["logfile"]
        else:
            logfile="./logfile.log"
except FileNotFoundError:
    print("file config.json found, using default settings")
    logging = False

'''
try:
    y = None
    with open("firewallrules.json","r") as f:
        y = json.load(f)
except FileNotFoundError:
    print("firewallrules.json not found")
    ListOfBannedIpAddr = []
    ListOfBannedPorts = []
    ListOfBannedPrefixes = []
    TimeThreshold = 10 #sec
    PacketThreshold = 100
    BlockPingAttacks = True
'''

def logger(direction, src, dst, name, pname, secpname):
    if(logging):
        with open(logfile,"a") as f:
            f.write("{: >3} {: >15} -> {: >15}: {} {} {}\n".format(direction, src, dst, name, pname, secpname))
    else:
        print("{: >3} {: >15} -> {: >15}: {} {} {}".format(direction, src, dst, name, pname, secpname))

def firewallIn(pkt):
    #convert to scapy packet without ethernet frame
    sca = IP(pkt.get_payload())#scapy.layers.inet
    logger("in", sca.src, sca.dst, sca.name, sca.payload.name, sca.payload.payload.name)
    pkt.accept()

def firewallOut(pkt):
    #convert to scapy packet without ethernet frame
    sca = IP(pkt.get_payload())#scapy.layers.inet
    logger("out", sca.src, sca.dst, sca.name, sca.payload.name, sca.payload.payload.name)
    pkt.accept()

def firewallFwd(pkt):
    #convert to scapy packet without ethernet frame
    sca = IP(pkt.get_payload())#scapy.layers.inet
    logger("fwd", sca.src, sca.dst, sca.name, sca.payload.name, sca.payload.payload.name)
    pkt.accept()

def threadStart(queue, func):
    print("starting queue {}".format(queue))
    nfqueue = NetfilterQueue()
    nfqueue.bind(queue,func)
    try:
        nfqueue.run()
    except:
        print("nfqueue {} stopped".format(queue))
        nfqueue.unbind()

def main():
    processes = [(1,firewallIn),(2,firewallOut),(3,firewallFwd)]
    
    for process in processes:
        proc = Process(target=threadStart, args=process)
        proc.daemon = True
        proc.start()

    try:
        while(True):
            sleep(1000)#less cpu intensive
            #most cpu intensive task is starting multiprocess
    except:
        sleep(0.1)#give time for all threads to end
    print("end of firewall process")

if __name__=="__main__":
    main()
