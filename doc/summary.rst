Project Summary
===============
A summary of the concept and functionality:

===================
Summary
===================
The pycloud project allows the user to select a particular folder as a 'watched' folder and synchronizes this folder with a server and other clients connected. New clients connecting with a blank folder get a copy of the current state at the server and future modifications are synchronized. Android clients are also supported and this provides an excellent way to synchronize photos and music from the phone to a desktop opn the same network.

============================
Scope
============================
The project performs the above functionality for Android phones which have 'Scripting Layer for Android' and 'Python for Android' installed.
Watch support is for a single directory currently but can easily be extended to do this recursively (some support is included but the code needs a lot of fine tuning for that. It is disabled in the current state)
On initial sync file presence is only checked by filename, not file contents. All subsequent modifications are however tracked.
I have not added support for storage onto a samba server due to time constraints.
