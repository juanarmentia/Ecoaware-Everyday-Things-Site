#!/usr/bin/env python

import sys, os
import couchdb
import time
from datetime import datetime
import datetime
from collections import deque

groups_views      = {'Wikitoki':'Wikitoki', 'Ucrania':'Ucrania', 'LifeUD':'Life', 'MORElab':'MORElab','Compute':'Computing','Techabt':'Techabout','Bailen':'Bailen','Euskal':'Euskaltegi','Comunica':'Comunicacion','SGDTech':'ServiciosGenerales','Transprt':'Mobility','IEEC':'IEEC','Tlogica1':'Tlogica','Tlogica2':'Tlogica','Cowork3c':'Cowork3c'}
coffeeMakerStatus = {'RESET': -1, 'STANDBY': 0, 'START_TIME': 1, 'COFFEE': 2}
queue_status      = deque([])
forgottten_cost   = 40.534634
start_time_cost   = 7.452654
'''
This function is to control the queue where the previous operation modes of 
the coffee makers are stored. Its aim is to control whther someone has left the
coffee maker in standby mode after preparing a coffee.
'''
def addToQueue(con_type):
	if len(queue_status) < 2:
		queue_status.appendleft(coffeeMakerStatus[con_type])
	else:
		queue_status.pop()
		queue_status.appendleft(coffeeMakerStatus[con_type])


"""
This function get the documents from a specific group.
Inside we create a dictionary (my_searches) whre the id,
date in python format and the content is allocated.
"""
def get_personal_energy(groupName, rfid, nDays):
	couch = couchdb.Server("http://130.206.138.42:57984")
	db    = couch['eco-aware_devices']
	dateKey     = 'date'
	accEnergy   = []
	auxDate     = ''
	eWastedTemp    = 0.0
	eEffectiveTemp = 0.0
	firstComparisonMade   = False
	isThereConsumption    = False
	prevCoffeeMakerStatus = -1
	coffeeCounter         = 0
	strCoffee             = ''
	secondTest            = False	

	del accEnergy[:]
	
	for i in range(0,nDays):
		relDate = datetime.date.today() - (nDays-i-1)*datetime.timedelta(days=1)
		accEnergy.append({'id': i, 'date': relDate, 'wastedenergy': 0, 'effectiveenergy': 0})
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
					accEnergy[next(index for (index, d) in enumerate(accEnergy) if d["date"] == auxDate)]['wastedenergy']    = eWastedTemp
					accEnergy[next(index for (index, d) in enumerate(accEnergy) if d["date"] == auxDate)]['effectiveenergy'] = eEffectiveTemp
				eWastedTemp    = 0.0
				eEffectiveTemp = 0.0
				auxDate = tempDate
				isThereConsumption = False
			if info['consumption_type'] == 'RESET':
				prevCoffeeMakerStatus = coffeeMakerStatus['RESET']
				addToQueue(info['consumption_type'])
			#
			#if info['consumption_type'] == 'COFFEE':
			if info['userID'] == rfid:
				#print queue_status
				if(queue_status.count(0) == 2):
					print "[%s]: SE LA HA DEJADO ENCENDIDA!!!!! el dia %s a las %s" % (info['userID'], tempDate, info['time'])
					eWastedTemp += forgottten_cost
				addToQueue(info['consumption_type'])
				strCoffee =  str(tempDate) + " at " + info['time']
				print "Coffee energy cost: %s Wh. On %s" % (str(info['energy_consumption_Wh']), strCoffee)
				if secondTest:
					secondTest = False
					#print "COFFEE COUNTER: " + str(coffeeCounter) 
					#print "[SecondTest] Se estaba haciendo ya el coffee y no cuenta.\n"
				elif(prevCoffeeMakerStatus == coffeeMakerStatus['COFFEE']):
					secondTest = False
					#print "COFFEE COUNTER: " + str(coffeeCounter)
					#print "Se estaba haciendo ya el coffee y no cuenta.\n" #TODO: sumar consumos
				else:
					coffeeCounter += 1 #we only increase the coffee counter when the first capsule is prepared
				prevCoffeeMakerStatus = coffeeMakerStatus['COFFEE']
				eEffectiveTemp       += float(info['energy_consumption_Wh'])
				isThereConsumption    = True
			elif info['consumption_type'] == 'START_TIME':
				addToQueue(info['consumption_type'])
				if secondTest:
					#print "COFFEE COUNTER: " + str(coffeeCounter)
					#print "[SecondTest] La cafetera estaba apagada\n"
					eEffectiveTemp += start_time_cost*0.7
					eWastedTemp    += start_time_cost*0.3						
				if(prevCoffeeMakerStatus == coffeeMakerStatus['COFFEE']):
					eEffectiveTemp += start_time_cost*0.7
					eWastedTemp    += start_time_cost*0.3
					#print "COFFEE COUNTER: " + str(coffeeCounter)
					#print "La cafetera estaba apagada\n"	
				prevCoffeeMakerStatus = coffeeMakerStatus['START_TIME']				
				#eEffectiveTemp += float(start_time_cost)*0.7
				#eWastedTemp    += float(start_time_cost)*0.3
				isThereConsumption = True
				secondTest = False
			elif info['consumption_type'] == 'STANDBY':
				addToQueue(info['consumption_type'])
				if (prevCoffeeMakerStatus == coffeeMakerStatus['COFFEE']):
					if secondTest:
						#print "[SecondTest] La cafetera estaba encendida el %s\n" % (str(tempDate) + " at " + info['time'])
						prevCoffeeMakerStatus = coffeeMakerStatus['STANDBY']
						secondTest = False				
					else:
						secondTest = True
						eWastedTemp += float(info['energy_consumption_Wh'])
				isThereConsumption = True
		else:
			break
	#sorted(accEnergy, key=lambda ident: ident['id'])
	if isThereConsumption: 
		accEnergy[next(index for (index, d) in enumerate(accEnergy) if d["date"] == auxDate)]['wastedenergy']    = eWastedTemp
		accEnergy[next(index for (index, d) in enumerate(accEnergy) if d["date"] == auxDate)]['effectiveenergy'] = eEffectiveTemp
	print auxDate
	return accEnergy
if __name__ == "__main__":
	print get_personal_energy('LifeUD', '6900906A06', 10)	
