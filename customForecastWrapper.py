#!/usr/bin/env python

# Student No. 3407908
# Student Name: James Nicastri
# Assignment 2
# Scripting Language Programming
# 2015, SP1


import json, httplib

BASE_URL = "api.forecast.io"

class ForecastIOObject(object):

	def __init__(self, apikey, lt, lg):
		self.apiKey = apikey
		self.lat = lt
		self.lng = lg
		


	def requestForecastByTime(self, dt, options):
		
		connection = httplib.HTTPSConnection(BASE_URL)
		connection.request("GET", "/forecast/" + self.apiKey + "/" + str(self.lat) + "," + str(self.lng) + "," + dt + options)

		return json.loads(connection.getresponse().read())
