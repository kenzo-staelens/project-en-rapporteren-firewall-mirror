#!/usr/bin/python
#example code
import os
import importlib

# Define the path to the modules folder
module_folder = "modules"

def getModules():
	# Get a list of all Python files in the modules folder
	module_filenames = [f[:-3] for f in os.listdir(module_folder) if f.endswith(".py")]

	# Import all modules in the modules folder and store them in a dictionary
	modules = {}
	for module_name in module_filenames:
		module = importlib.import_module(f"{module_folder}.{module_name}",package=None)
		modules[module_name] = module

	return modules
