import os
from datetime import datetime
import MySQLdb
import time

global cmd
cmd = ""

global cdt
cdt = ""


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
                        print("Cannot Open Database! Quitting...")
                        sys.exit()
#### Even after 100 tries, if Mysql is not loaded, then exit the application



while True:
#       print "Entering Loop"
#       print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql = "Select * from `DT` where `Updated` = 0"
        cursor.execute(sql)
        result = cursor.fetchall()
         
        cmd = ""
        cdt = ""
        rid = ""
 
	if len(result) > 0:
                for rows in result:
                        cmd = rows['Request Set']
                        cdt = rows['CDT']
                        rid = rows['RecordID']

#       print cmd
        if cmd <> "":
                if cmd == "Request":
                        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        sql = "Update `DT` Set `CDT` = '%s'" %(dt)
                        print sql
                        cursor.execute (sql)
                        conn.commit()
                        sql = "Update `DT` Set `Updated` = 1 where `RecordID` = '%d'" %(rid)
                        print sql
                        cursor.execute(sql)
                        conn.commit()
                        print "Record updated!"
                elif cmd == "Set":
                        dt = datetime.strptime(cdt, '%Y-%m-%d %H:%M:%S')
                        print "Setting Date Time to Pi"
                        print "dt = ", dt
                        os.system("sudo date -s '" + str(dt) + "'")
                        os.system("sudo hwclock --systohc")
                        print "hw clock updated successfully!"
                        sql = ""
                        sql = "Delete from `DT` where `RecordID` = " + str(rid)
                        cursor.execute(sql)
                        conn.commit()
                        print "Record Deleted Successfully!"

#       print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#       print "Exiting Loop"
	cursor.close()
	del cursor
	conn.close()
	del conn
	
	time.sleep(1)
	