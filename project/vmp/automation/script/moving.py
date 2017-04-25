from subprocess import call
import sys
import os


for filename in os.listdir("/home/root"):
    if "malware.exe_" in filename:
        print("mv " + filename)
        print(sys.argv)
        call(["mv", os.path.join("/home/root/" + filename), os.path.join("/home/root/automation/output/" + sys.argv[1] + "_" + filename.split("_")[1])])
