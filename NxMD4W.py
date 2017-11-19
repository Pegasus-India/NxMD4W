#!/usr/bin/env python
from Adafruit_I2C import Adafruit_I2C 
from MCP23017 import MCP23017 
import time
from datetime import datetime, timedelta, date 
from threading import Thread
from threading import Timer

#import sqlite3
import pyodbc
import MySQLdb

import calendar
import os
import sys

import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

global Ex1
Ex1 = []

global Jx1
Jx1 = []

global xC1
xC1 = []

global xUD1
xUD1 = []

global xUD2
xUD2 = []

global xUD3
xUD3 = []

global xUD4
xUD4 = []

global xOA1
xOA1 = []

global xOA2
xOA2 = []

global xOA3
xOA3 = []

global xOA4
xOA4 = []

global xODG
xODG = []

global xOAG
xOAG = []

global xL1
xL1 = []

global dataT
dataT = []

global xI1
xI1 = []

global T1			# Timer for Door sensor 1
global T2			# Timer for Door sensor 2
global T3			# Timer for Door sensor 3
global T4			# Timer for Door sensor 4

global dr1			# A Flag to check if lock 1 is released
global dr2			# A Flag to check if lock 1 is released
global dr3			# A Flag to check if lock 1 is released
global dr4			# A Flag to check if lock 1 is released

# initializing dr flags
dr1 = 0
dr2 = 0
dr3 = 0
dr4 = 0

global cid			# Controller ID
global cname		# Controller name
global psn			# product Serial Number
global model		# Model

global lrt1			# Lock Release Time Door 1
global dmt1			# Door monitoring time, door 1
global alarmtime1	# Alarm Time Door 1
global doorsensor1	# Door Sensor Type, Door 1
global doorname1	# Door 1 Name

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

global firealarmtime
global auxalarmtime

global interlock
interlock = 0

global mssql1
mssql1 =[]

global mysql1
mysql1 = []

global ServerDSN
ServerDSN = []

global UID
UID = []

global PWD
PWD = []

global i
i = 0

global j
j = 0

global k
k = 0

global dt

global ServerDSNMySQL
ServerDSNMySQL = []

global hstMySQL
hstMySQL = []

global UIDMysQL
UIDMysQL = []

global PWDMySQL
PWDMySQL = []

global dBMySQL
dBMySQL = []

global ptMySQL
ptMySQL = []

global UpdateURL
UpdateURL = []

global url
url = []

global sqlMSSQL

global sqlMySQL

global updateURL
updateURL = 0

global updateMSSQL
updateMSSQL = 0

global updateMYSQL
updateMYSQL = 0

global attendance1
attendance1 = 0

global attendance2
attendance2 = 0

global attendance3
attendance3 = 0

global attendance4
attendance4 = 0

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

tt = 0
while tt < 100:
	try:
		db = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		db.close()
		del db
		tt=100 
	except:       
		tt+=1
		time.sleep(1)
		if(tt==99):
			print("Unable to connect to Database! Quitting...")
			sys.exit()
#### Even after 100 tries, if Mysql is not loaded, then exit the application


conpsn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="PSN", port=3306)
curpsn = conpsn.cursor(MySQLdb.cursors.DictCursor)
sqlpsn = "Select * from `PSN`"

if conpsn.open:
	try:
		if conpsn.open:
			try:
				curpsn.execute (sqlpsn)
			except MySQLdb.OperationalError:
				cursor.close()
				del cursor
				conpsn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="PSN", port=3306)
				curpsn = conpsn.cursor(MySQLdb.cursors.DictCursor)
				curpsn.execute (sqlpsn)
		else:
			conpsn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="PSN", port=3306)
			curpsn = conpsn.cursor(MySQLdb.cursors.DictCursor)
			curpsn.execute (sqlpsn)
		
		psndata = curpsn.fetchall()
		
		
		if len(psndata) > 0:
			for rows in psndata:
				psn = rows['PSN']
				model = rows['Model']
		else:
			psn = "PEPL20170915001"
			model = "NxMD4W"
	except:
		conpsn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="PSN", port=3306)
		curpsn = conpsn.cursor(MySQLdb.cursors.DictCursor)
		curpsn.execute (sqlpsn)
		psndata = curpsn.fetchall()
		if len(psndata) > 0:
			for rows in psndata:
				psn = rows['PSN']
				model = rows['Model']
		else:
			psn = "PEPL20170915001"
			model = "NxMD4W"

curpsn.close()
del curpsn
conpsn.close()
del conpsn

conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

sqlcon = "Select * from `Controller Parameters`"
if conn.open:
	try:
		cursor.execute (sqlcon)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlcon)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlcon)

condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		cid = rows['Controller ID']
		cname = rows['Controller Name']
		interlock = rows['Interlock']
		firealarmtime = rows['Fire Alarm Time']
		auxalarmtime = rows['Aux Alarm Time']
		
		
if interlock == None:
	interlock = 0
#print "Interlock Config = ", interlock
		
sqlcon = "Select * from `Door Parameter` where `Door No` = 1"
if conn.open:
	try:
		cursor.execute (sqlcon)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlcon)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlcon)

condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt1 = rows['Lock Release Time']
		dmt1 = rows['Lock Monitoring Time']
		alarmtime1 = rows['Alarm Time']
		doorsensor1 = rows['Door Sensor']
		doorname1 = rows['Door Name']
		attendance1 = rows['Attendance']
else:
	lrt1 = 0
	dmt1 = 0
	alarmtime1 = 0
	doorsensor1 = ""
	doorname1 = ""
	attendance1 = 0
	
sqlcon = "Select * from `Door Parameter` where `Door No` = 2"
if conn.open:
	try:
		cursor.execute (sqlcon)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlcon)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlcon)

condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt2 = rows['Lock Release Time']
		dmt2 = rows['Lock Monitoring Time']
		alarmtime2 = rows['Alarm Time']
		doorsensor2 = rows['Door Sensor']
		doorname2= rows['Door Name']
		attendance2 = rows['Attendance']
else:
	lrt2 = 0
	dmt2 = 0
	alarmtime2 = 0
	doorsensor2 = ""
	doorname2 = ""
	attendance2 = 0

sqlcon = "Select * from `Door Parameter` where `Door No` = 3"
if conn.open:
	try:
		cursor.execute (sqlcon)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlcon)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlcon)

condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt3 = rows['Lock Release Time']
		dmt3 = rows['Lock Monitoring Time']
		alarmtime3 = rows['Alarm Time']
		doorsensor3 = rows['Door Sensor']
		doorname3= rows['Door Name']
		attendance3 = rows['Attendance']
else:
	lrt3 = 0
	dmt3 = 0
	alarmtime3 = 0
	doorsensor3 = ""
	doorname3 = ""
	attendance3 = 0
	
sqlcon = "Select * from `Door Parameter` where `Door No` = 4"
if conn.open:
	try:
		cursor.execute (sqlcon)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlcon)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlcon)

condata = cursor.fetchall()

if len(condata) > 0:
	for rows in condata:
		lrt4 = rows['Lock Release Time']
		dmt4 = rows['Lock Monitoring Time']
		alarmtime4 = rows['Alarm Time']
		doorsensor4 = rows['Door Sensor']
		doorname4 = rows['Door Name']		
		attendance4 = rows['Attendance']
else:
	lrt4 = 0
	dmt4 = 0
	alarmtime4 = 0
	doorsensor4 = ""
	doorname4 = ""
	attendance4 = 0
	
#print "Lock Release Time = ", lrt1, lrt2, lrt3, lrt4
#print "Door Monitor Time = ", dmt1, dmt2, dmt3, dmt4
#print "Alarm Time = ", alarmtime1, alarmtime2, alarmtime3, alarmtime4
#print "Door Sensor Details = ", doorsensor1, doorsensor2, doorsensor3, doorsensor4
#print "Door Name = ", doorname1, doorname2, doorname3, doorname4
#print "Door Sensor status = ", dr1, dr2, dr3, dr4
		
#MSSQL
sqltemp = "Select * from `MSSQL`"
if conn.open:
	try:
		cursor.execute (sqltemp)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqltemp)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqltemp)

result = cursor.fetchall()
#print "table opened"

if len(result) > 0:
		updateMSSQL = 1
		for rows in result:
			ServerDSN.append(i)
			UID.append(i)
			PWD.append(i)
			ServerDSN[i] = rows['ServerDSN']
			UID[i] =  rows['UID']
			PWD[i] = rows['PWD']
			#print ServerDSN[i], UID[i], PWD[i]
			i = i + 1
#print "MS SQL Info Obtained Successfully!"

#MySQL
sqltemp = "Select * from `MYSQL`"
if conn.open:
	try:
		cursor.execute (sqltemp)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqltemp)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqltemp)


result = cursor.fetchall()
#print "table opened"

if len(result) > 0:
		updateMYSQL = 1
		for rows in result:
			
			hstMySQL.append(j)
			UIDMysQL.append(j)
			PWDMySQL.append(j)
			dBMySQL.append(j)
			ptMySQL.append(j)
						
			hstMySQL[j] = rows['Hostname']
			UIDMysQL[j] =  rows['UID']
			PWDMySQL[j] = rows['PWD']
			dBMySQL[j] = rows['Database']
			ptMySQL[j] = rows['Port']
			#print ServerDSN[i], UID[i], PWD[i]
			j = j + 1
			#host=hstMySQL[x], user=UIDMysQL[x], passwd=PWDMySQL[x], db=dBMySQL[x], port=int(ptMySQL[x])
#print "My SQL DB info obtained Successfully!"


# HTTP Cloud
sqlCloud = "Select * from `URL` where `Update Cloud` = 1"
if conn.open:
	try:
		cursor.execute (sqlCloud)
	except MySQLdb.OperationalError:
		cursor.close()
		del cursor
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlCloud)
else:
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute (sqlCloud)


urlResult = cursor.fetchall()

if len(urlResult) > 0:
	for rows in urlResult:
		UpdateURL.append(k)
		url.append(k)
		
		if rows['Update Cloud'] == 1:
			UpdateURL = 1
		else:
			UpdateURL = 0
				
		url = rows['url']
		#url = 'http://pegasus.16mb.com/recTXN.php?'
		k = k + 1
#print "Cloud DB Info Obtained Successfully!"


if conn.open:
	cursor.close()
	del cursor
	conn.close()
	del conn


def UnlockDoor1(lrt1):
	mcp.output(2, 1)
	x1LD = Timer(lrt1, LockDoor1,)
	x1LD.start()
	

def LockDoor1():
	mcp.output(2, 0)
	dr1 = 2
	
def UnlockDoor2(lrt2):
	mcp.output(3, 1)
	x2LD = Timer(lrt2, LockDoor2,)
	x2LD.start()
	

def LockDoor2():
	mcp.output(3, 0)
	dr2 = 2

def UnlockDoor3(lrt3):
	mcp.output(0, 1)
	x3LD = Timer(lrt3, LockDoor3,)
	x3LD.start()
		
def LockDoor3():
	mcp.output(0, 0)
	dr3 = 2
	
def UnlockDoor4(lrt4):
	mcp.output(1, 1)
	x4LD = Timer(lrt4, LockDoor4,)
	x4LD.start()
	
	
def LockDoor4():
	mcp.output(1, 0)
	dr4 = 2

def Alarm1(alarmtime1):
	mcp.output(9, 1)
	x1CA = Timer(alarmtime1, CloseAlarm1,)
	x1CA.start()
	
def CloseAlarm1():
	mcp.output(9, 0)

def Alarm2(alarmtime2):
	mcp.output(7, 1)
	x2CA = Timer(alarmtime2, CloseAlarm2,)
	x2CA.start()
	
def CloseAlarm2():
	mcp.output(7, 0)
	
def Alarm3(alarmtime3):
	mcp.output(8, 1)
	x3CA = Timer(alarmtime3, CloseAlarm3,)
	x3CA.start()
	
def CloseAlarm3():
	mcp.output(8, 0)
	
def Alarm4(alarmtime4):
	mcp.output(6, 1)
	x4CA = Timer(alarmtime4, CloseAlarm4,)
	x4CA.start()
	
def CloseAlarm4():
	mcp.output(6, 0)
	
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
	
	
def OpenAlarm(doornumber):
	print "Opening Alarm Output"
	print "Alarm Relay Number = ", doornumber
	if doornumber == 1:
		xL = Thread(target = Alarm1, args=(alarmtime1,))
		xL1.append(xL)
		xL.start()
		xL.join()
		
	elif doornumber == 2:
		xL = Thread(target = Alarm2, args=(alarmtime2,))
		xL1.append(xL)
		xL.start()
		xL.join()
	elif doornumber == 3:
		xL = Thread(target = Alarm3, args=(alarmtime3,))
		xL1.append(xL)
		xL.start()
		xL.join()
	elif doornumber == 4:
		xL = Thread(target = Alarm4, args=(alarmtime4,))
		xL1.append(xL)
		xL.start()
		xL.join()

def Interlock(interlock, doornumber):
	if interlock == 12:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor2
		elif doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor2
	elif interlock == 13:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor3
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor1
	elif interlock == 14:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor1		
	elif interlock == 23:
		if doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor3
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor2
	elif interlock == 24:
		if doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor2
	elif interlock == 34:
		if doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor3	
	elif interlock == 123:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor2
			LockDoor3
		elif doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor1
			LockDoor3
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor1
			LockDoor2
	elif interlock == 124:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor2
			LockDoor4
		elif doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor1
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor1
			LockDoor2	
	elif interlock == 134:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor3
			LockDoor4
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor1
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor1
			LockDoor3	
	elif interlock == 234:
		if doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor3
			LockDoor4
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor2
			LockDoor4
		elif doornumber == 4:
			UnlockDoor4(lrt4)
			LockDoor2
			LockDoor3		
	elif interlock == 1234:
		if doornumber == 1:
			UnlockDoor1(lrt1)
			LockDoor2
			LockDoor3
			LockDoor4
		elif doornumber == 2:
			UnlockDoor2(lrt2)
			LockDoor1
			LockDoor3
			LockDoor4
		elif doornumber == 3:
			UnlockDoor3(lrt3)
			LockDoor1
			LockDoor2
			LockDoor4
		elif doornumber == 3:
			UnlockDoor4(lrt4)
			LockDoor1
			LockDoor2
			LockDoor3	
			
def OpenDoor(doornumber):
	dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if doornumber == 1:
		xUD = Thread(target = UnlockDoor1, args=(lrt1,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
		dr1 = 1
		T1 = dt
	elif doornumber == 2:
		xUD = Thread(target = UnlockDoor2, args=(lrt2,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
		dr2 = 1
		T2 = dt
	elif doornumber == 3:
		xUD = Thread(target = UnlockDoor3, args=(lrt3,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
		dr3 = 1
		T3 = dt
	elif doornumber == 4:
		xUD = Thread(target = UnlockDoor4, args=(lrt4,))
		xUD1.append(xUD)
		xUD.start()
		xUD.join()
		dr4 = 1
		T4 = dt
		
		
def Reset1():
	# IP Address Reset
	conn1 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor1 = conn1.cursor(MySQLdb.cursors.DictCursor)
	
	sql = "Update `Controller Parameters` Set "
	sql = sql + "`IP Address` = '192.168.1.103', "
	sql = sql + "`Subnet` = '255.255.255.0', "
	sql = sql + "`Gateway` = '192.168.1.1', "
	sql = sql + "`WiFi IP Address` = '192.168.1.105', "
	sql = sql + "`WiFi Gateway` = '192.168.1.1', "
	sql = sql + "`WiFi SSID` = 'Pegasus Cable', "
	sql = sql + "`WiFi PWD` = '1234567890', "
	sql = sql + "`WiFi KeyManagement` = 'WPA2-PSK', "
	sql = sql + "`Updated` = 0"
	
	if conn1.open:
		try:
			cursor1.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor1.close()
			del cursor1
			conn1 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor1 = conn1.cursor(MySQLdb.cursors.DictCursor)
			cursor1.execute (sql)
	else:
		conn1 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor1 = conn1.cursor(MySQLdb.cursors.DictCursor)
		cursor1.execute (sql)
	conn1.commit()
	
	print "IP Address Reset Successfully!"
	time.sleep(2)
	print "Rebooting Now!"
	
	if conn1.open:
		cursor1.close()
		del cursor1
		conn1.close()
		del conn1
	
	os.system("sudo reboot -h now")

def Reset2():
	# Factory Reset to Default Values
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		
		
	# IP Address Reset
	sql = "Update `Controller Parameters` Set "
	sql = sql + "`IP Address` = '192.168.1.103', "
	sql = sql + "`Subnet` = '255.255.255.0', "
	sql = sql + "`Gateway` = '192.168.1.1', "
	sql = sql + "`WiFi IP Address` = '192.168.1.105', "
	sql = sql + "`WiFi Gateway` = '192.168.1.1', "
	sql = sql + "`WiFi SSID` = 'Pegasus Cable', "
	sql = sql + "`WiFi PWD` = '1234567890', "
	sql = sql + "`WiFi KeyManagement` = 'WPA2-PSK', "
	sql = sql + "`Updated` = 0"
	
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "IP Address Reset Successfully!"
	
	# Controller Info Reset
	sql = ""
	sql = "Delete from `Door Parameter`"
	
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
		
	print "Door Parameter Reset Successfully!"
	
	# Deleting data from other tables
	
	# Client Details Table
	sql = ""
	sql = "Delete from `Client Details`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Client Details Table Deleted!"
	
	
	# Emergency Table
	sql = ""
	sql = "Delete from `Emergency`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Emergency Table Deleted!"
	
	# Employee Enroll Info
	sql = ""
	sql = "Delete from `Enroll Info`"
	cursor.execute(sql)
	conn.commit()
	print "Data from Enroll Info Table Deleted!"
	
	# Employee TimeZone Table
	sql = ""
	sql = "Delete from `Employee TimeZone`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Employee Timezone Table Deleted!"
	
	# Holidays Table
	sql = ""
	sql = "Delete from `Holidays`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Holidays Table Deleted!"
	
	
	# Antipassback Log Table
	sql = ""
	sql = "Delete from `Antipassback Log`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	
	conn.commit()
	print "Data from Antipassback Log Table Deleted!"
	
	# Installer Details Table
	sql = ""
	sql = "Delete from `Installer Details`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Installer Details Table Deleted!"
	
	
	# Antipassback Group Table
	sql = ""
	sql = "Delete from `Anti Passback Group`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	
	conn.commit()
	print "Data from Antipassback Log Table Deleted!"
	
	# HTTP Error Transaction
	sql = ""
	sql = "Delete from `HTTP Error Txn`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from HTTP-Error-Txn Table Deleted!"
	
	# MS SQL 
	sql = ""
	sql = "Delete from `MSSQL`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from MSSQL Table Deleted!"
	
	# MS SQL Error Transaction
	sql = ""
	sql = "Delete from `MSSQL Error Txn`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from MSSQL Error Txn Table Deleted!"
	
	# MYSQL
	sql = ""
	sql = "Delete from `MYSQL`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from MYSQL Table Deleted!"
	
	# MYSQL Error Transaction
	sql = ""
	sql = "Delete from `MYSQL Error Txn`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from MYSQL Error Txn Table Deleted!"
	
	# Management Log Transaction
	sql = ""
	sql = "Delete from `Management Log`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Management Log Table Deleted!"
	
	# Time Zone
	sql = ""
	sql = "Delete from `Time Zone`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Timezone Table Deleted!"
	
	# Txn
	sql = ""
	sql = "Delete from `Txn`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from Txn Table Deleted!"
	
	# URL
	sql = ""
	sql = "Delete from `URL`"
	if conn.open:
		try:
			cursor.execute(sql)
			
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sql)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sql)
	conn.commit()
	print "Data from URL Table Deleted!"
	
	
	print "Factory Reset Completed Successfully!"
	time.sleep(2)
	
	print "Rebooting Now!"
	
	if conn.open:
		cursor.close()
		del cursor
		conn.close()
		del conn
	
	os.system("sudo reboot -h now")
	
	
def datatransfermssql(sqlMSSQL):
# dim cursor as cursor
	#print "Entered MS SQL Transfer Process"
	x = 0
	for x in range (i):
		try:
			#print ServerDSN[x], UID[x], PWD[x]
			csql = 'DSN=' + str(ServerDSN[x]) + ';UID=' + UID[x] + ';PWD=' + PWD[x] + ';'
			#print csql
			connSQL = pyodbc.connect('DSN=' + str(ServerDSN[x]) + ';UID=' + UID[x] + ';PWD=' + PWD[x] + ';')
			print "Local MS SQL Database Connected!"
			cursorSQL = connSQL.cursor()
			#print "sqlMSSQL = ", sqlMSSQL
			cursorSQL.execute(sqlMSSQL)
			print "Updated MS SQL Database"
			connSQL.commit()
			cursorSQL.close()
			del cursorSQL
			connSQL.close()
			#x = x + 1
		except:
			csql = 'DSN=' + str(ServerDSN[x]) + ';UID=' + UID[x] + ';PWD=' + PWD[x] + ';'
			csql1 =  str(csql)
			tp1 = "'"
			csql1 = tp1 + csql1 + tp1
			#print csql1
			sqlMSSQL1 =  str(sqlMSSQL) 			
			tp = '"'
			sqlMSSQL1 = tp + sqlMSSQL1 + tp
			#print sqlMSSQL1
						
			sqlErrorMSSQL = "Insert into `MSSQL Error Txn` (`connMSSQL`, `sqlMSSQL`) Values ({}, {})"  .format(csql1, sqlMSSQL1)
			
			#print sqlErrorMSSQL
			conn5 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor5 = conn5.cursor(MySQLdb.cursors.DictCursor)
			if conn5.open:
				try:
					cursor5.execute(sqlErrorMSSQL)
				except MySQLdb.OperationalError:
					cursor5.close()
					del cursor5
					conn5 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
					cursor5 = conn5.cursor(MySQLdb.cursors.DictCursor)
					cursor5.execute(sqlErrorMSSQL)
			else:
				conn5 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
				cursor5 = conn5.cursor(MySQLdb.cursors.DictCursor)
				cursor5.execute(sqlErrorMSSQL)
			conn5.commit()
			if conn5.open:
				cursor5.close()
				del cursor5
				conn5.close()
				del conn5
			print "Updated MS SQL Error Table in built in Db"
			
			continue

def datatransfermysql(sqlMYSQL):
	# dim cursor as cursor
	y = 0
	for y in range (j):
		try:
			connMySQL = MySQLdb.connect(host=hstMySQL[x], user=UIDMysQL[x], passwd=PWDMySQL[x], db=dBMySQL[x], port=int(ptMySQL[x]))
			print "MySQL Database Connected!"
			cursorMySQL = connMySQL.cursor()
			
			cursorMySQL.execute(sqlMYSQL)
			print "Updated MySQL Database"
			connMySQL.commit()
			cursorMySQL.close()
			del cursorMySQL
			connMySQL.close()
			#y = y + 1
		except:
			connMySQL = "host=" + hstMySQL[y] + ", user=" + UIDMysQL[y] + ", passwd=" + PWDMySQL[y] + ", db=" + dBMySQL[y] + ', port=' + str(ptMySQL[y])
			connMySQL1 = str(connMySQL)
			tp1 = "'"
			connMySQL1 = tp1 + connMySQL1 + tp1
			sqlMYSQL1 = str(sqlMYSQL)
			tp = '"'
			sqlMYSQL1 = tp + sqlMYSQL1 + tp
			sqlmysql = "Insert into `MYSQL Error Txn` (`connMYSQL`, `sqlMYSQL`) values ({}, {})" .format(connMySQL1, sqlMYSQL1)
			conn4 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor4 = conn4.cursor(MySQLdb.cursors.DictCursor)
			if conn4.open:
				try:
					cursor4.execute(sqlmysql)
				except MySQLdb.OperationalError:
					cursor4.close()
					del cursor4
					conn4 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
					cursor4 = conn4.cursor(MySQLdb.cursors.DictCursor)
					cursor4.execute(sqlmysql)
			else:
				conn4 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
				cursor4 = conn4.cursor(MySQLdb.cursors.DictCursor)
				cursor4.execute(sqlmysql)
			
			conn4.commit()
			if conn4.open:
				cursor4.close()
				del cursor4
				conn4.close()
				del conn4
			print "Updated MySQL Error Table in built in DB"
			
			continue

def httptransfer(sqlHTTP):
	z = 0
	for z in range (k):
		if UpdateURL[z] == 1:
			try:
				#print controller_serial_no, cid, cmsg, cno, usb_port, dt
				#print url
				#userdata ={"csno": controller_serial_no, "from": cid, "message": cmsg, "School_ID": schoolid, "No": cno, "usbport": usb_port, "datetime": dt}
				#resp = requests.post(url, params=userdata)
				resp = requsts.post(url[z], params=sqlHTTP)
				print "Cloud Database Updated!"

			except:
				
				urlz = url[z]
				urlz1 = str(urlz)
				tp1 = "'"
				urlz1 = tp1 + urlz1 + tp1
				
				sqlHTTP1 = str(sqlHTTP) 
				tp = '"'
				sqlHTTP1 = tp + sqlHTTP1 + tp
				
				sqlhttp = "Insert into `HTTP Error Txn` (`url`, `userdata`) values ({}, {})" .format(urlz1, sqlHTTP1)
				conn3 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NXMD4W", port=3306)
				cursor3 = conn3.cursor(MySQLdb.cursors.DictCursor)
				if conn3.open:
					try:
						#print "sqlhttp = ", sqlhttp
						cursor3.execute(sqlhttp)
					except MySQLdb.OperationalError:
						# cursor.close()
						# del cursor()
						conn3 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NXMD4W", port=3306)
						cursor3 = conn3.cursor(MySQLdb.cursors.DictCursor)
						cursor3.execute(sqlhttp)
				else:
					conn3 = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NXMD4W", port=3306)
					cursor3 = conn3.cursor(MySQLdb.cursors.DictCursor)
					cursor3.execute(sqlhttp)
				print "Updated Cloud Error Table in built-in Db"
				conn3.commit()
				#continue
				
				if conn3.open:
					cursor3.close()
					del cursor3
					conn3.close()
					del conn3
				
				cursor.execute(sqlhttp)
				print "Updated Cloud Error Table in built-in Db"
				conn.commit()
				continue
	
def datatransfer (sqlMSSQL, sqlMYSQL, sqlHTTP):
	# Checking if data is to be sent to cloud
	if updateURL == 1:
		# Updating Cloud DB
		x = Thread(target = httptransfer, args=(sqlHTTP,))
		x1.append(x)
			
		x.start()
		x.join()

	#Updating Local MS SQL Server
	if updateMSSQL == 1:
		mssql = Thread(target = datatransfermssql, args=(sqlMSSQL,))
		mssql1.append(mssql)
		
		mssql.start()
		mssql.join

	
	#Updating Local MYSQL Server
	if updateMYSQL == 1:
		mysql = Thread(target = datatransfermysql, args=(sqlMYSQL,))
		mysql1.append(mysql)
		
		mysql.start()
		mysql.join
	
	
	# Updating Local DB
	conn4x = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor4x = conn4x.cursor(MySQLdb.cursors.DictCursor)
	cursor4x.execute(sqlMYSQL)
	print "Updated built in Db"
	conn4x.commit()
	cursor4x.close()
	del cursor4x
	conn4x.close
	del conn4x
	
# interrupt callback function just get the pin and values and print them
def inthappened1(channel):
	#print "interrupt happened!"
	pin, value = mcp.readInterrupt()
	print("%s %s" % (pin, value), "MCP1") 
	
	if pin == 10:
		print("Exit 3 Interrupt")
		print ("Opening Lock 3")
		Ex = Thread(target = UnlockDoor3(lrt3))
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
			
		# Update Transaction Table
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		
				
		doorname = doorname3
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %( cname, cid, doorname, '3',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %( cname, cid, doorname, '3',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '3', "timestamp": dt, "vmode": 'ExitSwitch', "exr": 'Exit', "status": 'Valid', "Remarks": 'Exit Switch', "Shown": 0, "PSN": psn}
		
		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
		
	elif pin == 11:
		print("Door Sensor 3 Interrupt")
		dr33 = dr3
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
		if dr33 == 0:
			print "Door Forced Open!  Generating Alarm and updating records"
			doorname = doorname3
			doornumber = 3
			
			xOA = Thread(target = OpenAlarm, args=(doornumber,))
			xOAG.append(xOA)
			xOA.start()
			xOA.join()
			
			sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '3',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '3',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '3', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Forced Open', "Shown": 0, "PSN": psn}

			datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
			dataT.append(datat)
			datat.start()
			datat.join()
			
			dr33 = 0
			
		elif dr33 == 1:
			print "Door release time is not completed, hence no alarm"
		elif dr33 == 2:
			print "Checking Door Monitoring Time"
			#dt3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
			delta = dt - T3
			if dmt3 < delta.seconds:
				# generating alarm for "door held open"
				print "Door Held Open! Generating Alarm"
				doorname = doorname3
				doornumber = 3
				# Generate Alarm 
				xOA = Thread(target = OpenAlarm, args=(doornumber,))
				xOAG.append(xOA)
				xOA.start()
				xOA.join()
				
				# Updating Txn Table
				sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '3',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '3',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '3', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Held Open', "Shown": 0, "PSN": psn}

				datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
				dataT.append(datat)
				datat.start()
				datat.join()
				
	elif pin == 12:
		print("Exit 4 Interrupt")
		print ("Opening Lock 4")
		Ex = Thread(target = UnlockDoor4(lrt4))
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
		# Update Transaction Table 
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		doorname = doorname4
		
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '4', "timestamp": dt, "vmode": 'ExitSwitch', "exr": 'Exit', "status": 'Valid', "Remarks": 'Exit Switch', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
					
	elif pin == 13:
		print("Door Sensor 4 Interrupt")
		dr44 = dr4
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
		if dr44 == 0:
			print "Door Forced Open!  Generating Alarm and updating records"
			doorname = doorname4
			doornumber = 4
			
			xOA = Thread(target = OpenAlarm, args=(doornumber,))
			xOAG.append(xOA)
			xOA.start()
			xOA.join()
			
			sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '3', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Forced Open', "Shown": 0, "PSN": psn}

			datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
			dataT.append(datat)
			datat.start()
			datat.join()
			
			dr44 = 0
			
		elif dr44 == 1:
			print "Door release time is not completed, hence no alarm"
		elif dr44 == 2:
			print "Checking Door Monitoring Time"
			#dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
			delta = dt - T4
			if dmt4 < delta.seconds:
				# generating alarm for "door held open"
				print "Door Held Open! Generating Alarm"
				doorname = doorname4
				doornumber = 4
				# Generate Alarm 
				xOA = Thread(target = OpenAlarm, args=(doornumber,))
				xOAG.append(xOA)
				xOA.start()
				xOA.join()
				
				# Updating Txn Table
				sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '4',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '4', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Held Open', "Shown": 0, "PSN": psn}

				datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
				dataT.append(datat)
				datat.start()
				datat.join()
		
	elif pin == 14:
		print("Aux Interrupt")
		print ("Opening Aux Relay")
		Ex = Thread(target = OpenAux())
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
		# Updating Txn Table
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s')" %(cname, cid, dt, 'Fire Alarm', 'Invalid', 'Fire Alarm', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s')" %(cname, cid, dt, 'Fire Alarm', 'Invalid', 'Fire Alarm', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "timestamp": dt, "vmode": 'Fire Alarm', "status": 'Invalid', "Remarks": 'Fire Alarm', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
		
	elif pin == 15:
		print ("Fire Interrupt")
		print ("Opening Fire Relay")
		Ex = Thread(target = OpenFire())
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
		# Updating Txn Table
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s')" %(cname, cid, dt, 'Fire Alarm', 'Invalid', 'Fire Alarm', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s')" %(cname, cid, dt, 'Fire Alarm', 'Invalid', 'Fire Alarm', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "timestamp": dt, "vmode": 'Fire Alarm', "status": 'Invalid', "Remarks": 'Fire Alarm', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
	
def inthappened2(channel):
	#print "interrupt happened!"
	pin, value = mcp1.readInterrupt()
	print("%s %s" % (pin, value), "MCP2") 
	
	if pin == 0:
		print("Door Sensor 1 Interrupt")
		dr11 = dr1
		print dr11
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if dr11 == 0:
			print "Door Forced Open!  Generating Alarm and updating records"
			doorname = doorname1
			doornumber = 1
			
			xOA = Thread(target = OpenAlarm, args=(doornumber,))
			xOAG.append(xOA)
			xOA.start()
			xOA.join()
			
			sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '1', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Forced Open', "Shown": 0, "PSN": psn}

			datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
			dataT.append(datat)
			datat.start()
			datat.join()
			
			dr11 = 0
			
		elif dr11 == 1:
			print "Door release time is not completed, hence no alarm"
		elif dr11 == 2:
			print "Checking Door Monitoring Time"
			#dt1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
			delta = dt - T4
			if dmt1 < delta.seconds:
				# generating alarm for "door held open"
				print "Door Held Open! Generating Alarm"
				doorname = doorname1
				doornumber = 1
				# Generate Alarm 
				xOA = Thread(target = OpenAlarm, args=(doornumber,))
				xOAG.append(xOA)
				xOA.start()
				xOA.join()
				
				# Updating Txn Table
				sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '1', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Held Open', "Shown": 0, "PSN": psn}

				datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
				dataT.append(datat)
				datat.start()
				datat.join()
		
	elif pin == 1:
		print("Exit Switch 1 Interrupt")
		print ("Opening Lock 1")
		Ex = Thread(target = UnlockDoor1(lrt1))
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
		# Update Transaction Table 
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		doorname = doorname1
		
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '1',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '4', "timestamp": dt, "vmode": 'ExitSwitch', "exr": 'Exit', "status": 'Valid', "Remarks": 'Exit Switch', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
		
	elif pin == 2:
		print("Exit Switch 2 Interrupt")
		print ("Opening Lock 2")
		Ex = Thread(target = UnlockDoor2(lrt2))
		Ex1.append(Ex)
		Ex.start()
		Ex.join()
		
		# Update Transaction Table 
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		doorname = doorname2
		
		sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'ExitSwitch', 'Exit', 'Valid', 'Exit Switch', 0, psn)
		sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '2', "timestamp": dt, "vmode": 'ExitSwitch', "exr": 'Exit', "status": 'Valid', "Remarks": 'Exit Switch', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
		
	elif pin == 3:
		print ("Door Sensor 2 Interrupt")
		dr22 = dr2
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
		if dr22 == 0:
			print "Door Forced Open!  Generating Alarm and updating records"
			doorname = doorname2
			doornumber = 2
			
			xOA = Thread(target = OpenAlarm, args=(doornumber,))
			xOAG.append(xOA)
			xOA.start()
			xOA.join()
			
			sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'Door Sensor', 'Invalid', 'Door Forced Open', 0, psn)
			sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '2', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Forced Open', "Shown": 0, "PSN": psn}

			datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
			dataT.append(datat)
			datat.start()
			datat.join()
			
			dr22 = 0
			
		elif dr22 == 1:
			print "Door release time is not completed, hence no alarm"
		elif dr22 == 2:
			print "Checking Door Monitoring Time"
			#dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	# Current Time
			delta = dt - T2
			if dmt2 < delta.seconds:
				# generating alarm for "door held open"
				print "Door Held Open! Generating Alarm"
				doorname = doorname2
				doornumber = 2
				# Generate Alarm 
				xOA = Thread(target = OpenAlarm, args=(doornumber,))
				xOAG.append(xOA)
				xOA.start()
				xOA.join()
				
				# Updating Txn Table
				sqlMSSQL = "Insert into [Txn] ([Controller Name], [Controller ID], [Door Name], [Door Number], [TimeStamp], [Verification Mode], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlMYSQL = "Insert into `Txn` (`Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `TimeStamp`, `Verification Mode`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(cname, cid, doorname, '2',  dt, 'Door Sensor', 'Invalid', 'Door Held Open', 0, psn)
				sqlHTTP = {"cname": cname, "cid": cid, "doorname": doorname, "doornumber": '2', "timestamp": dt, "vmode": 'Door Sensor', "status": 'Invalid', "Remarks": 'Door Held Open', "Shown": 0, "PSN": psn}

				datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
				dataT.append(datat)
				datat.start()
				datat.join()
		
	elif pin == 4:
		print ("Jumper 1 Interrrupt - IP Reset")
		Jx = Thread(target = Reset2())
		Jx1.append(Jx)
		Jx.start()
		Jx.join()
		
	elif pin == 5:
		print ("Jumper 2 Interrupt - Factory Reset")
		Jx = Thread(target = Reset1())
		Jx1.append(Jx)
		Jx.start()
		Jx.join()
	
#def UpdateLog():

def cardprocess(cno, r):
	print "Entered card process"
	#print "Card Number : ", cno
	#conn1 = sqlite3.connect("/etc/Pegasus/NxLAC.db")
	# conn1 = sqlite3.connect("/home/pi/Pegasus/Nx_MD4W.db", timeout=1)
	# conn1.row_factory = sqlite3.Row
	# cursor1 = conn1.cursor()
		
	if r == "Door1IN" :
		doornumber = 1
		entry = 1
		doorname = doorname1
		exr = "Entry"
		attendance = attendance1
	elif r == "Door1OUT":
		doornumber = 1
		entry = 0
		doorname = doorname1
		exr = "Exit"
		attendance = attendance1
	elif r == "Door2IN":
		doornumber = 2
		entry = 1
		doorname = doorname2
		exr = "Entry"
		attendance = attendance2
	elif r == "Door2OUT":
		doornumber = 2
		entry = 0
		doorname = doorname2
		exr = "Exit"
		attendance = attendance2
	if r == "Door3IN" :
		doornumber = 3
		entry = 1
		doorname = doorname3
		exr = "Entry"
		attendance = attendance3
	elif r == "Door3OUT":
		doornumber = 3
		entry = 0
		doorname = doorname3
		exr = "Exit"
		attendance = attendance3
	elif r == "Door4IN":
		doornumber = 4
		entry = 1
		doorname = doorname4
		exr = "Entry"
		attendance = attendance4
	elif r == "Door4OUT":
		doornumber = 4
		entry = 0
		doorname = doorname4
		exr = "Exit"
		attendance = attendance4
	
	sqlCard = "Select * from `Enroll Info` where `Card Number` = '" + str(cno) + "'"
	
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	
	if conn.open:
		try:
			cursor.execute (sqlCard)
		except MySQLdb.OperationalError:
			cursor.close()
			del cursor
			conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute (sqlCard)
	else:
		conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute (sqlCard)
	
	carddata = cursor.fetchall()
	
	if len(carddata) > 0:
		print "Card Details Available!"
		
		for rows in carddata:
			empname = rows['Employee Name']
			empid = rows['Employee ID']
			pwd = rows['PIN']
		
			#print "Employee Details: ", empid, empname
			
		print "checking for timezone for the card!"
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		my_date = date.today()
		my_time = datetime.now().strftime('%H:%M')
		dayofweek = calendar.day_name[my_date.weekday()]
		
		# identifying the various timezones which could be applicable at the current moment
		sqltz = ""
		
		# sqltz = "Select A.[ID], A.[TimeZone Name], A.[Door Number], A.[Door Name], A.[Start Time], A.[End Time], A.[" + dayofweek + "], A.[Anti Passback], A.[Verification Mode], A.[Validity Date], B.[Employee Name], B.[Employee ID], B.[Door Number], B.[TimeZone ID], B.[TimeZone Name], B.[Controller Name], B.[Controller ID], C.[Employee ID], C.[Employee Name], C.[Card Number], C.[PIN], C.[Validity] FROM [Time Zone] AS A, [Employee TimeZone] AS B, [Enroll Info] AS C  WHERE ((A.[" + dayofweek + "] = 1 AND A.[Validity Date] >= '" + str(dt)  + "') AND (A.[Verification Mode] = 'Card' OR A.[Verification Mode] = 'Card + PIN' OR A.[Verification Mode] = 'Card or PIN') AND (A.[Start Time] <= '" + str(my_time) + "' AND A.[End Time] >= '" + str(my_time) + "') AND(A.[ID] = B.[TimeZone ID] AND A.[TimeZone Name] = B.[TimeZone Name]) AND (A.[Door Number] = " + str(doornumber) + " AND B.[Door Number] = " + str(doornumber) + ") AND (B.[Employee ID] = C.[Employee ID] AND B.[Employee Name] = C.[Employee Name]) AND (C.[Validity] >= '" + str(dt) + "') AND C.[Card Number] = " + str(cno) + ")"
		#sqltz = "Select A.`ID`, A.`TimeZone Name`, A.`Door Number`, A.`Door Name`, A.`Start Time`, A.`End Time`, A.`" + dayofweek + "`, A.`Anti Passback`, A.`Verification Mode`, A.`Validity Date`, B.`Employee Name`, B.`Employee ID`, B.`Door Number`, B.`TimeZone ID`, B.`TimeZone Name`, B.`Controller Name`, B.`Controller ID`, C.`Employee ID`, C.`Employee Name`, C.`Card Number`, C.`PIN`, C.`Validity` FROM `Time Zone` AS A, `Employee TimeZone` AS B, `Enroll Info` AS C  WHERE ((A.`" + dayofweek + "` = 1 AND A.`Validity Date` >= '" + str(dt)  + "') AND (A.`Verification Mode` = 'Card' OR A.`Verification Mode` = 'Card + PIN' OR A.`Verification Mode` = 'Card or PIN') AND (A.`Start Time` <= '" + str(my_time) + "' AND A.`End Time` >= '" + str(my_time) + "') AND(A.`ID` = B.`TimeZone ID` AND A.`TimeZone Name` = B.`TimeZone Name`) AND (A.`Door Number` = " + str(doornumber) + " AND B.`Door Number` = " + str(doornumber) + ") AND (B.`Employee ID` = C.`Employee ID` AND B.`Employee Name` = C.`Employee Name`) AND (C.`Validity` >= '" + str(dt) + "') AND C.`Card Number` = " + str(cno)+ ")"
		sqltz = "Select A.`ID`, A.`TimeZone Name`, A.`Start Time`, A.`End Time`, A.`" + dayofweek + "`, A.`Anti Passback`, A.`Verification Mode`, A.`Validity Date`, B.`Employee Name`, B.`Employee ID`, B.`Door Number`, B.`TimeZone ID`, B.`TimeZone Name`, B.`Controller Name`, B.`Controller ID`, C.`Employee ID`, C.`Employee Name`, C.`Card Number`, C.`PIN`, C.`Validity` FROM `Time Zone` AS A, `Employee TimeZone` AS B, `Enroll Info` AS C  WHERE ((A.`" + dayofweek + "` = 1 AND A.`Validity Date` >= '" + str(dt)  + "') AND (A.`Verification Mode` = 'Card' OR A.`Verification Mode` = 'Card + PIN' OR A.`Verification Mode` = 'Card or PIN') AND (A.`Start Time` <= '" + str(my_time) + "' AND A.`End Time` >= '" + str(my_time) + "') AND(A.`TimeZone ID` = B.`TimeZone ID` AND A.`TimeZone Name` = B.`TimeZone Name`) AND (B.`Door Number` = " + str(doornumber)+ ") AND (B.`Employee ID` = C.`Employee ID` AND B.`Employee Name` = C.`Employee Name`) AND (C.`Validity` >= '" + str(dt) + "') AND C.`Card Number` = " + str(cno)+ ")"
		#print sqltz
		cursor.execute (sqltz)
		tzdata = cursor.fetchall()
		if len(tzdata) > 0:
			print ("Time Zone Available and Valid!")
			#print ("Door Interlocking Checking Pending")
			# identifying the right timezone.
			for rows in tzdata:
				# Checking for antipass back 
				if rows['Anti Passback'] == 1:
					APBL = 1  # Anti Pass Back
				else:
					APBL = 0
				
				if APBL == 1:
					print "Checking Checking for Antipass Back!"
					# TimeDiff =    # Calculate Time from current time - 24 hours
					TimeDiff = datetime.today() - timedelta(days=1)
					#print TimeDiff
					
					sqlAPBL = ""
					if entry == 1:
						# sqlAPBL = "Select * from [Antipassback Log] where [Card Number] = '" + str(cno) + "' And [Door Name] = '" + doorname + "' And [Closed] = 0 And [DateTimeEntry] >= '" + str(TimeDiff) + "' and [Entry] = 1"
						sqlAPBL = "Select * from `Antipassback Log` where `Card Number` = '" + str(cno) + "' And `Door Name` = '" + doorname + "' And `Closed` = 0 And `DateTimeEntry` >= '" + str(TimeDiff) + "' and `Entry` = 1"
						#print sqlAPBL
						cursor.execute (sqlAPBL)
						apblog = cursor1.fetchall()
						if len(apblog) > 0:
							print "Anti Passback Error!"
							# Update Error Table
							# Update Transaction Table 
							sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Antipassback Error", 0, psn)
							sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Antipassback Error", 0, psn)
							sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Invalid', "Remarks": 'Antipassback Error', "Shown": 0, "PSN": psn}

							datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
							dataT.append(datat)
							datat.start()
							datat.join()
							
							# Generate Alarm 
							xOA = Thread(target = OpenAlarm, args=(doornumber,))
							xOAG.append(xOA)
							xOA.start()
							xOA.join()
						
						else:
							sqlAPBL = "Select * from [Antipassback Log] where [Card Number] = '" + str(cno) + "' And [Door Name] = '" + doorname + "' And [Closed] = 0 And [DateTimeExit] >= '" + str(TimeDiff) + "' and [Exit] = 0"
							#print sqlAPBL
							cursor1.execute (sqlAPBL)
							apblog1 = cursor1.fetchall()
							
							if len(apblog1) > 0:
								for rows in apblog1:
									recid = rows['RecID']
								
								if interlock == 0:
									# Open Lock
									#OpenDoor(doornumber)
									xOD = Thread(target = OpenDoor, args=(doornumber,))
									xODG.append(xOD)
									xOD.start()
									xOD.join()
								else:
									# Open door according to Interlock setting
									xI = Thread(target = Interlock, args=(interlock, doornumber,))
									xI1.append(xI)
									xI.start()
									xI.join()
								
								# Update Table
								sqlAPBL = "Update `Antipassback Log` Set `Closed` = 1, `DateTimeEntry` = '" + str(dt) + "', `Entry` = 1 Where `RecID` = " + str(recid)
								cursor.execute (sqlAPBL)
								conn.commit()
								
								# update Transaction Log
								sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number], [Attendance]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Closed", 0, psn, attendance)
								sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`, `Attendance`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Closed", 0, psn, attendance)
								sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Valid', "Remarks": 'Antipassback Closed', "Shown": 0, "PSN": psn, "Attendance": attendance}

								datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
								dataT.append(datat)
								datat.start()
								datat.join()
								
								
							else:
								# Check Interlock 
								
								# Open Lock
								if interlock == 0:
									#OpenDoor(doornumber)
									xOD = Thread(target = OpenDoor, args=(doornumber,))
									xODG.append(xOD)
									xOD.start()
									xOD.join()
								else:
									# Open door according to Interlock setting
									xI = Thread(target = Interlock, args=(interlock, doornumber,))
									xI1.append(xI)
									xI.start()
									xI.join()
								
								# Insert Record
								sqlAPBL = "Insert into `Antipassback Log` (`Employee ID`, `Employee Name`, `Card Number`, `PIN`, `Controller ID`, `Controller Name`, `Door Number`, `Door Name`, `Entry`, `DateTimeEntry`, `Closed`) Values ('%s', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cno, pwd, cid, cname, doornumber, doorname, entry, dt, 0)
								cursor.execute (sqlAPBL)
								conn.commit()
								
								# Update Transaction Log
								sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown]. [Product Serial Number], [Attendance]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Opened", 0, psn, attendance)
								sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`, `Attendance`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Opened", 0, psn, attendance)
								sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Valid', "Remarks": 'Antipassback Opened', "Shown": 0, "PSN": psn, "Attendance": attendance}
								
								datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
								dataT.append(datat)
								datat.start()
								datat.join()
								
					elif entry == 0:
						# sqlAPBL = "Select * from [Antipassback Log] where [Card Number] = '" + str(cno) + "' And [Door Name] = '" + doorname + "' And [Closed] = 0 And [DateTimeExit] >= '" + str(TimeDiff) + "' and [Exit] = 0"
						sqlAPBL = "Select * from `Antipassback Log` where `Card Number` = '" + str(cno) + "' And `Door Name` = '" + doorname + "' And `Closed` = 0 And `DateTimeExit` >= '" + str(TimeDiff) + "' and `Exit` = 0"
						
						cursor.execute (sqlAPBL)
						apblog = cursor.fetchall()
						if len(apblog) > 0:
							print "Anti Passback Error!"
							
							# Generate Alarm 
							xOA = Thread(target = OpenAlarm, args=(doornumber,))
							xOAG.append(xOA)
							xOA.start()
							xOA.join()
							
							
							# Update Error Log
							
							# update transaction log 
							sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Antipassback Error", 0, psn)
							sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Antipassback Error", 0, psn)
							sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Invalid', "Remarks": 'Antipassback Error', "Shown": 0, "PSN": psn}

							datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
							dataT.append(datat)
							datat.start()
							datat.join()
						
						else:
							# sqlAPBL = "Select * from [Antipassback Log] where [Card Number] = '" + str(cno) + "' And [Door Name] = '" + doorname + "' And [Closed] = 0 And [DateTimeEntry] >= '" + str(TimeDiff) + "' and [Entry] = 1"
							sqlAPBL = "Select * from `Antipassback Log` where `Card Number` = '" + str(cno) + "' And `Door Name` = '" + doorname + "' And `Closed` = 0 And `DateTimeEntry` >= '" + str(TimeDiff) + "' and `Entry` = 1"
							cursor.execute (sqlAPBL)
							apblog1 = cursor.fetchall()
							
							if len(apblog1) > 0:
								for rows in apblog1:
									recid = rows['RecID']
								
								# Check Interlock
								
								# Open Lock
								if interlock == 0:
									#OpenDoor(doornumber)
									xOD = Thread(target = OpenDoor, args=(doornumber,))
									xODG.append(xOD)
									xOD.start()
									xOD.join()
								else:
									# Open door according to Interlock setting
									xI = Thread(target = Interlock, args=(interlock, doornumber,))
									xI1.append(xI)
									xI.start()
									xI.join()
								
								# Update Table
								sqlAPBL = "Update `Antipassback Log` Set `Closed` = 1, `DateTimeExit` = '" + str(dt) + "', `Exit` = 0 Where `RecID` = " + str(recid)
								cursor1.execute (sqlAPBL)
								conn1.commit()
								
								# update transaction log
								sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number], [Attendance]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Closed", 0, psn, attendance)
								sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`, `Attendance`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Closed", 0, psn, attendance)
								sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Valid', "Remarks": 'Antipassback Closed', "Shown": 0, "PSN": psn, "Attendance":attendance}

								datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
								dataT.append(datat)
								datat.start()
								datat.join()
								
							else:
								# Check Interlock
								if interlock == 0:
									# Open Lock
									#OpenDoor(doornumber)
									xOD = Thread(target = OpenDoor, args=(doornumber,))
									xODG.append(xOD)
									xOD.start()
									xOD.join()
								else:
									# Open door according to Interlock setting
									xI = Thread(target = Interlock, args=(interlock, doornumber,))
									xI1.append(xI)
									xI.start()
									xI.join()
								
								# Insert Record
								sqlAPBL = "Insert into `Antipassback Log` (`Employee ID`, `Employee Name`, `Card Number`, `PIN`, `Controller ID`, `Controller Name`, `Door Number`, `Door Name`, `Exit`, `DateTimeExit`, `Closed`) Values ('%s', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cno, pwd, cid, cname, doornumber, doorname, entry, dt, 0)
								cursor1.execute (sqlAPBL)
								conn1.commit()
								
								# update Transaction Log
								sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number], [Attendance]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Opened", 0, psn, attendance)
								sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`, `Attendance`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "Antipassback Opened", 0, psn, attendance)
								sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Valid', "Remarks": 'Antipassback Opened', "Shown": 0, "PSN": psn, "Attendance": attendance}
								
								datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
								dataT.append(datat)
								datat.start()
								datat.join()
				else:
					# Antipass back not enabled!
					# Checking Interlocking
					print "Antipassback Not Enabled, Checking Interlocking!"
					print "interlock ", interlock
					
					if interlock == 0:
						
						print "Interlock Not Applicable, Opening Door!"
						#OpenDoor(doornumber)
						xOD = Thread(target = OpenDoor, args=(doornumber,))
						xODG.append(xOD)
						xOD.start()
						xOD.join()
					else:
						# Open door according to Interlock setting
						xI = Thread(target = Interlock, args=(interlock, doornumber,))
						xI1.append(xI)
						xI.start()
						xI.join()
					
					# update Transaction Log
					sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number], [Attendance]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "None", 0, psn, attendance)
					sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`, `Attendance`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Valid", "None", 0, psn, attendance)
					sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Valid', "Remarks": 'None', "Shown": 0, "PSN": psn, "Attendance": attendance}
					
					datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
					dataT.append(datat)
					datat.start()
					datat.join()
		else:
			print "Invalid TimeZone! for Employee: ", empid, empname
			# update Error Log
			
			# Generate Alarm 
			xOA = Thread(target = OpenAlarm, args=(doornumber,))
			xOAG.append(xOA)
			xOA.start()
			xOA.join()
			
			
			# update Transaction Log
			sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Invalid TimeZone", 0, psn)
			sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Invalid TimeZone", 0, psn)
			sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Invalid', "Remarks": 'Invalid TimeZone', "Shown": 0, "PSN": psn}

			datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
			dataT.append(datat)
			datat.start()
			datat.join()
		
	else:
		# Generate Alarm 
		xOA = Thread(target = OpenAlarm, args=(doornumber,))
		xOAG.append(xOA)
		xOA.start()
		xOA.join()
		
		print "Invalid Card!"
		empname = ""
		empid = ""
		pwd = ""
		
		#print "Employee Details: ", empid, empname
		if r == "Door1IN" :
			doornumber = 1
			entry = 1
			
			if doorname1 == "":
				doorname = r
			else:
				doorname = doorname1
			exr = "Entry"
		elif r == "Door1OUT":
			doornumber = 1
			entry = 0
			
			if doorname1 == "":
				doorname = r
			else:
				doorname = doorname1
			
			exr = "Exit"
		elif r == "Door2IN":
			doornumber = 2
			entry = 1
			
			if doorname2 == "":
				doorname = r
			else:
				doorname = doorname2
			exr = "Entry"
		elif r == "Door2OUT":
			doornumber = 2
			entry = 0
			
			if doorname2 == "":
				doorname = r
			else:
				doorname = doorname2
			exr = "Exit"
		elif r == "Door3IN" :
			doornumber = 3
			entry = 1
			
			if doorname3 == "":
				doorname = r
			else:
				doorname = doorname3
			exr = "Entry"
		elif r == "Door3OUT":
			doornumber = 3
			entry = 0
			if doorname3 == "":
				doorname = r
			else:
				doorname = doorname3
			exr = "Exit"
		elif r == "Door4IN":
			doornumber = 4
			entry = 1
			
			if doorname4 == "":
				doorname = r
			else:
				doorname = doorname4
				
			exr = "Entry"
		elif r == "Door4OUT":
			doornumber = 4
			entry = 0
			
			if doorname4 == "":
				doorname = r
			else:
				doorname = doorname4
			exr = "Exit"
		
		dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		my_date = date.today()
		my_time = datetime.now().strftime('%H:%M')
		dayofweek = calendar.day_name[my_date.weekday()]
		
		# update Error Log
		# Update Transaction Log
		sqlMSSQL = "Insert into [Txn] ([Employee ID], [Employee Name], [Controller Name], [Controller ID], [Door Name], [Door Number], [Card Number], [TimeStamp], [Verification Mode], [EXR], [Status], [Remarks], [Shown], [Product Serial Number]) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Invalid Card", 0, psn)
		sqlMYSQL = "Insert into `Txn` (`Employee ID`, `Employee Name`, `Controller Name`, `Controller ID`, `Door Name`, `Door Number`, `Card Number`, `TimeStamp`, `Verification Mode`, `EXR`, `Status`, `Remarks`, `Shown`, `Product Serial Number`) Values ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s')" %(empid, empname, cname, cid, doorname, doornumber, cno, dt, "Card", exr, "Invalid", "Invalid Card", 0, psn)
		sqlHTTP = {"empid" : empid, "empname": empname, "cname": cname, "cid": cid, "doorname": doorname, "doornumber": doornumber, "cno": cno, "timestamp": dt, "vmode": 'Card', "exr": 'Entry', "status": 'Invalid', "Remarks": 'Invalid Card', "Shown": 0, "PSN": psn}

		datat = Thread(target = datatransfer, args=(sqlMSSQL, sqlMYSQL, sqlHTTP,))
		dataT.append(datat)
		datat.start()
		datat.join()
	

	if conn.open:
		cursor.close()
		del cursor
		conn.close()
		del conn
	
if __name__ == "__main__":

	
   import pigpio
   import wiegand

   def callbackD1In(bits, value):
      #print("bits={} value={}".format(bits, value))   
      readr = "Door1IN"
      print "Card Number = ", value, readr
      # Card Processing
      xC = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC)
      xC.start()
      xC.join()
     
	
   def callbackD1Out(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door1OUT"
      print "Card Number = ", value, readr
      # Card Processing
      xC2 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC2)
      xC2.start()
      xC2.join()
      
   
   def callbackD2In(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door2IN"
      print "Card Number = ", value, readr
      # Card Processing
      xC3 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC3)
      xC3.start()
      xC3.join()
	 

   def callbackD2Out(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door2OUT"
      print "Card Number = ", value, readr
      # Card Processing
      xC4 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC4)
      xC4.start()
      xC4.join()
	  
   def callbackD3In(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door3IN"
      print "Card Number = ", value, readr
      # Card Processing
      xC5 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC5)
      xC5.start()
      xC5.join()
	 

   def callbackD3Out(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door3OUT"
      print "Card Number = ", value, readr	  
      # Card Processing
      xC6 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC6)
      xC6.start()
      xC6.join()
   
   def callbackD4In(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door4IN"
      print "Card Number = ", value, readr
      # Card Processing
      xC7 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC7)
      xC7.start()
      xC7.join()
	 

   def callbackD4Out(bits, value):
      #print("bits={} value={}".format(bits, value))
      #print "Card Number = ", value
      readr = "Door4OUT"
      print "Card Number = ", value, readr
      # Card Processing
      xC8 = Thread(target = cardprocess, args=(value, readr,))
      xC1.append(xC8)
      xC8.start()
      xC8.join()
	  
   pi = pigpio.pi()

   D1In = wiegand.decoder(pi, 13, 4, callbackD1In)
   D1Out = wiegand.decoder(pi, 26, 19, callbackD1Out)
   D2In = wiegand.decoder(pi, 12, 16, callbackD2In)
   D2Out = wiegand.decoder(pi, 20, 21, callbackD2Out)
   D3In = wiegand.decoder(pi, 27, 17, callbackD3In)
   D3Out = wiegand.decoder(pi, 10, 22, callbackD3Out)
   D4In = wiegand.decoder(pi, 6, 5, callbackD4In)
   D4Out = wiegand.decoder(pi, 11, 9, callbackD4Out)
   
   try:
		mcp = MCP23017(address = 0x20, num_gpios = 16) # MCP23017
		mcp1 = MCP23017(address = 0x21, num_gpios = 16) # MCP23017
		print ("MCP Configured!")
		
		inpin0 = 0
		mcp.pinMode(inpin0, mcp.OUTPUT)
		#mcp.pullUp(inpin0, 1)
		mcp1.pinMode(inpin0, mcp1.INPUT)
		mcp1.pullUp(inpin0, 1)

		inpin1 = 1
		mcp.pinMode(inpin1, mcp.OUTPUT)
		#mcp1.pullUp(inpin1, 1)
		mcp1.pinMode(inpin1, mcp1.INPUT)
		mcp1.pullUp(inpin1, 1)

		inpin2 = 2
		mcp.pinMode(inpin2, mcp.OUTPUT)
		mcp1.pinMode(inpin2, mcp1.INPUT)
		mcp1.pullUp(inpin2, 1)

		inpin3 = 3
		mcp.pinMode(inpin3, mcp.OUTPUT)
		mcp1.pinMode(inpin3, mcp1.INPUT)
		mcp1.pullUp(inpin3, 1)

		inpin4 = 4
		mcp.pinMode(inpin4, mcp.OUTPUT)
		mcp1.pinMode(inpin4, mcp1.INPUT)
		mcp1.pullUp(inpin4, 1)
		
		inpin5 = 5
		mcp.pinMode(inpin5, mcp.OUTPUT)
		mcp1.pinMode(inpin5, mcp1.INPUT)
		mcp1.pullUp(inpin5, 1)
		
		inpin6 = 6
		mcp.pinMode(inpin6, mcp.OUTPUT)
		# mcp1.pinMode(inpin5, mcp.INPUT)
		# mcp1.pullUp(inpin5, 1)
		
		inpin7 = 7
		mcp.pinMode(inpin7, mcp.OUTPUT)
		# mcp1.pinMode(inpin7, mcp1.OUTPUT)
		# mcp1.pullUp(inpin7, 1)

		inpin8 = 8
		mcp.pinMode(inpin8, mcp.OUTPUT)
		mcp1.pinMode(inpin8, mcp1.OUTPUT)
		#mcp1.pullUp(inpin8, 1)

		inpin9 = 9
		mcp.pinMode(inpin9, mcp.OUTPUT)
		mcp1.pinMode(inpin9, mcp1.OUTPUT)
		#mcp.pullUp(inpin9, 1)

		inpin10 = 10
		mcp.pinMode(inpin10, mcp.INPUT)
		mcp.pullUp(inpin10, 1)
		mcp1.pinMode(inpin10, mcp1.OUTPUT)

		inpin11 = 11
		mcp.pinMode(inpin11, mcp.INPUT)
		mcp.pullUp(inpin11, 1)
		mcp1.pinMode(inpin11, mcp1.OUTPUT)
			
		inpin12 = 12
		mcp.pinMode(inpin12, mcp.INPUT)
		mcp.pullUp(inpin12, 1)
		mcp1.pinMode(inpin12, mcp1.OUTPUT)

		inpin13 = 13
		mcp.pinMode(inpin13, mcp.INPUT)
		mcp.pullUp(inpin13, 1)
		mcp1.pinMode(inpin13, mcp1.OUTPUT)

		inpin14 = 14
		mcp.pinMode(inpin14, mcp.INPUT)
		mcp.pullUp(inpin14, 1)
		mcp1.pinMode(inpin14, mcp1.OUTPUT)
		
		inpin15 = 15
		mcp.pinMode(inpin15, mcp.INPUT)
		mcp.pullUp(inpin15, 1)
		mcp1.pinMode(inpin15, mcp1.OUTPUT)
		
		#print ("MCP IO Pin 0 to 15  configured!")
		
		# ledpin = 6
		# mcp.pinMode(ledpin, mcp.OUTPUT)
		# print ("LED MCP Pin 8 configured!")
		
		# mirror on, int pin high indicates interrupt
		mcp.configSystemInterrupt(mcp.INTMIRRORON, mcp.INTPOLACTIVEHIGH)
		mcp1.configSystemInterrupt(mcp1.INTMIRRORON, mcp1.INTPOLACTIVEHIGH)
		#print ("System Interrupt Configured!")
		
		# for the input pin, enable interrupts and compare to previous 
		# value rather than default
		mcp1.configPinInterrupt(inpin0, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		mcp1.configPinInterrupt(inpin1, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		mcp1.configPinInterrupt(inpin2, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		mcp1.configPinInterrupt(inpin3, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		mcp1.configPinInterrupt(inpin4, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		mcp1.configPinInterrupt(inpin5, mcp1.INTERRUPTON, mcp1.INTERRUPTCOMPAREPREVIOUS)
		# mcp.configPinInterrupt(inpin6, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		# mcp.configPinInterrupt(inpin7, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		# mcp.configPinInterrupt(inpin8, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		# mcp.configPinInterrupt(inpin9, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin10, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin11, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin12, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin13, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin14, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)
		mcp.configPinInterrupt(inpin15, mcp.INTERRUPTON, mcp.INTERRUPTCOMPAREPREVIOUS)

		#print ("Config Pin Interrupt Configured!")

		# use a builting GPIO pin from the Pi to detect any change on 
		# the mcp23017 specify the callback function edge must be set to 
		# rising - rising to high indicates the interrupt happened, 
		# while falling is just the pin resetting set the pin to pull 
		# down to act as a sink when the mcp23017 int pin goes high do 
		# not thread - the mcp23017 int pin stays high until cleared 
		# even if multiple interrupts occur. there is a risk that we'll 
		# miss an interrupt if they happen very quickly together set a 
		# very small debounce. 5ms seems good. higher and you could end 
		# up with the int pin getting "stuck"
		#GPIO.add_interrupt_callback(4, inthappened, edge='rising', pull_up_down=GPIO.PUD_DOWN, threaded_callback=False, debounce_timeout_ms=5)
		GPIO.add_event_detect(15, GPIO.RISING, callback = inthappened1, bouncetime=5)
		GPIO.add_event_detect(18, GPIO.RISING, callback = inthappened2, bouncetime=5)
		# regular GPIO wait for interrupts
		#GPIO.wait_for_interrupts(threaded=True)
		while (True):
			#print ("While True loop")
			# mcp.output(ledpin, 1)
			# time.sleep(1)
			# mcp.output(ledpin, 0)
			time.sleep(0.5)
			# this is a failsafe for the instance when two 
			# interrupts happen before the debounce timeout expires. 
			# it will check for interrupts on the pin three times in 
			# a row, .5 seconds apart. if it gets to the end of 3 
			# iterations, we're probably stuck so it will reset
			mcp.clearInterrupts() 
			mcp1.clearInterrupts()
			
   except Exception as e:
		print("Error in main: " + format(e)) 
   finally:
		mcp.cleanup()
		mcp1.cleanup()
		GPIO.cleanup()
   
   #time.sleep(157680000)
