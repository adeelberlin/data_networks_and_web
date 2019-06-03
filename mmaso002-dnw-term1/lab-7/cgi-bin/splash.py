#!/usr/bin/env python3

"""
	This script is the main entry point to
	the catflucks application.
"""

# import modules from Python standard library
from bson.objectid import ObjectId
import cgi
import cgitb
cgitb.enable()
from datetime import datetime

# import custom modules
from config import config
import utils

# connect to database
db = utils.db_connect( config )

# render header HTML
print("Content-Type: text/html\n")
print( utils.render_template( config['TEMPLATE_DIR'] + 'header.html') )

# get the form data
form = cgi.FieldStorage()

# get one random document from images collection
result = db.images.aggregate(
	[{ '$sample': { 'size': 1 } }]
)

# if a result came back, do stuff with it...
if result:
	# iterate through objects in the cursor (should only be 1)
	for img in result:
		# pull out the img url and alt text
		img_src = img['url']
		img_alt = img['alt']
		img_id = img['_id']
	
	# render serve_cat template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'serve_cat.html', data=[img_src, img_alt] ) )

	# find and count flucks with matching img_id and where is_flucked is 1
	num_flucks = db.flucks.find( {"image_id": ObjectId(img_id), "is_flucked":1} ).count()

	# render cat_stats template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'cat_stats.html', data=[num_flucks] ) )

	# render form_fluck template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'form_fluck.html', data=["/cgi-bin/splash.py",img_id] ) )
else:
	print("<p>Oops. Something went wrong!</p>")

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

# render cat_stats template, passing it the dynamic data
print( utils.render_template( config['TEMPLATE_DIR']+'footer.html' ) )
