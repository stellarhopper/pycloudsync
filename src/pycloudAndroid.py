#!/usr/bin/python

"""Author: Vishal Verma"""


import os
import select
import socket
import sys
import getopt
import time
from threading import Thread
import Queue
from ftplib import FTP, error_perm
from copy import copy


#Global Queue for passing filesystem update messages
q = Queue.Queue()
ftpIp = ''
watchPath = ''


def usage():
    """This function shows the usage of the script if called with invalid or
    no options"""
    print "Usage:"
    print "$./pycloud.py [OPTIONS]"
    print "--mode     [client | server]"
    print "--ip       IP address to connect to (with --mode=client)"
    print "--port     port number to serve on/connect to"
    print "-h for help"
    print "e.g: $ ./pycloudC.py --mode=server --port=5054"
    print "e.g: $ ./pycloudC.py --mode=client --ip=10.0.1.10 --port=5054"
    sys.exit()
    
    
def getUsrOpts():
    """Get command line arguments passed by the user"""
    retlist = ['client', '10.0.1.9', '6005', '/sdcard/DCIM/Camera/']
    mymode = ''
    myip = ''
    myport = ''
    mypath = ''
    if(len(sys.argv) > 2):
        opt, args = getopt.getopt(sys.argv[1:], "h:", \
                                  ['mode=', 'port=', 'ip=', 'path='])	
        print opt
        for option, value in opt:
            if option == "-h":
                usage()
            elif option == "--mode":
                mymode = value
            elif option == "--ip":
                myip = value
            elif option == "--port":
                myport = value
            elif option == "--path":
                mypath = value
            else:
                print "Unknown option"
                usage()
    else:
        return retlist
        
    del retlist[:]
    retlist.append(mymode)
    retlist.append(myip)
    retlist.append(myport)
    retlist.append(mypath)
    return retlist


def ftpGetFile(fName):
    """Retrieve a file from the ftp server at the specified IP address 
    (parameters: file name)"""
    print 'Check and get:', fName
    if os.path.isfile(watchPath+fName):
        print 'ftpGetFile:', fName, 'exists, will not RETR'
    else:
        global ftpIp
        global watchPath
        ftp = FTP(ftpIp)
        ftp.login('stellarhopper', 'hoppingstar')
        #TODO: Possibly implement file validation using size from LIST cmd
        retval = ftp.retrbinary('RETR '+fName, open(watchPath+fName, 'wb').write)
        print 'FTP:', retval

        
def readQandFTP():
    """Function (thread) to dequeue a command from the global actions queue 
    and perform the appropriate FTP command (store/retrieve/delete"""
    global ftpIp
    ftp = FTP(ftpIp)
    ftp.login('stellarhopper', 'hoppingstar')
    retval = ftp.retrlines('NLST', ftpGetFile)
    print "FTP Listing and Syncing: ", retval
    
    fsThread = Thread(target=fsMonitor)
    fsThread.start()
    
    while 1:
        while not q.empty():
            qMsg =  q.get()
            cmd = qMsg[0]
            fName = qMsg[1]
            fPath = qMsg[2]
            isDir = qMsg[3]
            print 'Dequeued:', qMsg
            
            if cmd == 'CREATE':
                if isDir == True:
                    #This is a directory operation
                    #FTP MKD
                    pass
                else:
                    #Store new file
                    fDes = open(fPath, "r")
                    retval = ftp.storbinary('STOR '+fName, fDes)
                    print 'FTP:', retval
                    fDes.close()
                    
            elif cmd == 'DELETE':
                try:
                    retval = ftp.delete(fName)
                except error_perm:
                    pass
                print 'FTP:', retval
                
            elif cmd == 'GET':
                #retval = ftp.retrbinary('RETR '+fName, open(watchPath+fName, 'wb').write)
                #print 'FTP:', retval
                ftpGetFile(fName)
    #TODO: Find a good way to end this thread
    

def fsMonitor():
    """This function uses the 'os' module to implement filesystem monitoring.
    It is started as a thread and checks for changes every one second and
    enqueues the changes into a global queue"""
    global watchPath
    oldListing = os.listdir(watchPath)
    listing = []
    
    while 1:
        addList = []
        delList = []
        
        listing = os.listdir(watchPath)
        for entry in listing:
            if oldListing.count(entry) == 0:
                addList.append(entry)
            #else TODO: compare contents and verify same file
        for oldEntry in oldListing:
            if listing.count(oldEntry) == 0:
                delList.append(oldEntry)
                
        for item in addList:
            q.put(('CREATE', item, watchPath+item, os.path.isdir(watchPath+item)))
                
        for item in delList:
            q.put(('DELETE', item, watchPath+item, os.path.isdir(watchPath+item)))
        
        del oldListing[:]
        oldListing = copy(listing)
        time.sleep(1)

        
def cloudConnect(port, ftpIp):
    """Function to create and handle the TCP client side connection using the
    sockets API. (parameters: port, IP address to connect to)"""
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ftpIp, port))
    
    ftpThread = Thread(target=readQandFTP)
    ftpThread.start()

    while 1:
        # receive message from server
        data = s.recv(size)
        if data: 
            print "SRV_MSG: ", data 
            msg = data.split(' ')
            cmd = msg[0]
            fName = msg[1]
            fPath = msg[2]
            isDir = msg[3]
            
            if cmd == 'GET': #Push this data into queue so that FTP can RETR
                q.put(tuple(msg))
            elif cmd == 'DEL': #delete local file
                if os.path.isfile(watchPath+fName):
                    os.remove(watchPath+fName)
        else:
            s.close()
            break
            

def main():
    """This is the main function containing Android specific code for the 
    cloud sync application. The command line arguments can be specified but 
    have a default set since I could not find an easy way to supply them 
    when calling the script from the phone."""
    global ftpIp
    global watchPath
    
    usrOpts = getUsrOpts()
    #os.system('clear')
    print "options:", usrOpts
    mode = usrOpts[0]
    ip = usrOpts[1]
    portstr = usrOpts[2]
    if portstr != None:
        port = int(portstr)
    else:
        port = 5050
    watchPath = usrOpts[3]
    ftpIp = ip
    
    if mode == 'client':
        cloudConnect(port, ip)
    else:
        print 'Android only supports client mode'
    print "Exiting"
    sys.exit()

    
if __name__ == '__main__':
    main()
