# Module     : session lock suspender program
# Synopsis   : Windows System tray icon.
# Programmer : Zbigniew Zasieczny - z.zasieczny@gmail.com
# Date       : 1 December 2016
# Notes      : Based on (i.e. ripped off from) Simon Brunning's
#              SysTrayIcon.py
"""
Copyright [2016] [Zbigniew Zasieczny]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from SysTrayIcon import SysTrayIcon
from threading import Thread
import ctypes
import time
import os
import logging
from logging.handlers import  RotatingFileHandler


def get_logging_format():
    return '%(asctime)s : %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'

logging.basicConfig(format=get_logging_format(), datefmt='%Y %b %d %H:%M:%S')

log = logging.getLogger('main')

logging.getLogger().setLevel(logging.DEBUG)

root_logger = logging.getLogger()

logfile_handler = RotatingFileHandler(os.path.join(os.path.dirname('__file__'), 'log.txt'),
                                      maxBytes=2048 * 1024,
                                      backupCount=2)
formatter = logging.Formatter(get_logging_format(),
                              datefmt='%b %d %H:%M:%S')
logfile_handler.setFormatter(formatter)
logfile_handler.setLevel(logging.DEBUG)
root_logger.addHandler(logfile_handler)



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
                log.info("generating mouse event")
                self._mouse_event(self._MOUSEEVENTF_MOVE, 0, 0, 0, 0)
            time.sleep(self._mouse_event_generation_timeout_sec)


if __name__ == '__main__':

    lock_icon = os.path.join(os.path.dirname('__file__'), 'lock.ico')
    unlock_icon = os.path.join(os.path.dirname('__file__'), 'unlock.ico')
    hover_text = "windows session lock suspender"


    def disable_lock(sysTrayIcon):
        sysTrayIcon.icon = unlock_icon
        sysTrayIcon.refresh_icon()
        log.info("disable session lock")


    def enable_lock(sysTrayIcon):
        sysTrayIcon.icon = lock_icon
        sysTrayIcon.refresh_icon()
        log.info("enable session lock")


    def left_ckick():
        print(">> left click")
        print("%s" % sys_tray_app.icon)
        if str(sys_tray_app.icon).__contains__('unlock.ico'):
            log.info("unlocked -> locked")
            enable_lock(sys_tray_app)
        else:
            log.info("locked -> unlocked")
            disable_lock(sys_tray_app)
        print("<< left click")


    def bye(sysTrayIcon):
        log.info('Bye, then.')

    menu_options = (('enable session locking', None, enable_lock),
                    ('disable session locking', None, disable_lock),
                    )

    sys_tray_app = SysTrayIcon(unlock_icon, hover_text, menu_options,left_click_action=left_ckick, on_quit=bye, default_menu_index=1)
    session_unlocking_thd = SessionUnlockingThread(sys_tray_app)
    session_unlocking_thd.start()
    sys_tray_app.start()

