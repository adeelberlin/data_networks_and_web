# Lab 9: Template README

Here is a template README file you could include in your final app submission, so that your marker knows exactly where to look for evidence of your learning.

Doing this is another way of showing that you understand the code you wrote!

**Note:** They will also be looking at your commit history, to see how much of the app you wrote from scratch.

## Evidence

| Checklist point | Evidence (filename(s) and line number(s) and/or short desciption) |
|-------------|------------|
| write a simple server script which is capable of serving a web application written in Python |	|
| retrieve one or more documents or rows from one or more collections or tables |	|
| iterate over documents returned in a results cursor object |	|
| filter and/or sort documents in the result set based on some simple criteria |	|
| perform more advanced filtering and/or aggregation operations in a database query |	|
| handle a POST request made via an HTML form in a server-side script |	|
| demonstrate consideration for Separation of Concerns through the modularisation (separation) of related code |	|
| demonstrate an awareness of how related data is modelled in the database |	|
| design and implement an original functional feature in a Python web app |	|
| other relevant extension of the taught material (if applicable) |	|
| make a Python script self-executable |	|
| utilise a range of Python's built-in functions and methods |	|
| make use of user-defined functions |	|
| design and implement reuseable functions |	|
| write readable, well-presented code | Everywhere?! |

## Installation instructions

If you have used any modules or configured any global variables that a tester of your app should be aware of, please detail them here.

For example, in the case of this example app:

+ The app requires Python 3+ and MongoDB 3.2 or later
+ The bcrypt and pymongo modules should be are available from your python environment
+ You should open and set the variables in cgi-bin/config.py to match your configuration
+ To launch,

		./simpleServer.py 
+ Restore the database by running `mongorestore` from the base directory
+ After restoring the database, you can test the app with these login credentials:
	- Username: tester
	- Password: password
