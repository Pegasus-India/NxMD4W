#!/usr/bin/env python

#import sqlite3
import MySQLdb


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

# dim conn as connection
#print "Opening DB"
conn = MySQLdb.connect(host="localhost", user="root", passwd="pegasus", db="NxMD4W", port=3306)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

print "database opened..."

sqltemp = "Select * from `Controller Parameters` where `Updated` = 0"
cursor.execute(sqltemp)
result = cursor.fetchall()
print "Controller IP Table Opened"
print len(result)

if len(result) > 0:
			
	#open('C:/Documents and Settings/user/Desktop/testfreetds.conf', 'w').close()
	#f = open('C:/Documents and Settings/user/Desktop/testfreetds.conf', 'w')
	
	print "Updating eth0"
	open('/etc/dhcpcd.conf', 'w').close()
	f = open('/etc/dhcpcd.conf', 'w')

	f.write('# A sample configuration for dhcpcd. \n')
	f.write('# See dhcpcd.conf(5) for details. \n')
	f.write('\n')
	f.write('# Allow users of this group to interact with dhcpcd via the control socket. \n')
	f.write('#controlgroup wheel \n')
	f.write('\n')
	f.write ('# Inform the DHCP server of our hostname for DDNS. \n')
	f.write('hostname\n')
	f.write('# Use the hardware address of the interface for the Client ID. \n')
	f.write('clientid \n')
	f.write('# or \n')
	f.write('# Use the same DUID + IAID as set in DHCPv6 for DHCPv4 ClientID as per RFC4361. \n')
	f.write('#duid \n')
	f.write(' \n')
	f.write('# Persist interface configuration when dhcpcd exits.\n')
	f.write('persistent \n')
	f.write('\n')
	f.write('# Rapid commit support.  \n')
	f.write('# Safe to enable by default because it requires the equivalent option set \n')
	f.write('# on the server to actually work. \n')
	f.write('option rapid_commit \n')
	f.write('# A list of options to request from the DHCP server. \n')
	f.write('option domain_name_servers, domain_name, domain_search, host_name \n')
	f.write('option classless_static_routes \n')
	f.write('# Most distributions have NTP support. \n')
	f.write('option ntp_servers \n')
	f.write('# Respect the network MTU. \n')
	f.write('# Some interface drivers reset when changing the MTU so disabled by default. \n')
	f.write('#option interface_mtu \n')
	f.write(' \n')
	f.write('# A ServerID is required by RFC2131. \n')
	f.write('require dhcp_server_identifier \n')
	f.write(' \n')
	f.write('# Generate Stable Private IPv6 Addresses instead of hardware based ones \n')
	f.write('slaac private \n')
	f.write(' \n')
	f.write('# A hook script is provided to lookup the hostname if not set by the DHCP \n')
	f.write('# server, but it should not be run by default. \n')
	f.write('nohook lookup-hostname \n')
	f.write(' \n')
	f.write('interface eth0 \n')
	f.write('\n')

	for rows in result:
		IPAddress = rows['IP Address']
		Gateway = rows['Gateway']
		WLanIP = rows['WiFi IP Address']
		WLanGateway = rows['WiFi Gateway']
		SSID = rows['WiFi SSID']
		ssid_pwd = rows['WiFi PWD']
		
		#print IPAddress, Gateway

	f.write('inform ' + str(IPAddress) + '\n')
	f.write('static routers=' + str(Gateway) + '\n')
	f.write('static domain_name_servers=' + str(Gateway) + '\n')
	print "eth0 updated"
	
	if WLanIP <> "":
		print "Updating wlan0"
		f.write('\n')
		f.write('\n')
		f.write('interface wlan0 \n')
		f.write('\n')
		f.write('inform ' + str(WLanIP) + '\n')
		f.write('static routers=' + str(WLanGateway) + '\n')
		f.write('static domain_name_servers=' + str(WLanGateway) + '\n')
		f.close()
		print "wlan0 Updated!"
		
		# open ('/etc/wpa_supplicant/wpa_supplicant.conf', 'w').close()
		# f1 = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
		# f1.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \n')
		# f1.write('update_config=1 \n')
		# f1.write('Country=IN \n')
		# f1.write('\n')
		# f1.write('network={ \n')
		# f1.write('	ssid="' + str(SSID) + '" \n')
		# f1.write('	psk="' + str(ssid_pwd) + '" \n')
		# f1.write('	key_mgmt=WPA-PSK \n')
		# f1.write('} \n')
		# f1.close()
		# print "wlan0 Updated"

		# Updating Table
	sqltemp = ""
	sqltemp = "Update `Controller Parameters` Set `Updated` = 1"
	cursor.execute(sqltemp)
	conn.commit()
	print "Table Updated"
else:
	print "No Data Change in IP Address Info!"		
	
# updating ODBC File
sql = "Select * from `MSSQL`"
cursor.execute(sql)
sqlResult  = cursor.fetchall()

if len(sqlResult) > 0:
	print "Updating ODBC File"
	f = open('/etc/odbc.ini', 'w')	
	open('/etc/odbc.ini', 'w').close()
	for rows in sqlResult:
		ServerDSN = rows['ServerDSN']
		Servername = rows['MyServer']
		Db = rows['Database']
		
		f.write('[' + str(ServerDSN) + '] \n')
		f.write('Description = Some Description \n')
		f.write('Driver = FreeTDS \n')
		f.write('Servername = ' + Servername + '\n')
		f.write('Database = '+ Db + '\n')			
		f.write(' \n')

	f.close()
	print "odbc.conf updated!"

# updating Freetds File
sql = "Select * from `MSSQL`"
cursor.execute(sql)
sqlResult  = cursor.fetchall()

if len(sqlResult) > 0:
	# Updating freetds
	print "Updating freetds.conf"
	open('/etc/freetds/freetds.conf', 'w').close()
	f = open('/etc/freetds/freetds.conf', 'w')

	f.write('#   $Id: freetds.conf,v 1.12 2007/12/25 06:02:36 jklowden Exp $ \n')
	f.write('#\n')
	f.write('# This file is installed by FreeTDS if no file by the same \n')
	f.write('# name is found in the installation directory. \n')
	f.write ('#\n')
	f.write('# For information about the layout of this file and its settings, \n')
	f.write('# see the freetds.conf manpage "man freetds.conf". \n')
	f.write('\n')
	f.write('# Global settings are overridden by those in a database \n')
	f.write('# server specific section \n')
	f.write('[global] \n')
	f.write('        # TDS protocol version \n')
	f.write(';       tds version = 4.0 \n')
	f.write('\n')
	f.write(' Whether to write a TDSDUMP file for diagnostic purposes \n')
	f.write('        # (setting this to /tmp is insecure on a multi-user system) \n')
	f.write(';       dump file = /tmp/freetds.log \n')
	f.write(';       debug flags = 0xffff \n')
	f.write('\n')
	f.write('        # Command and connection timeouts \n')
	f.write(';       timeout = 10 \n')
	f.write(';       connect timeout = 10 \n')
	f.write('\n')
	f.write('        # If you get out-of-memory errors, it may mean that your client \n')
	f.write('        # is trying to allocate a huge buffer for a TEXT field. \n')
	f.write("        # Try setting 'text size' to a more reasonable limit \n")
	f.write('        text size = 64512 \n')
	f.write('\n')
	f.write('# A typical Sybase server \n')
	f.write('[egServer50] \n')
	f.write('        host = symachine.domain.com \n')
	f.write('        port = 5000 \n')
	f.write('        tds version = 5.0 \n')
	f.write('\n')
	f.write('# A typical Microsoft server \n')
	
	for rows in sqlResult:
		
		MyServer = rows['MyServer']
		Hostname = rows['Hostname']
		InstanceName = rows['InstanceName']
		Port = rows['Port']
		
		f.write(' \n')
		f.write('[' + MyServer + '] \n')
		f.write('        host = ' + Hostname + '\n')
		f.write('	instance = ' + InstanceName + '\n')
		f.write('        tdsversion = 7.0 \n')
		f.write('        port = '+ str(Port) + '\n')
		f.write('        charset = UTF-8 \n')

	f.close()
	
	print "freetds.conf Updated"
	
	print "All Files Updated Successfully!"

	# Updating Table
	sqltemp = ""
	sqltemp = "Update `MSSQL` Set `Updated` = 1"
	cursor.execute(sqltemp)
	conn.commit()
	print "Table Updated"
else:
	print "No Data"

cursor.close()
del cursor
conn.close()
del conn
print "Connection Closed"
