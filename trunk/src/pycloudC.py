#!/usr/bin/python

"""Author: Vishal Verma"""


import os
import select
import socket
import sys
import getopt
import time
import pyinotify
from threading import Thread
import Queue
from ftplib import FTP, error_perm


#Global Queue for passing filesystem update messages
q = Queue.Queue()
ftpIp = ''
watchPath = ''


class EventHandler(pyinotify.ProcessEvent):
    """This is a sub-class to create overriding callback functions for 
    queueing inotify events. Each callback function enqueues 
    to a global queue"""
    def process_IN_CREATE(self, event):
        """This callback is used by pyinotify to notify for a file create 
        event in the watched directory"""
        if event.name[0] != '.':
            #print "Creating:", event.pathname
            #q.put(('CREATE', event.name, event.pathname, event.dir))
            pass

    def process_IN_DELETE(self, event):
        """This callback is used by pyinotify to notify for a file delete 
        event in the watched directory"""
        if event.name[0] != '.':
            print "Delete:", event.pathname
            #q.put(('DELETE', event.name, event.pathname, event.dir))
    
    def process_IN_DELETE_SELF(self, event):
        """This callback is used by pyinotify to notify for a file delete 
        event in the watched directory"""
        if event.name[0] != '.':
            print "Delete self:", event.pathname
            #q.put(('DELETE', event.name, event.pathname, event.dir))
        
    def process_IN_MODIFY(self, event):
        """This callback is used by pyinotify to notify for a file modify 
        event in the watched directory"""
        if event.name[0] != '.':
            #print "Modifying:", event.pathname
            #q.put(('CREATE', event.name, event.pathname, event.dir))
            pass
            
    def process_IN_CLOSE_WRITE(self, event):
        """This callback is used by pyinotify to notify for a file close  
        after modification event in the watched directory"""
        if event.name[0] != '.':
            #print "Close_write:", event.pathname
            q.put(('CREATE', event.name, event.pathname, event.dir))
    
    def process_IN_MOVE_SELF(self, event):
        """This callback is used by pyinotify to notify for a file move 
        event in the watched directory"""
        if event.name[0] != '.':
            print "Move_self:", event.pathname
            #q.put(('CREATE', event.name, event.pathname, event.dir))
        
    def process_IN_MOVED_FROM(self, event):
        """This callback is used by pyinotify to notify for a file move 
        event in the watched directory"""
        if event.name[0] != '.':
            #print "Move_from:", event.pathname
            q.put(('DELETE', event.name, event.pathname, event.dir))
    
    def process_IN_MOVED_TO(self, event):
        """This callback is used by pyinotify to notify for a file move 
        event in the watched directory"""
        if event.name[0] != '.':
            #print "Move_to:", event.pathname
            q.put(('CREATE', event.name, event.pathname, event.dir))
    
    def process_default(self, event):
        """This callback is used by pyinotify to notify for a default 
        event in the watched directory"""
        #print "Default event:", event.name, event.pathname, event.dir
        pass

        
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
    retlist = []
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
        usage()
        
    retlist.append(mymode)
    retlist.append(myip)
    retlist.append(myport)
    retlist.append(mypath)
    return retlist
        

def initWatches(watchPath):
    """Initialize the pynotify watches for the watched directory. 
    (parameters: path to watched directory)"""
    wm = pyinotify.WatchManager()  # Watch Manager
    mask = (pyinotify.IN_DELETE      | 
            pyinotify.IN_CREATE      |
            pyinotify.IN_MODIFY      |
            pyinotify.IN_CLOSE_WRITE |
            pyinotify.IN_MOVED_FROM  |
            pyinotify.IN_MOVED_TO    |
            pyinotify.IN_MOVE_SELF)
    #mask = pyinotify.ALL_EVENTS
    notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
    notifier.start()
    notifier.coalesce_events()
    wdd = wm.add_watch(watchPath, mask, rec=True, auto_add=True)
    print "Added watches at:", watchPath
    return wm, wdd, notifier


def killWatches(wm, wdd, notifier):
    """Stop the previously set watches"""
    wm.rm_watch(wdd.values())
    notifier.stop()
    print "Stopped Watches"


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
        retval = ftp.retrbinary('RETR '+fName, \
                                open(watchPath+fName, 'wb').write)
        print 'FTP:', retval

        
def readQandFTP():
    """Function (thread) to dequeue a command from the global actions queue 
    and perform the appropriate FTP command (store/retrieve/delete"""
    global ftpIp
    ftp = FTP(ftpIp)
    ftp.login('stellarhopper', 'hoppingstar')
    retval = ftp.retrlines('NLST', ftpGetFile)
    print "FTP Listing and Syncing: ", retval
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
                ftpGetFile(fName)
    #TODO: Find a good way to end this thread

    
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
    

def serveCloud(port, notifier):
    """Function to act as the TCP server (cloud) where clients would connect
    to. (parameters: port to serve on and 'notifier' object from pyinotify"""
    host = '' 
    backlog = 5 
    size = 1024 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((host,port)) 
    server.listen(backlog) 
    inputs = [server,sys.stdin] 
    clients = []
    running = 1 
    while running: 
        inputready,outputready,exceptready = select.select(inputs, [], [], 0) 
        for s in inputready: 
            if s == server: 
                # handle the server socket 
                client, address = server.accept() 
                inputs.append(client) 
                clients.append(client) 
            elif s == sys.stdin: 
                # handle standard input 
                junk = sys.stdin.readline() 
                running = 0 
            else: 
                # handle all other sockets 
                data = s.recv(size) 
                if data: 
                    s.send(data) 
                    #handle client requests here if any
                else: 
                    s.close() 
                    inputs.remove(s) 
                    clients.remove(s)
        #monitor fs for changes here:
        try:
            qMsg =  q.get(block=False)
            cmd = qMsg[0]
            fName = qMsg[1]
            fPath = qMsg[2]
            isDir = qMsg[3]
            if cmd == 'CREATE':
                cliCmd = 'GET ' + fName + ' ' + fPath + ' ' + str(isDir)
            elif cmd == 'DELETE':
                cliCmd = 'DEL ' + fName + ' ' + fPath + ' ' + str(isDir)
            print 'ACTIVITY: cliCmd =', cliCmd
            sys.stdout.flush()
            for s in clients:
                s.send(cliCmd)

        except Queue.Empty:
            pass
    
    server.shutdown(socket.SHUT_RDWR)            
    server.close()


def main():
    """This is the main function for the cloud sync application. The command
    line arguments decide whether it will go into server or client mode"""
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
    
    wm, wdd, notifier = initWatches(watchPath)
    
    if mode == 'server':
        print "Serving on Port %d" % (port)
        serveCloud(port, notifier)
    elif mode == 'client':
        cloudConnect(port, ip)
    
    killWatches(wm, wdd, notifier)
    print "Exiting"
    sys.exit()

    
if __name__ == '__main__':
    main()
