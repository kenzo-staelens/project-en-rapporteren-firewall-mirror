#!/usr/bin/python
#example code
import os
import importlib

# Define the path to the modules folder
module_folder = "modules"

def getModules():
	# Get a list of all Python files in the modules folder
	module_filenames = [f for f in os.listdir(module_folder) if os.path.isdir(f"{module_folder}/{f}")]

	# Import all modules in the modules folder and store them in a dictionary
	modules = {}
	for module_name in module_filenames:
		try:
			module = importlib.import_module(f"{module_folder}.{module_name}.main",package=None)
			modules[module_name] = module
		except:
			print(f"error loading module {module_name}")

	return modules
