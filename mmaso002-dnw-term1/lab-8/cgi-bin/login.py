#!/usr/bin/env python3

"""
	This script handles the processing
	of the login form in the catflucks application.
	Note: 
		there is code repetition here...
		What could we do about that?
	Also note:
		this functionality is not yet integrated
		with the rest of the application.
		How could it be?
"""

# import modules from Python standard library
import cgi
import cgitb
cgitb.enable()
import bcrypt

# import custom modules
from config import config
import utils

# connect to database
db = utils.db_connect( config )

# tell the browser we are outputting HTML
print("Content-Type: text/html\n")

# get the form data
form = cgi.FieldStorage()

# check that login form was submitted
if 'btn_login' in form:
	# get the username from the form
	username = form['username'].value
	# look for an account with the username
	account = db.accounts.find_one({
		"username":username,
		})
	# check if an account came back 
	if account is not None:
		# get the unhashed password sent in the form
		pw = form['password'].value
		# compare the unhashed password from the form
		# with the hashed version in the database
		if bcrypt.checkpw( pw.encode('utf-8'), account['password'].encode('utf-8') ):
			# if they match, output a personal greeting
			response = "Hello {}!".format( account['name']['first'] )
		else:
			# if not, we know it was a wrong password
			response = "Wrong password."
	else:
		# their username didn't match, so tell them that
		response = "Sorry, I don't think I know you!"
	# for testing purposes, output the response here...
	print("<p>"+response+"</p>")
else:
	# they didn't come via the form, so tell them to go away!
	print("<p>How did you get here? Maybe you want to <a href='/cgi-bin/splash.py'>go back home</a>?</p>")
