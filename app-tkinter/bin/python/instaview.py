#!/usr/bin/env python3

import platform
import os

if __name__ == '__main__':

    path = input("Enter the absolute path to your data directory:\n")
    script = "bin/python/requesthandler.py instaview"
    if "Windows" in platform.system():
        cmd = "python " + script + " " + path
        os.system(cmd)
    else:
        cmd = "python3 " + script + " " + path
        os.system(cmd)
