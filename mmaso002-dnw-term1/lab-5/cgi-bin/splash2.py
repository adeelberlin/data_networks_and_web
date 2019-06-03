#!/usr/bin/env python3

from pymongo import MongoClient

def db_connect():
	# try to create instance of MongoClient object
	try:
		client = MongoClient('mongodb://localhost:8000/')
	except:
		print("Error: failed to create mongo client")
	# switch to the specified database
	db = client.test
	# return a handle to the database
	return

# connect to database
db = db_connect()

# get one random document from images collection
result = db.images.find()

# if a result came back
if result:
	# iterate through objects in the cursor (should only be 1)
	for img in result:
		# pull out the img url and alt text
		img_src = img['src']
		img_alt = img['alt']

	print("Content-Type: text/html\n")
	print("""<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta charset="utf-8">
	<title>Hello Caflucks</title>
	</head>
	<body>
	<h1>Welcome to Catflucks</h1>
	<p>You are viewing a random image of a cat.</p>
	<img src="{}" alt="{}" width=500>
	</body>
	</html>""".format( img_alt, img_src ))
