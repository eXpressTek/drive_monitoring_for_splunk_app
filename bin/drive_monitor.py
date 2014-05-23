#!/usr/local/bin/python2.7
import os
import re
import sys
import subprocess
import time
import json
import glob

debug = False

rev="1.1"
#smartctl requires root.
if not os.geteuid()==0:
    if not inTesting:
        sys.exit("\nOnly root can run this script\n")

#make a timestamp
def stamp():
    return time.strftime("%m-%d-%YT%H:%M:%S+0000 ",time.gmtime())

#get everything in /dev/rdsk (all the disks attached to the system)
ls = glob.glob('/dev/rdsk/*d0')
#print ls
#now ls contains only disks (not parts) so now we iterate through them and get information from each

for drive in ls:
    #print drive
    if debug:
        print drive
    #ask the drive for its information
    smart = ""
    try:
        smart = subprocess.check_output(['smartctl','-a','-d','scsi',drive],stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        #if the drive does not exist, just go on to the next one.
        if debug:
            print err.message
            print smart
        continue
    if debug:
        print smart
    #massage the data to get what we want
    smart = re.sub(' +',' ',smart)
    smart = re.sub(r'<=','is less than', smart)
    smart = re.sub(r':','=',smart)
    smart = smart = re.sub('= ','=',smart)
    #now we start splitting the information we want (line by line) and putting it into a string
    smart = smart.split('\n')
    smartInfo = ""
    #unstructured information is for information that is not necessarily easily parsible (just puts it in an array for later retrieval)
    unstructured = []
    for line in smart:
        lineInfo = line.split('=')
        #if it is easily parsible, parse it and put it in a key all by itself
        if (len(lineInfo) == 2):
            smartInfoKey = str(lineInfo[0])
            smartInfoValue = str(lineInfo[1])
            smartInfoKey = smartInfoKey.rstrip()
            smartInfoValue = smartInfoValue.rstrip()
            smartInfoKey = smartInfoKey.lstrip()
            smartInfoValue = smartInfoValue.lstrip()
            smartInfoKey = re.sub(' ','_',smartInfoKey)
            smartInfo = smartInfo+smartInfoKey+"=\""+smartInfoValue+"\", "
        else:
            #otherwise, put it in the unstructured information
            unstructured.append(line)
    #print what we've found.
    smartInfo = smartInfo+"Device_Name=\""+str(drive)+"\", "
    smartInfo = smartInfo+"unstructured="+str(unstructured)
    print "{0} rev=\"{1}\" {2} ".format(stamp(),rev,smartInfo)
