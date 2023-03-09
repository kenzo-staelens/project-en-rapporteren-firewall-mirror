#!/usr/bin/python
#import module.to.test as mod
import modules.Layer3.firewallrules as mod
from json import load
import moduleloader

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

mod.run()
