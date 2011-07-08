Code
=======================================
=================
Code Description
=================
The server client code is uses a simple socket connection for command exchange and an FTP client and server for data transfer. 
Here is a description of the code

----------------------
Linux Server/Client
----------------------

| **Server Mode:**
|    1. The server listens on a TCP socket to await clients
|    2. It starts pyinotify watches on the specified directory
|    3. The pyinotify callbacks enqueue directory changes which are broadcast to all clients
|    4. The queue is emptied by the server function in a loop and the messages are sent across the TCP connection.
|    5. The command sends all the info needed to retrieve the changed files via FTP or to delete files.
    
| **Client Mode:**
|    1. The clients connect to the specified server
|    2. It starts pyinotify watches on the specified directory
|    3. The pyinotify callbacks enqueue changes
|    4. A thread dequeues the changes and performs the appropriate FTP commands.
|    5. The client function also listens to messages from the server to either enqueue a retrieve command or to delete a local file.

-----------------
Android Client
-----------------

The Android Client differs in the following way:
|   1. The pyinotify module is not available on Android
|   2. My monitorFS function gets a directory listing every second and compares it to the previous listing.
|   3. It then Lists the additions and deletions and enqueues appropriate commands
|   4. These commands are then dequeued by the same thread as above.
    

======================
Code AutoDocumentation
======================

---------------------
Linux Client/Server
---------------------

The description of the various modules in the code are as follows:

.. automodule:: pycloudC
   :members:

-----------------
Android Client
-----------------

The description of the various modules in the code are as follows:

.. automodule:: pycloudAndroid
   :members:

   
