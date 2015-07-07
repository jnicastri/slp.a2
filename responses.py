#!/usr/bin/env python

# Student No. 3407908
# Student Name: James Nicastri
# Assignment 2
# Scripting Language Programming
# 2015, SP1

import stage3, time
from PIL import Image, ImageDraw, ImageFont

def forecast():
		
	data = stage3.getStationList()
	
	out = "<html><head><title>Stage3 Weather Forecast</title><style>.field{width:600px;}</style></head><body>\n"
	out += "<h1>Melbourne Train Station Weather Forecast</h1>"
	out += "<form action=\"http://127.0.0.1:34567/forecast/result\" method=\"POST\">\n"
	out += "<fieldset class=\"field\"><legend>Choose a destination station:</legend>"
	out += "<select name=\"stationSelect\">"
	
	for key in data.keys():
		out += "<option value=\"" + data[key].stationSuburbName + "," + str(data[key].lat) + "," + str(data[key].lng) + "\">" + data[key].stationSuburbName + "</option>\n"

	out += "</select></fieldset><br /><br />\n"
	
	out += "<fieldset class=\"field\"><legend>Choose a day:</legend>\n"
	out += "<select name=\"daySelect\">"
	out += "<option value=\"1\">Monday</option>\n"
	out += "<option value=\"2\">Tuesday</option>\n"
	out += "<option value=\"3\">Wednesday</option>\n"
	out += "<option value=\"4\">Thursday</option>\n"
	out += "<option value=\"5\">Friday</option>\n"
	out += "<option value=\"6\">Saturday</option>\n"
	out += "<option value=\"7\">Sunday</option>\n"
	out += "</select>\n"

	out += "&nbsp;&nbsp;"
	
	out += "<select name=\"dimSelect\">"
	out += "<option value=\"1\">This Week</option>\n"
	out += "<option value=\"2\">Next Week</option>\n"
	out += "</select></fieldset><br /><br />\n"

	out += "<fieldset class=\"field\"><legend>Enter a time:</legend>\n"
	out += "<input type=\"time\" placeholder=\"12-hour time. eg: 1:24pm\" name=\"timeTb\" required />\n"
	out += "</fieldset><br /><br />\n"
	
	
	out += "<input type=\"submit\" value=\"Submit\">\n"
	out += "</form></body></html>"

	return out



def forecastresult(form):
	
	#validate time format
	
	try:
		time.strptime(form["timeTb"], "%I:%M%p")
	except ValueError:
		return "Time is not in a valid format!"

		
	selectList = form["stationSelect"].split(",")
	queryParams = selectList[1] + "," + selectList[2]	

	# request some forecast data
	dataSource = None
	
	try:
		dataSource = stage3.getForecastData(queryParams, form["timeTb"], int(form["daySelect"]), int(form["dimSelect"]))
	except IOError as e:
		return str(e)
		
	out = ""
	out += "<html><head><title>Stage3 Weather Forecast Results</title><style>.field{width:600px;}</style></head><body>\n"
	out += "<h1>Weather Forecast Results</h1>\n"
	out += "<fieldset class=\"field\"><legend>Results</legend>"
	out += "<strong>Summary:</strong>&nbsp;" + dataSource["currently"]["summary"] + "<br />\n"
	out += "<strong>Temperature:</strong>&nbsp;" + str(dataSource["currently"]["temperature"]) + "<br />\n"
	out += "<strong>Apparent Temperature:</strong>&nbsp;" + str(dataSource["currently"]["apparentTemperature"]) + "<br />\n"
	out += "<strong>Dew Point:</strong>&nbsp;" + str(dataSource["currently"]["dewPoint"]) + "<br />\n"
	out += "<strong>Humidity:</strong>&nbsp;" + str(dataSource["currently"]["humidity"]) + "<br />\n"
	out += "<strong>Wind Speed:</strong>&nbsp;" + str(dataSource["currently"]["windSpeed"]) + "<br />\n"
	out += "<strong>Wind Bearing:</strong>&nbsp;" + str(dataSource["currently"]["windBearing"]) + "<br />\n"
	out += "<strong>Cloud Cover:</strong>&nbsp;" + str(dataSource["currently"]["cloudCover"]) + "<br />\n"
	out += "</fieldset><br />"

	try:
		selectionCoOrds = stage3.getStationCoOrds(selectList[0].lower())
	except IOError as e:
		out += str(e) + "<br />"
	
	if selectionCoOrds != None:
		
		original = Image.open("assets/sourceMap.png").convert("RGBA")
		original.load()
		drawing = ImageDraw.Draw(original)
		
		coOrdsTuple = (float(selectionCoOrds.x1),float(selectionCoOrds.y1),float(selectionCoOrds.x2),float(selectionCoOrds.y2))

		drawing.rectangle(coOrdsTuple, fill=None, outline="red")
		del drawing

		original.save("assets/outImg.png")

		out += "<br /><img src=\"../outImg.png\" alt=\"Map Image\" /></br />"
	
	out += "<a href=\"/\">Get another forecast</a>"
	out += "<br /><br />Powered by <a href=\"http://forecast.io/\">Forecast</a><br /><br />"

	out += "</body></html>"
	return out

