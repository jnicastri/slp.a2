#!/usr/bin/python
#!/usr/bin/env python


# Written by Dale Stanbrough 30th April 2015
# 


# this finds a matching GET/POST module/function to dispatch to
# based on a list of routes (declared in the routes file)

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

import sys
import importlib


import cgi

# the modules/functions to respond to incoming requests
from routes import routes


#--------------------------------
def getController(method, path):
	for each in routes():
		
		# each looks like ('get', '/', 'things::wow')
		if each[0].lower() == method.lower() and each[1].lower() == path.lower():
			moduleController  = each[2]
			break
	else:
		# didn't find a match
		raise ValueError

	# split this up, and get the module, function names
	middle =  moduleController.find('::');
	
	# get the module name
	moduleName = moduleController[:middle]
	# get the function name
	controllerName = moduleController[middle + 2:]


	module  = importlib.import_module(moduleName)
	methodToCall = getattr(sys.modules[moduleName], controllerName)

	return methodToCall
	
	


PORT_NUMBER = 34567	

# This class will handles any incoming request from
# the browser

class myHandler (BaseHTTPRequestHandler):
	
	# send a header...
	def sendHeader(self, code, mimetype):
		self.send_response(code)
		self.send_header('Content-type', mimetype)
		self.end_headers()
		
	#---------------------------------------------------------
	# Handler for the GET requests
	def do_GET(self):
		assetsDir = "assets"
		asset = False
		
		try:
			# Check the file extension required and
			# set the right mime type

			sendReply = False
			if self.path.endswith(".html") or self.path.endswith("/"):
				mimetype = 'text/html'
				sendReply = True

			elif self.path.endswith(".jpg"):
				mimetype = 'image/jpg'
				sendReply = True
				asset = True

			elif self.path.endswith(".png"):
				mimetype = 'image/png'
				sendReply = True
				asset = True
				
			elif self.path.endswith(".gif"):
				mimetype = 'image/gif'
				sendReply = True
				asset = True
				
			elif self.path.endswith(".js"):
				mimetype = 'application/javascript'
				sendReply = True
				asset = True
				
			elif self.path.endswith(".css"):
				mimetype = 'text/css'
				sendReply = True
				asset = True

			# It was a recognized type, send a reply
			
			if sendReply == True:
			
				
				# should we send an asset, or should we generate a page?
				if asset == True:
					self.sendHeader(200, mimetype)
					# Open the static file requested and send it
					# assets all live in an asset directory
					
					f = open(curdir + sep + assetsDir + sep + self.path) 
					self.wfile.write(f.read())
					f.close()
				else:
					
					try:
						self.sendHeader(200, mimetype)
						method = getController('GET', self.path)
						self.wfile.write(method())
					except:
						# doesn't seem to work for some reason...???
						self.send_error(404,'File Not Found: %s' % self.path)

			return

		except IOError, ValueError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#---------------------------------------------------------
	# Handler for the POST requests
	def do_POST(self):
			
		# get all the interesting goodness from the incoming post
		form = cgi.FieldStorage(
			fp = self.rfile, 
			headers = self.headers,
			environ = {'REQUEST_METHOD':'POST',
	                   'CONTENT_TYPE'  :'Content-Type',
					  },
			keep_blank_values = True
			)


		# move the cgi parameters (from the form) into a dictionary
		
		parameters = {}
		for key in form.keys():
			parameters[key] = form[key].value
		
		
		# create a response back to the web browser that
		# requested this page.
		# The reply should be a web page.

		# response headers
		
		self.send_response(200)
		self.send_header('Content-type','text/html')	
		self.end_headers()
		
		# identify a function that should be called to generate
		# the web page
		method = getController('POST', self.path)
		
		# call it with the cgi parameters from the form,
		# return this value as the main page
		
		self.wfile.write(method(parameters))

		return
			
try:
	# Create a web server and define the handler to manage the
	# incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	# Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
