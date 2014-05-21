#!/usr/local/bin/python2.7
import os
import re
import sys
import subprocess

debug = False

#smartctl requires root.
if not os.geteuid()==0:
    if not inTesting:
        sys.exit("\nOnly root can run this script\n")

#get everything in /dev/rdsk (all the disks attached to the system)
ls = subprocess.check_output(['ls','/dev/rdsk/'])
#do some massaging to get just the data we want out of it
ls = re.sub(r' +',' ',ls)
ls = re.sub(r' ','\n',ls)
ls = re.findall(r'(?m)c0t[0-9A-F]+d0$', ls)

#now ls contains only disks (not parts) so now we iterate through them and get information from each
for drive in ls:
    if debug:
        print drive
    #ask the drive for its information
    smart = ""
    try:
        smart = subprocess.check_output(['smartctl','-a','-d','scsi',"/dev/rdsk/"+drive],stderr=subprocess.STDOUT)
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
    #now we start splitting the information we want (line by line) and putting it into a dictionary
    smart = smart.split('\n')
    smartInfo = {}
    #unstructured information is for information that is not necessarily easily parsible (just puts it in an array for later retrieval)
    smartInfo['Unstructured Information'] = []
    for line in smart:
        lineInfo = line.split('=')
        #if it is easily parsible, parse it and put it in a key all by itself
        if (len(lineInfo) == 2):
            smartInfo[lineInfo[0]] = lineInfo[1]
        else:
            #otherwise, put it in the unstructured information
            smartInfo['Unstructured Information'].append(line)
    #print what we've found.
    print smartInfo