#!/usr/bin/pythons
import time
import telnetlib
from subprocess import call
from subprocess import Popen
import sys
import os


for filename in os.listdir("/home/root"):
    if "malware.exe_" in filename:
        print("mv " + filename)
        if "hooklog" in filename:
            call(["mv", os.path.join("/home/root/" + filename),
                  os.path.join("/home/root/automation/output/" + sys.argv[2] + "_" + filename.split("_")[1])])