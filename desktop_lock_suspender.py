#!/usr/bin/env python
# Module     : session lock suspender program
# Synopsis   : Windows System tray icon.
# Programmer : Zbigniew Zasieczny - z.zasieczny@gmail.com
# Date       : 1 December 2016
# Notes      : Based on (i.e. ripped off from) Simon Brunning's
#              SysTrayIcon.py

from SysTrayIcon import SysTrayIcon
from threading import Thread
import ctypes
import time
import os


class SessionUnlockingThread(Thread):
    def __init__(self, app_ref):
        super(SessionUnlockingThread, self).__init__()

        self.setDaemon(True)
        self._app = app_ref
        self._mouse_event_generation_timeout_sec = 15

        self._mouse_event = ctypes.windll.user32.mouse_event
        self._MOUSEEVENTF_MOVE = 0x0001

    def run(self):
        while True:
            if str(self._app.icon).__contains__('unlock.ico'):
                print("generating mouse event")
                self._mouse_event(self._MOUSEEVENTF_MOVE, 0, 0, 0, 0)
            time.sleep(self._mouse_event_generation_timeout_sec)


if __name__ == '__main__':

    lock_icon = os.path.join(os.path.dirname('__file__'), 'lock.ico')
    unlock_icon = os.path.join(os.path.dirname('__file__'), 'unlock.ico')
    hover_text = "windows session lock suspender"


    def disable_lock(sysTrayIcon):
        sysTrayIcon.icon = unlock_icon
        sysTrayIcon.refresh_icon()
        print("disable session lock")


    def enable_lock(sysTrayIcon):
        sysTrayIcon.icon = lock_icon
        sysTrayIcon.refresh_icon()
        print("enable session lock")


    def left_ckick():
        print(">> left click")
        print("%s" % sys_tray_app.icon)
        if str(sys_tray_app.icon).__contains__('unlock.ico'):
            print("unlocked -> locked")
            enable_lock(sys_tray_app)
        else:
            print("locked -> unlocked")
            disable_lock(sys_tray_app)
        print("<< left click")


    def bye(sysTrayIcon):
        print('Bye, then.')

    menu_options = (('enable session locking', None, enable_lock),
                    ('disable session locking', None, disable_lock),
                    )

    sys_tray_app = SysTrayIcon(unlock_icon, hover_text, menu_options,left_click_action=left_ckick, on_quit=bye, default_menu_index=1)
    session_unlocking_thd = SessionUnlockingThread(sys_tray_app)
    session_unlocking_thd.start()
    sys_tray_app.start()

