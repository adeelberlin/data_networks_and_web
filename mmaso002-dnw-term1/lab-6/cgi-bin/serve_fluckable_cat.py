#!/usr/bin/env python3

from utils import db_connect
from bson.objectid import ObjectId
from datetime import datetime

import cgi
import cgitb
cgitb.enable()

# connect to database
db = db_connect()

# output some header html
print("Content-Type: text/html\n")
print("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Hello Caflucks</title>
</head>
<body>
<h1>Welcome to Catflucks</h1>""")

# get the form data
form = cgi.FieldStorage()

# get one random document from images collection
result = db.images.aggregate(
	[{ '$sample': { 'size': 1 } }]
)

# if a result came back
if result:
	# iterate through objects in the cursor (should only be 1)
	for img in result:
		# pull out the img url and alt text
		img_src = img['url']
		img_alt = img['alt']
		img_id = img['_id']

	# find and count flucks with matching img_id and where is_flucked is 1
	num_flucks = db.flucks.find( {"image_id": ObjectId(img_id), "is_flucked":1} ).count()

	print("""<p>You are viewing a random image of a cat.</p>
	<img src="{}" alt="{}" width=500>
	<p>This poor cat has been flucked {} times already.</p>
	""".format( img_src, img_alt, str(num_flucks) ))
else:
	print("<p>Oops. Something went wrong!</p>")

# output a form with skip/fluck buttons
print("""<form method="POST" action="/cgi-bin/serve_cat_beta.py">
		<input type="hidden" value="{}" name="img_id">
		<input name="btn_skip" type="submit" value="Skip">
		<input name="btn_fluck" type="submit" value="Fluck">
		</form>""".format( img_id ))

# check if either button clicked and insert a fluck in the database
if 'btn_fluck' in form:
	result = db.flucks.insert( { 
		"image_id":ObjectId(form['img_id'].value),
		"is_flucked":1,
		"timestamp":datetime.now().timestamp() 
	} )
elif 'btn_skip' in form:
	result = db.flucks.insert( { 
		"image_id":ObjectId(form['img_id'].value),
		"is_flucked":0,
		"timestamp":datetime.now().timestamp() 
	} )

# output some footer html
print("</body></html>")
