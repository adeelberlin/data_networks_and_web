#!/usr/bin/env python3

from bson.objectid import ObjectId

import cgi
import cgitb
cgitb.enable()
from datetime import datetime

from config import config
import utils

db = utils.db_connect( config )


print("Content-Type: text/html\n")
print( utils.render_template( config['TEMPLATE_DIR'] + 'header.html') )


form = cgi.FieldStorage()

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
	#create likes varibale find fluck with image id and if fluck has likes
	likes  = db.flucks.find( {"image_id": ObjectId(img_id), "likes":1} ).count()
	#print(likes)
	# render cat_stats template, passing it num_flucks and likes to cat_stats.html file
	print( utils.render_template( config['TEMPLATE_DIR']+'cat_stats.html', data=[num_flucks,likes] ) )

	# render form_fluck template, passing it dynamic data
	print( utils.render_template( config['TEMPLATE_DIR']+'form_fluck.html', data=["/scripts/cats.py",img_id] ) )
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
#check if btn_like in form is clicked
elif 'btn_like' in form:
        result = db.flucks.insert( {
                "image_id":ObjectId(form['img_id'].value),
                "is_flucked":0,
                "timestamp":datetime.now().timestamp(),
		"likes":1
        } )
	

print( utils.render_template( config['TEMPLATE_DIR']+'footer.html' ) )
