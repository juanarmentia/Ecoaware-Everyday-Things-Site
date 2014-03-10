
#!/usr/bin/env python

import sys, os
import couchdb
import time
from datetime import datetime
import datetime

"""
This function get the documents from a specific group.
Inside we create a dictionary (my_searches) whre the id,
date in python format and the content is allocated.
"""
def get_numcoffees_by_date(groupName, nDays):
	couch = couchdb.Server("http://130.206.138.42:57984")
	db    = couch['eco-aware_devices']
	dateKey     = 'date'
	timeKey     = 'time'
	dataKey     = 'data'
	numCoffees  = []
	strTemp = ''
	nCoffeesTemp = 0
	dateTemp = ''
	firstComparisonMade = False
	orderID = nDays-1
	dateTemp = ''
	nDaysComputed = 0
	nullCoffees = True;
	
	
	for i in range(0,nDays):
		relDate = datetime.date.today() - (nDays-i-1)*datetime.timedelta(days=1)
		numCoffees.append({'id': i, 'date': relDate,'numcoffees': 0})
		
	
	for row in db.view('getCoffesInfo/coffeeByGroup', descending=True, key=groupName): # we do use of a couchdb's view
		nullCoffees = False;
		info = db.get(row.id)
		dateTemp = info[dateKey]
		if strTemp != dateTemp:
			if firstComparisonMade:
				for orderID in range(0,nDays):
					if numCoffees[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': 0}):
						numCoffees[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': nCoffeesTemp})   #UPDATE
						nDaysComputed += 1
			strTemp = dateTemp
			nCoffeesTemp = 0
			firstComparisonMade = True
		nCoffeesTemp += 1
		dateTemp = ''
		if nDaysComputed==19:
			break
	if not nullCoffees:
		for orderID in range(0,nDays):
			if numCoffees[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': 0}):
				numCoffees[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': nCoffeesTemp})   #UPDATE
	nCoffeesTemp = 0
	sorted(numCoffees, key=lambda ident: ident['id'])
	
	return numCoffees


"""
This function get the documents from a specific group.
Inside we create a dictionary (my_searches) whre the id,
date in python format and the content is allocated.
"""
def get_coffees_by_date(groupName, nDays, nHours):
	couch = couchdb.Server("http://130.206.138.42:57984")
	db    = couch['eco-aware_devices']
	dateKey     = 'date'
	timeKey     = 'time'
	dataKey     = 'data'
	coffees  = []
	strTemp = ''
	nCoffeesTemp = 0
	dateTemp = ''
	firstComparisonMade = False
	orderID = nDays-1
	dateTemp = ''
	nDaysComputed = 0
	
	
	#for i in range(0,nDays):
	#	relDate = datetime.date.today() - (nDays-i-1)*datetime.timedelta(days=1)
	#	relTime = datetime.datetime.strptime("14:05:33", "%H:%M:%S").time()
	#	floatTime = round(float(relTime.hour) + (relTime.minute/60.0)+(relTime.second/3600.0), 2)
	#	coffees.append({'date': relDate,'time': floatTime})
	
	today=datetime.date.today()
	print today
	relDate = today - (nDays-1)*datetime.timedelta(days=1)
	for row in db.view('getCoffesInfo/coffeeByGroup', descending=True, key=groupName): # we do use of a couchdb's view
		info = db.get(row.id)
		
		try:
			date = datetime.datetime.strptime(info[dateKey], "%Y-%m-%d").date()
			time = datetime.datetime.strptime(info[timeKey], "%H:%M:%S").time()
			floatTime = round(float(time.hour) + (time.minute/60.0)+(time.second/3600.0), 2)
			if not(nHours==12 and (floatTime<7 or floatTime>19)):
				if date>=relDate and date<=datetime.date.today():
					coffees.append({'date': date,'time': floatTime})
		except:
			print "Unexpected error:", sys.exc_info()[0]
			
	#	if strTemp != dateTemp:
	#		if firstComparisonMade:
	#			for orderID in range(0,nDays):
	#				if numCoffees[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': 0}):
	#					numCoffees[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': nCoffeesTemp})   #UPDATE
	#					nDaysComputed += 1
	#		strTemp = dateTemp
	#		nCoffeesTemp = 0
	#		firstComparisonMade = True
	#	nCoffeesTemp += 1
	#	dateTemp = ''
	#	if nDaysComputed==19:
	#		break
	#for orderID in range(0,nDays):
	#	if numCoffees[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': 0}):
	#		numCoffees[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(),'numcoffees': nCoffeesTemp})   #UPDATE
	#nCoffeesTemp = 0
	#sorted(numCoffees, key=lambda ident: ident['id'])
	
	return coffees, today, relDate
	
	

def print_numcoffees_by_date(idcoffeemaker, nDays):
	#get_numcoffees_by_date(idcoffeemaker)
	for date in get_numcoffees_by_date(idcoffeemaker, nDays).keys():
		n = 1
		print "-",get_numcoffees_by_date(idcoffeemaker)[date],"coffees prepared on",date
	

if __name__ == "__main__":
	print_numcoffees_by_date('UDEUSTO', 20)
	print get_numcoffees_by_date('UDEUSTO', 20)
	