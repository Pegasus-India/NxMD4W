import os
import sys
from datetime import datetime

cdt = ""
cdt = datetime.now().strftime('%Y-%m-%d %H:%M')
print cdt

dt = ""
os.system("sudo sntp -s time.google.com")
dt = datetime.now().strftime('%Y-%m-%d %H:%M')

print "DT = ", dt

hdt = ""
os.system ("sudo hwclock --hctosys")
hdt = datetime.now().strftime('%Y-%m-%d %H:%M')
print "HDT = ", hdt

if hdt > dt:
        print "HW Clock time is greater than System time"
elif hdt < dt:
        print "HW Clock is lower than System time"
        print "Resetting HW Clock and System time"
        os.system("sudo date -s cdt")
        os.system("sudo hwclock --systohw")
else:
        print "Date need not be changed!"

print "HW Clock Time Set"
hwc =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print "HWC = ", hwc

