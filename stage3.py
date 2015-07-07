#!/usr/bin/env python

# Student No. 3407908
# Student Name: James Nicastri
# Assignment 2
# Scripting Language Programming
# 2015, SP1


import sys, station, customForecastWrapper, datetime, time, stationCoOrds


def getForecastData(latLng, timeStr, dayNum, weekDim):

	API_KEY = ""
	fp = None

	# get API Key
	try:
		fp = open("forecastKey", "r")
		API_KEY = fp.readline()
		API_KEY = API_KEY.rstrip('\n')
	except:
		raise IOError("API Key Loading has failed")
	finally:
		if fp != None:
			fp.close()

	# getting time info for use later

	timeListStr = timeStr.split(':')
	
	#print(timeListStr)
	queryHour = int(timeListStr[0])
	queryMins = int(timeListStr[1][:2])

	if timeListStr[1][-2] == "P" or timeListStr[1][-2] == "p":
		if queryHour != 12:
			queryHour = queryHour + 12

	# working out day specifier

	dayOffsetFromToday = -1
	currentDayIndex = datetime.datetime.today().weekday()

	if weekDim == 1:
		if currentDayIndex > dayNum:
			dayOffsetFromToday = dayNum - currentDayIndex
		elif currentDayIndex == dayNum:
			dayOffsetFromToday = 0
		else:
			dayOffsetFromToday = currentDayIndex - dayNum
	else:
		dayOffsetFromToday = (7 - currentDayIndex) + dayNum 

	# build a query date
	dtNow = datetime.datetime.now()
	queryDate = dtNow + datetime.timedelta(days=dayOffsetFromToday)
	queryDateTime = queryDate.replace(hour=queryHour, minute=queryMins, second=0, microsecond=0)

	#spliting the lat long string
	latLngList = latLng.split(",")

	# create a forecast object	
	FIOObj = customForecastWrapper.ForecastIOObject(API_KEY, float("{0:.10f}".format(float(latLngList[0]))), float("{0:.10f}".format(float(latLngList[1]))))

	return FIOObj.requestForecastByTime(queryDateTime.isoformat(), "?units=si")


def getStationList():
	
	stationDict = {}	
	
	try:
		fp = open("google_transit/stops.txt", "r")

		fp.readline() #done to skip the heading line of the file

		for line in fp:
			fileLine = line.split(",", 5)
			stationName = fileLine[1]
			stationSuburb = stationName[stationName.find("(")+1:stationName.find(")")]
			cleanLat = fileLine[2].translate(None, "\"")
			cleanLong = fileLine[3].translate(None, "\"")
			cleanLong = cleanLong.translate(None, "\n")
			newStation = station.Station(stationName, stationSuburb, cleanLat, cleanLong)
			stationDict[stationSuburb] = newStation
	except:
		inLoadingError = True
	finally:
		if fp != None:	
			fp.close()	

	return stationDict

def getStationCoOrds(queryStationName):

	stationDict = {}	
	
	try:
		fp = open("coords.txt", "r")

		for line in fp:
			fileLine = line.split(",", 5)
			stationName = fileLine[0]
			x1 = fileLine[1]
			y1 = fileLine[2]
			x2 = fileLine[3]
			y2 = fileLine[4]
			newStation = stationCoOrds.stationCoOrds(x1, y1, x2, y2, stationName.lower())
			stationDict[stationName.lower()] = newStation
	except:
		raise IOError("Error loading map co-ordinates")
	finally:
		if fp != None:	
			fp.close()

	if queryStationName in stationDict.keys():
		return stationDict[queryStationName]
	else:
		return None	


