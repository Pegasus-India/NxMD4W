from Adafruit_I2C import Adafruit_I2C 
from MCP23017 import MCP23017 
import time
from datetime import datetime, timedelta, date 
from threading import Thread
from threading import Timer

import MySQLdb

import calendar
import os
import sys

import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

global lrt1
global dmt1
global alarmtime1
global doorsensor1
global doorname1

global lrt2
global dmt2
global alarmtime2
global doorsensor2
global doorname2

global lrt3
global dmt3
global alarmtime3
global doorsensor3
global doorname3

global lrt4
global dmt4
global alarmtime4
global doorsensor4
global doorname4

global xUD1
xUD1 = []

global xUD2
xUD2 = []

global xUD3
xUD3 = []

global xUD4
xUD4 = []

global firealarmtime
global auxalarmtime

global Jx1
Jx1 = []

#### Checking if MySQL is loaded, so that application can be launched
tt = 0
while tt < 100:
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		db.close()
		tt=100 
	except:       
		tt+=1
		time.sleep(1)
		if(tt==99):
			print("can not open database")
			sys.exit()
#### Even after 100 tries, if Mysql is not loaded, then exit the application

conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

sqlcon = "Select * from `Controller Parameters`"
cursor.execute (sqlcon)
condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		
		firealarmtime = rows['Fire Alarm Time']
		auxalarmtime = rows['Aux Alarm Time']
		

sqlcon = "Select * from `Door Parameter` where `Door No` = 1"
cursor.execute (sqlcon)
condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt1 = rows['Lock Release Time']
		dmt1 = rows['Lock Monitoring Time']
		alarmtime1 = rows['Alarm Time']
		doorsensor1 = rows['Door Sensor']
		doorname1 = rows['Door Name']
		
sqlcon = "Select * from `Door Parameter` where `Door No`= 2"
cursor.execute (sqlcon)
condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt2 = rows['Lock Release Time']
		dmt2 = rows['Lock Monitoring Time']
		alarmtime2 = rows['Alarm Time']
		doorsensor2 = rows['Door Sensor']
		doorname2= rows['Door Name']


sqlcon = "Select * from `Door Parameter` where `Door No` = 3"
cursor.execute (sqlcon)
condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt3 = rows['Lock Release Time']
		dmt3 = rows['Lock Monitoring Time']
		alarmtime3 = rows['Alarm Time']
		doorsensor3 = rows['Door Sensor']
		doorname3= rows['Door Name']

		
sqlcon = "Select * from `Door Parameter` where `Door No` = 4"
cursor.execute (sqlcon)
condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt4 = rows['Lock Release Time']
		dmt4 = rows['Lock Monitoring Time']
		alarmtime4 = rows['Alarm Time']
		doorsensor4 = rows['Door Sensor']
		doorname4 = rows['Door Name']		
		

if conn.open:
	cursor.close()
	del cursor
	conn.close()
	del conn
		
		
mcp = MCP23017(address = 0x20, num_gpios = 16) # MCP23017
print ("MCP Configured!")
		
inpin0 = 0
mcp.pinMode(inpin0, mcp.OUTPUT)


inpin1 = 1
mcp.pinMode(inpin1, mcp.OUTPUT)


inpin2 = 2
mcp.pinMode(inpin2, mcp.OUTPUT)


inpin3 = 3
mcp.pinMode(inpin3, mcp.OUTPUT)


inpin4 = 4
mcp.pinMode(inpin4, mcp.OUTPUT)

inpin5 = 5
mcp.pinMode(inpin5, mcp.OUTPUT)


inpin6 = 6
mcp.pinMode(inpin6, mcp.OUTPUT)


inpin7 = 7
mcp.pinMode(inpin7, mcp.OUTPUT)


inpin8 = 8
mcp.pinMode(inpin8, mcp.OUTPUT)


inpin9 = 9
mcp.pinMode(inpin9, mcp.OUTPUT)

def UnlockDoor1(lrt1):
	mcp.output(2, 1)
	x1LD = Timer(lrt1, LockDoor1,)
	x1LD.start()
	

def LockDoor1():
	mcp.output(2, 0)
	
	
def UnlockDoor2(lrt2):
	mcp.output(3, 1)
	x2LD = Timer(lrt2, LockDoor2,)
	x2LD.start()
	

def LockDoor2():
	mcp.output(3, 0)

def UnlockDoor3(lrt3):
	mcp.output(0, 1)
	x3LD = Timer(lrt3, LockDoor3,)
	x3LD.start()
		
def LockDoor3():
	mcp.output(0, 0)
	
def UnlockDoor4(lrt4):
	mcp.output(1, 1)
	x4LD = Timer(lrt4, LockDoor4,)
	x4LD.start()
	
	
def LockDoor4():
	mcp.output(1, 0)

def CloseFire():
	mcp.output(4, 0)  	# Fire Relay Opened
	mcp.output(2, 0)	# Lock Relay 1 Opened
	mcp.output(3, 0)	# Lock Relay 2 Opened
	mcp.output(0, 0)	# Lock Relay 3 Opened
	mcp.output(1, 0)	# Lock Relay 4 Opened
	
def OpenFire():
	mcp.output(4, 1)  	# Fire Relay Opened
	mcp.output(2, 1)	# Lock Relay 1 Opened
	mcp.output(3, 1)	# Lock Relay 2 Opened
	mcp.output(0, 1)	# Lock Relay 3 Opened
	mcp.output(1, 1)	# Lock Relay 4 Opened

def CloseAux():
	# time.sleep(auxalarmtime)
	mcp.output(5, 0)
	
def OpenAux():
	mcp.output(5, 1)
	xALD = Timer(auxalarmtime, CloseAux,)
	
	
def OpenDoor(doornumber):
	if doornumber == 1:
		xUD = Thread(target = UnlockDoor1, args=(lrt1,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
		
	elif doornumber == 2:
		xUD = Thread(target = UnlockDoor2, args=(lrt2,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
	elif doornumber == 3:
		xUD = Thread(target = UnlockDoor3, args=(lrt3,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
	elif doornumber == 4:
		xUD = Thread(target = UnlockDoor4, args=(lrt4,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()


while True:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)

	sqlcon = "Select * from `Controller Parameters`"
	cursor.execute (sqlcon)
	condata = cursor.fetchall()

	if len(condata) > 0:
		for rows in condata:
			
			firealarmtime = rows['Fire Alarm Time']
			auxalarmtime = rows['Aux Alarm Time']
			

	sqlcon = "Select * from `Door Parameter` where `Door No` = 1"
	cursor.execute (sqlcon)
	condata = cursor.fetchall()

	if len(condata) > 0:
		for rows in condata:
			lrt1 = rows['Lock Release Time']
			dmt1 = rows['Lock Monitoring Time']
			alarmtime1 = rows['Alarm Time']
			doorsensor1 = rows['Door Sensor']
			doorname1 = rows['Door Name']
			
	sqlcon = "Select * from `Door Parameter` where `Door No`= 2"
	cursor.execute (sqlcon)
	condata = cursor.fetchall()

	if len(condata) > 0:
		for rows in condata:
			lrt2 = rows['Lock Release Time']
			dmt2 = rows['Lock Monitoring Time']
			alarmtime2 = rows['Alarm Time']
			doorsensor2 = rows['Door Sensor']
			doorname2= rows['Door Name']


	sqlcon = "Select * from `Door Parameter` where `Door No` = 3"
	cursor.execute (sqlcon)
	condata = cursor.fetchall()

	if len(condata) > 0:
		for rows in condata:
			lrt3 = rows['Lock Release Time']
			dmt3 = rows['Lock Monitoring Time']
			alarmtime3 = rows['Alarm Time']
			doorsensor3 = rows['Door Sensor']
			doorname3= rows['Door Name']

			
	sqlcon = "Select * from `Door Parameter` where `Door No` = 4"
	cursor.execute (sqlcon)
	condata = cursor.fetchall()

	if len(condata) > 0:
		for rows in condata:
			lrt4 = rows['Lock Release Time']
			dmt4 = rows['Lock Monitoring Time']
			alarmtime4 = rows['Alarm Time']
			doorsensor4 = rows['Door Sensor']
			doorname4 = rows['Door Name']		
			
	sqlsetup = "Select * from `Emergency`"
	cursor.execute(sqlsetup)
	result = cursor.fetchall()
	if len(result) > 0:
		for rows in result:
			doornumber = rows['Door Number']
			rid = rows['RowID']
			fo = rows['Fire Open']
			fc = rows['Fire Close']
			ao = rows['Aux Open']
			ac = rows['Aux Close']
			print "Door Number: ", doornumber
			print "Fire Open: ", fo
			print "Fire Close: ", fc
			print "Aux Open: ", ao
			print "Aux Close :", ac
			
			if doornumber <> '':
				print "Opening Lock Number: ", doornumber 
				OpenDoor(doornumber)
				
			
			if fo == 1:
				print "Activating Fire Alarm"
				OpenFire()
			
			if fc == 1:
				print "Deactivating Fire Alarm"
				CloseFire()
				
			if ao == 1:
				print "Activating Aux Alarm"
				OpenAux()
			
			if ac == 1:
				print "Deactivating Aux Alarm"
				CloseAux()
				
			
			sqldel = "Delete from `Emergency` where `RowID` = " + str(rid)
			cursor.execute(sqldel)
			conn.commit()
	
	cursor.close()
	del cursor
	conn.close()
	time.sleep (1)