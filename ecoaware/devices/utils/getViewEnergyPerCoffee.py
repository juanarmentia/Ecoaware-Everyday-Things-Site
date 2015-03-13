#!/usr/bin/env python

import sys, os
import couchdb
import time
from datetime import datetime
import datetime


groups_views = {'Wikitoki':'Wikitoki', 'Ucrania':'Ucrania', 'LifeUD':'Life', 'MORElab':'MORElab','Compute':'Computing','Techabt':'Techabout','Bailen':'Bailen','Euskal':'Euskaltegi','Comunica':'Comunicacion','SGDTech':'ServiciosGenerales','Transprt':'Mobility','IEEC':'IEEC','Tlogica1':'Tlogica','Tlogica2':'Tlogica','Cowork3c':'Cowork3c'}
"""
This function get the documents from a specific group.
Inside we create a dictionary (my_searches) whre the id,
date in python format and the content is allocated.
"""
def get_coffee_cost_by_group(groupName, nDays):
	couch = couchdb.Server("http://130.206.138.42:57984")
	db    = couch['eco-aware_devices']
	dateKey     = 'date'
	accEnergy   = []
	auxDate     = ''
	eEffectiveTemp  = 0.0
	eEffectiveTotal = 0.0
	coffee_num      = 0.0
	firstComparisonMade = False
	isThereConsumption  = False

	del accEnergy[:]
	
	for i in range(0,nDays):
		relDate = datetime.date.today() - (nDays-i-1)*datetime.timedelta(days=1)
		accEnergy.append({'id': i, 'date': relDate, 'effectiveenergy': 0, 'average': 0})
	lastDate = relDate
	firstDate = datetime.date.today() - (nDays-1)*datetime.timedelta(days=1)
	indexCount = 0
	#for row in db.view('getGroupsInfo/byDate', descending=True, key=groupName): # we do use of a couchdb's view 
	for row in db.view('getGroupsInfo/'+groups_views[groupName], descending=True): # we do use of a couchdb's view 
		info     = db.get(row.id)
		tempDate = datetime.datetime.strptime(info[dateKey], "%Y-%m-%d").date()
		if tempDate >= firstDate:
			if tempDate != auxDate:
				if isThereConsumption: 
					if coffee_num == 0:
						coffee_num = 1
					accEnergy[next(index for (index, d) in enumerate(accEnergy) if d["date"] == auxDate)]['effectiveenergy'] = eEffectiveTemp/coffee_num
					eEffectiveTotal += eEffectiveTemp/coffee_num
				eEffectiveTemp = 0.0
				coffee_num     = 0
				auxDate = tempDate
				isThereConsumption = False
			if info['consumption_type'] == 'COFFEE':
				coffee_num += 1
			eEffectiveTemp += float(info['energy_consumption_Wh'])
			isThereConsumption = True
		else:
			break
	for (index, d) in enumerate(accEnergy):
		accEnergy[index]['average'] = eEffectiveTotal/nDays
	return accEnergy

if __name__ == "__main__":
	#print_numcoffees_by_date('UDEUSTO')
	print get_coffee_cost_by_group('LifeUD',10)	
