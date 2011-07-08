Tutorial
=======================================

The desktop and client use the same python script 'pycloudC.py' called with different arguments. The android phone has a different script called 'pycloudAndroid.py'

---------------------
Code options:
---------------------
The different command line options for the script configure it to runn in different modes and with specific parameters.

|   ``--mode <server or client>``
|   This specifies the mode of the script
|   Options are server or client

|   ``--ip <IP_address>``
|   This specifies IP address to connect to (client only)
|   It should be a valid reachable IP
|   Ex: --ip 10.0.1.9

|   ``--port <portnumber>``
|   This specifies the port to listen on (server) or to connect to (client)
|   Valid range is any unused TCP port between 1-65535 (Pref. higher than 1024)
|   Ex: --port 4566

|   ``--path <watch_path>``
|   This specifies the watch path for the client or server
|   It should be a valid, FULL path (with permissions) on the device.
|   Make sure to have a trailing '/' in the path.
|   Ex: /home/ftp

|   ``-h``
|   This displays usage help


--------------------------
Running the applications
--------------------------
| Note: Always run the server first followed by the client/clients.
| Note: You need to have root access while runnng the server.
| Note: Make sure that the ports that you use are not blocked by the network.

| To run the server:

| ``bash# ./pycloudC.py --mode server --port 5050 --path /home/ftp/``

| To run each client:

| ``bash# ./pycloudC.py --mode client --ip 10.0.1.9 --port 5050 --path /home/Desktop/watchDir1/``

---------------------
Operation
---------------------

Create or delete any files in the watched directories. The changes should reflect in all the clients.


