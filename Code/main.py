from Backend import firewall as backend
from Backend import moduleloader
from Frontend import main as frontend
from threading import Thread
from time import sleep
from json import load

def main():
    config={}
    try:
        with open("../VM/Config/config.json","r") as f:
            fdata = load(f)
            #logging settings
            if("logging" in fdata):
                config["logging"]=(fdata["logging"]=="True")#convert from string to bool
            else:
                config["logging"]=False
            if("logfile" in fdata):
                config["logfile"]=fdata["logfile"]
            else:
                config["logfile"]="../VM/Logs/logfile.log"
            #module loading
            ignored_l3 = fdata["ignored_modules"]["Layer3"]
            ignored_l4 = fdata["ignored_modules"]["Layer4"]
            L3_modules = moduleloader.getModules("Backend/Layer3",ignored_l3)
            L4_modules = moduleloader.getModules("Backend/Layer4",ignored_l4)
            for module_name in L3_modules:
                try:
                    L3_modules[module_name][0].config(fdata)
                except:
                    print(f"could not load module {module_name}")
                    del L3_modules[module_name]
            config["L3_modules"] = L3_modules
            config["L4_modules"] = L4_modules
    except FileNotFoundError:
        print("file config.json not found, using default settings")
        config["logging"] = False
        config["L3_modules"] = {}
        config["L4_modules"] = {}

    print("starting backend")
    backendThread = Thread(target=backend.main,args=(config,))
    backendThread.daemon = True
    backendThread.start()
    
    sleep(5)#wait for backend to fully start
    print("starting frontend")
    frontendThread = Thread(target=frontend.main,args=(config,))
    frontendThread.daemon = True
    frontendThread.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("shutting down firewall")
    
    
if __name__ =="__main__":
    main()
