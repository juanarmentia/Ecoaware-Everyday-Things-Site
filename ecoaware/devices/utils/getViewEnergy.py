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
def get_energy_by_group(groupName, nDays):
	couch = couchdb.Server("http://130.206.138.42:57984")
	db    = couch['eco-aware_devices']
	dateKey     = 'date'
	timeKey     = 'time'
	dataKey     = 'data'
	accEnergy  = []
	strTemp = ''
	eWastedTemp = 0.0
	eEffectiveTemp = 0.0
	dateTemp = ''
	firstComparisonMade = False
	orderID = nDays-1
	dateTemp = ''
	
	for i in range(0,nDays):
		relDate = datetime.date.today() - (nDays-i-1)*datetime.timedelta(days=1)
		accEnergy.append({'id': i, 'date': relDate, 'wastedenergy': 0, 'effectiveenergy': 0})
		
	firstDate = datetime.date.today() - (nDays-1)*datetime.timedelta(days=1)
	
	for row in db.view('getGroupsInfo/byGroup', descending=True, key=groupName): # we do use of a couchdb's view 
		info = db.get(row.id)
		if datetime.datetime.strptime(info[dateKey], "%Y-%m-%d").date()<firstDate:
			for orderID in range(0,nDays):
				if accEnergy[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(), 'wastedenergy': 0, 'effectiveenergy': 0}):
					accEnergy[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(), 'wastedenergy': eWastedTemp, 'effectiveenergy': eEffectiveTemp})   #UPDATE
			break
		if info.has_key(dateKey) and info[dateKey] != "":
			if "-" in info[dateKey] and len(info[dateKey]) is 10:
				dateTemp = info[dateKey]
				if info.has_key(timeKey) and info[timeKey] != "":
					if type(info[timeKey]) is unicode:
						try:
							timeInDateTime = time.mktime(time.strptime(dateTemp+" "+info[timeKey], "%Y-%m-%d %H:%M:%S"))
						except:
							print "ERROR - %s %s %s"%(info[dateKey], info[timeKey], row.id)
		if strTemp != dateTemp:
			if firstComparisonMade:
				for orderID in range(0,nDays):
					if accEnergy[orderID]==({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(), 'wastedenergy': 0, 'effectiveenergy': 0}):
						accEnergy[orderID]=({'id': orderID, 'date': datetime.datetime.strptime(strTemp, "%Y-%m-%d").date(), 'wastedenergy': eWastedTemp, 'effectiveenergy': eEffectiveTemp})   #UPDATE
						#nDaysComputed += 1
			strTemp = dateTemp
			eWastedTemp = 0.0
			eEffectiveTemp = 0.0
			firstComparisonMade = True
		if info['consumption_type'] == 'COFFEE':
			eEffectiveTemp += float(info['energy_consumption_Wh'])
		else:
			eWastedTemp += float(info['energy_consumption_Wh'])
		dateTemp = ''
		
	eWastedTemp = 0.0
	eEffectiveTemp = 0.0
	sorted(accEnergy, key=lambda ident: ident['id'])
	
	return accEnergy


if __name__ == "__main__":
	#print_numcoffees_by_date('UDEUSTO')
	print get_energy_by_group('UDEUSTO',20)	