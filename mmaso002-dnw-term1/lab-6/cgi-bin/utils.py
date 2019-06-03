#!/usr/bin/env python3

""" 
	This module provides a set of reuseable utility functions
	This is a Google style docstring by the way.
	Read more about them here: 
	https://www.python.org/dev/peps/pep-0257/
"""

from pymongo import MongoClient

def db_connect():
	""" Provides a connection to mongoDB database
	
	Returns:
		Object: A handle to a mongoDB database 
	"""
	# try to create instance of MongoClient object
	try:
		client = MongoClient('mongodb://localhost:27017/')
	except:
		print("Error: failed to create mongo client")
		raise
	# if we have a mongo client...
	else:
		# switch to the specified database
		db = client.catflucks
		# return a handle to the database
		return db

