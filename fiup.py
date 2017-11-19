import os
import sys
import MySQLdb
import time

#### Checking if MySQL is loaded, so that application can be launched
tt = 0
while tt < 100:
        try:
                db = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
                db.close()
                tt=100
        except:
                tt+=1
		#print tt
                time.sleep(1)
                if(tt==99):
                        print("Cannot Open Database")
                        sys.exit()
#### Even after 100 tries, if Mysql is not loaded, then exit the application


while True:
#       print "Entering Loop"
#       print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	#print "Connected to DB"
        sql = "Select * from `FiUp`"
        cursor.execute(sql)
        result = cursor.fetchall()

        rs = ""
        rid = ""
        if len(result) > 0:
            	print "Record Available!"
		for rows in result:
			rid = rows['RecordID']
			rs = rows['File Update']

		if rs == 1:
			sql = ""
			sql  = "Delete from `FiUp` where `RecordId` = " + str(rid)
			cursor.execute (sql)
			conn.commit()
			cursor.close()
			del cursor
			conn.close()
			del conn
			print "Updating Parameters..."
			os.system("sudo python /home/pi/Documents/Pegasus/fileupdates.py")
        else:
			cursor.close()
			del cursor

			conn.close()
			del conn

        time.sleep(1)



