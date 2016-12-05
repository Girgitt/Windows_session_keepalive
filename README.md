# desktop_lock_suspender
A tiny taskbar-icon type of program to disable windows auto-locking.

Windows build is available in dist folder. Just unpack and run the exe. 


Program stays in the taskbar and displays current operation mode using an icon:

 * red lock means desktop session will be locked according to the policy / windows settings

 * green lock means every N seconds a mouse event will be sent which resets (typically) session locking timeout

Lock suspension can be enabled or disabled using a context menu available under the right mouse button. 

Program also cycles the mode with a left-button double-click. 

