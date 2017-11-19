from threading import Thread
import requests

import time
from datetime import datetime
import pyodbc
from datetime import datetime 
import MySQLdb

global t


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
			print("Cannot Open Database")
			sys.exit()
#### Even after 100 tries, if Mysql is not loaded, then exit the application

def httptransfer():
	print "Entered HTTP Data Transfer Function!"
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	
	sqlCloud = "Select * from `HTTP Error Txn`"
	cursor.execute (sqlCloud)

	urlResult = cursor.fetchall()

	if len(urlResult) > 0:
		for rows in urlResult:
			url = rows['url']
			userdata = rows['userdata']
			recordID = rows['RecordID']
			try:
				resp = requests.post(url, params=userdata)
				#print "Cloud Database Updated!"
				
				sqlupdate = "Delete from `HTTP Error Txn` where `RecordID` = '%d'" %(recordID)
				cursor.execute (sqlupdate)
				conn.commit()
				
			except:
				print "Unable to upload to Cloud DB. Quiting..."
				continue
	cursor.close()
	del cursor			
	conn.close()
	print "Exiting HTTP Data Transfer Function!"
	datatransfermysql()

def datatransfermysql():
	print "Entered MySQL Data Transfer Function!"
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	
	sqlCloud = "Select * from `MYSQL Error Txn`"
	cursor.execute (sqlCloud)

	MySQLResult = cursor.fetchall()
	if len(MySQLResult) > 0:
		for rows in MySQLResult:
			recordID = rows['RecordID']
			mysqlconn = rows['connMYSQL']
			sqlMYSQL = rows['sqlMYSQL']
	
			try:
				print "Connecting to MySQL DB"
				#print mysqlconn
				#tpcon = "MySQLdb.connect(" + mysqlconn + ")"
				#print tpcon
				connMySQL = MySQLdb.connect(mysqlconn)
				print "MySQL Database Connected!"
				cursorMySQL = connMySQL.cursor()
				cursorMySQL.execute(sqlMYSQL)
				print "Updated MySQL Database"
				connMySQL.commit()
				sqlupdate = "Delete from `MYSQL Error Txn` where `RecordID` = '%d'" %(recordID)
				cursor.execute (sqlupdate)
				conn.commit()
				cursorMySQL.close()
				del cursorMySQL
				connMySQL.close()
			
			except :
				#print e
				print "Unable to connect to MYSQL DB.  Quiting..."
				continue
	cursor.close()
	del cursor			
	conn.close()
	print "Exiting MySQL Data Transfer Function!"
	datatransfermssql()
	
def datatransfermssql():
	print "Entered MSSQL Data Transfer Function!"
	conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)	
	
	sqlCloud = "Select * from `MSSQL Error Txn`"
	cursor.execute (sqlCloud)

	MSSQLResult = cursor.fetchall()
	if len(MSSQLResult) > 0:
		for rows in MSSQLResult:
			recordID = rows['RecordID']
			mssqlconn = rows['connMSSQL']
			sqlMSSQL = rows['sqlMSSQL']
	
			try:
				#tp = "'"
				#mssqlconn = tp + mssqlconn + tp
				print mssqlconn
				print "Connecting to MS SQL DB"
				#cmsqltp = "pyodbc.connect(" + mssqlconn + ")"
				#print cmsqltp
				print sqlMSSQL

				connMSSQL = pyodbc.connect(mssqlconn)
				#print sqlMSSQL
				#connMSSQL = pyodbc.connect('DSN=ServerDSN1;UID=sa;PWD=Pegasus;')
				print "MS SQL Database Connected!"
				cursorMSSQL = connMSSQL.cursor()
				cursorMSSQL.execute(sqlMSSQL)
				print "Updated MSSQL Database"
				connMSSQL.commit()
				sqlupdate = "Delete from `MSSQL Error Txn` where `RecordID` = '%d'" %(recordID)
				print sqlupdate
				cursor.execute(sqlupdate)
				conn.commit()
				cursorMSSQL.close()
				del cursorMSSQL
				connMSSQL.close()
			
			except :
				#print err
				print "Unable to connect to MS SQL DB.  Quiting..."
				continue
	cursor.close()
	del cursor			
	conn.close()
	print "Exiting MSSQL Data Transfer Function!"

conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

sqlCloud = "Select * from `Controller Parameters`"
cursor.execute (sqlCloud)

SResult = cursor.fetchall()
if len(SResult) > 0:
	for rows in SResult:
        	t = rows['Retrytime']
		t = t * 60
else:
	t = 600

cursor.close()
del cursor
conn.close()
del conn

print "Rety Time = ", t/60

while True:
	print "Entering Loop"
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	httptransfer()
	time.sleep(t)
	#time.sleep(10)
	print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print "Exiting Loop"
