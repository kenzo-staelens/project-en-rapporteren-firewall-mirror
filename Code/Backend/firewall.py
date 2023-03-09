#!/usr/bin/python
from netfilterqueue import NetfilterQueue
from scapy.all import IP
from multiprocessing import Process
from time import sleep
from json import load
import moduleloader

#import configs
try:
    with open("../../VM/Config/config.json","r") as f:
        fdata = load(f)
        if("logging" in fdata):
            logging=(fdata["logging"]=="True")
        else:
            logging=False
        if("logfile" in fdata):
            logfile=fdata["logfile"]
        else:
            logfile="../../VM/Logs/logfile.log"
        ignored_l3 = fdata["ignored_modules"]["Layer3"]
        ignored_l4 = fdata["ignored_modules"]["Layer4"]
        L3_modules = moduleloader.getModules("Layer3",ignored_l3)
        L4_modules = moduleloader.getModules("Layer4",ignored_l4)
        for module in L3_modules:
                L3_modules[module].config(fdata)
except FileNotFoundError:
    print("file config.json found, using default settings")
    logging = False
    L3_modules = {}
    L3_modules = {}



def logger(direction, src, dst, name, pname, secpname, extra=""):
    if(logging):
        with open(logfile,"a") as f:
            f.write("{: >3} {: >15} -> {: >15}: {} {} {} {}\n".format(direction, src, dst, name, pname, secpname, extra))
    else:
        print("{: >3} {: >15} -> {: >15}: {} {} {}".format(direction, src, dst, name, pname, secpname))

def firewallChannel(direction):
    def channel(pkt):
        try:
            sca = IP(pkt.get_payload())#scapy.layers.inet
            logger(direction, sca.src, sca.dst, sca.name, sca.payload.name, sca.payload.payload.name)
            for module in L3_modules: #for key in dictionary
                accepted = L3_modules[module].run(direction, sca)
                if(not accepted):
                    pkt.drop()
                    break
            pkt.accept()
        except Exception as e:
            print(e)
    
    return channel

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
    processes = [(1,firewallChannel("in")),(2,firewallChannel("out")),(3,firewallChannel("fwd"))]
    
    for process in processes:
        proc = Process(target=threadStart, args=process)
        proc.daemon = True
        proc.start()

    try:
        while(True):
            sleep(1)#less cpu intensive
            #most cpu intensive task is starting multiprocess
    except:
        sleep(0.1)#give time for all threads to end
    print("end of firewall process")

if __name__=="__main__":
    main()
