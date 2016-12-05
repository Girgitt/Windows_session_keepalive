__author__ = 'zasiecznyz'

import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name="Windows session lock suspender",
        version="0.1",
        description="Windows session lock suspender",
        options={"build_exe": build_exe_options},
        executables=[Executable("desktop_lock_suspender.py", base=base)])
