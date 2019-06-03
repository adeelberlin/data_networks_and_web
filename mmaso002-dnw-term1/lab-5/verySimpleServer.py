#!/usr/bin/env python3
# above 'she-bang' line makes the script executable from command line

""" A Very Simple Web Server
	Run with ./verySimpleServer.py
	Make sure all scripts are executable
	e.g. for single script:
		 chmod +x verySimpleServer.py
	or for a whole directory:
		 chmod -r +x htdocs/
"""

import http.server

PORT = 8000										# specifies the port number to accept connections on

server = http.server.HTTPServer					# instantiates an HTTP server object
handler = http.server.SimpleHTTPRequestHandler 	# instantiates a request handler object
server_address = ("", PORT)						# specifies server directory and port number

print("Starting server...")					# outputs a message 
httpd = server(server_address, handler)		# creates the server which will listen at the HTTP socket, dispatching requests to the handler
print("serving at port", PORT)				# outputs a message
httpd.serve_forever()						# puts program in infinite loop so that the server can `serve_forever'
