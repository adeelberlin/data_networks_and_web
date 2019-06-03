#!/usr/bin/env python3


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

print( utils.render_template( config['TEMPLATE_DIR']+'form_new_cat.html' ,data=["/scripts/new_cat.py",ObjectId.from_datetime(datetime.now())]) )

# check if either button clicked and insert a image in the database
if 'btn_submit' in form:
	result = db.images.insert( { 
		"_id":ObjectId(form['img_id'].value),
		"alt":form.getvalue('alt'),
		"url":form.getvalue('url'),
		"created":datetime.now().timestamp() 
	} )

# render cat_stats template, passing it the dynamic data
print( utils.render_template( config['TEMPLATE_DIR']+'footer.html' ) )
