Project Goals
=============

-------------------------------------------------------------------------------------
**GOAL-1:** *Develop an application script to monitor updates to selected folders.*
-------------------------------------------------------------------------------------
^^^^^^^^^^^^^^^^
Original Goal
^^^^^^^^^^^^^^^^
This involved developing a system to monitor a selected directory

^^^^^^^^^^^^^^^
Goal Achieved?
^^^^^^^^^^^^^^^

    I achieved this goal with two different methods - one for the Linux clients and other for the Android phone clients.

^^^^^^^^^^^^^^^^^^^^^^^^
How did I achieve it?
^^^^^^^^^^^^^^^^^^^^^^^^

Medhod 1: (Linux computer clients)
    - I used the Inotify system in Linux (Kernels 2.6 > only)
    - It allows you to set 'watches' on directories
    - The watch can be configured to detect recursive actions and auto-add new subdirectories
    - The 'pyinotify' module provides python bindings for inotify

Method 2: (Android clients)
    - I was not able to use the above method for Android even though the inotify subsystem is present in the Linux kernel running on the phone.
    - The reason is I could not install pyinotify on the phone or inotify-tools (which is a set of command line wrappers to access the inotify system possibly from a script)
    - I used the os module to get a listing every one second and compare with the previous version to track filesystem changes.

------------------------------------------------------------------------------------
**GOAL-2:** *Develop an FTP/push notification subsystem to send updates.*
------------------------------------------------------------------------------------
^^^^^^^^^^^^^^^^
Original Goal
^^^^^^^^^^^^^^^^

    The goal was to use FTP for actual file transfers because it was easy to use with the available python library and it also provided a web interface to access the server via a browser or an FTP client.

^^^^^^^^^^^^^^^
Goal Achieved?
^^^^^^^^^^^^^^^

    The goal was achieved using ftplib.

^^^^^^^^^^^^^^^^^^^^^^^^
How did I achieve it?
^^^^^^^^^^^^^^^^^^^^^^^^

    I had good knowledge of the FTP protocol having worked with it in the past, so using ftplib was not too difficult. Ftplib was directly accessible from Linux on the computers, and I had to put the source file ftplib.py into the working directory on the phone. Interpreting the FTP responses was trivial.

---------------------------------------------------------------------------------------------
**GOAL-3:**  *Sync to a Network Attached Storage and extend application to mobile devices*
---------------------------------------------------------------------------------------------

^^^^^^^^^^^^^^^^
Original Goal
^^^^^^^^^^^^^^^^

    The goal was to allow sync to a NAS with a samba server and extension to an Android phone. Android seemed feasible because it runs a Linux kernel and has apps to run a python interpreter.

^^^^^^^^^^^^^^^
Goal Achieved?
^^^^^^^^^^^^^^^

    Partially. I have full functionality as intended on Android but I did not implement the samba client to sync to NAS devices.

^^^^^^^^^^^^^^^^^^^^^^^^
How did I achieve it?
^^^^^^^^^^^^^^^^^^^^^^^^

    First I installed the SL4A app (Scripting Layer for Android) on my Android phone. This provides an infrastructure for various scripting interpreters such as python, perl, lua etc.
    Next I installed Python for Android (Py4A). This is a python interpreter for Android. 
    This made most things easy after the initial setup. I was able to use most python modules for directory/file access.
    The ftplib module was not pre-installed on the phone so I downloaded the source file 'ftplib.py' and put it in my working directory.
    The pyinotify module was not installable on android since it required re-compilation. I created my own filesystem monitoring system to replace this.
