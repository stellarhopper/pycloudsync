Pre-requisites
=======================================
The following procedure is for installation on Ubuntu.

There are some packets required for the system to work.
You will need:

    * Python 2.6 or higher
    * ftplib
    * build-essential
    * pyinotify

-------------------------------
Setup Procedure
-------------------------------

^^^^^^^^^^^^^^^^^^
Install Python
^^^^^^^^^^^^^^^^^^
This will install python
    | ``bash# apt-get install python``

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install ftplib and pyinotify
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    | ``bash# easy_install ftplib``
    | ``bash# easy_install pyinotify``
    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install pureftpd and configure on server side
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    | ``bash# sudo apt-get install pureftpd``

| Configure pureftpd as per available documentation and set ftp root path to /home/ftp
| Since this path will belong to user 'ftpuser', all accesses to this will have to be as root


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Preparing the Android phone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| Google for 'SL4A' and install the app using the QR code on the googlecode page
| From SL4A get the python interpreter; it will download Py4A.
| Put the ftplib.py source in the working directory, along with pyclourAndroid.py
| Install an SSH daemon app (I used quickSSHd) to gain access to a linux shell on the phone.
| On this Linux shell, set some environment variables:

    | ``PYTHONPATH=/data/data/com.googlecode.pythonforandroid/files/python/lib/python2.6/lib-dynload``
    | ``PYTHONPATH=${PYTHONPATH}:/mnt/sdcard/com.googlecode.pythonforandroid/extras/python``
    | ``export PYTHONPATH``
    | ``export PYTHONHOME=/data/data/com.googlecode.pythonforandroid/files/python``
    | ``export LD_LIBRARY_PATH=/data/data/com.googlecode.pythonforandroid/files/python/lib``

| Test the setup by typing 'python' anywhere from the shell and the interpreter should start.

