from subprocess import call
import sys
import os

base_dir = '/home/root/'
target_dir = '/home/root/automation/output/'

for filename in os.listdir(base_dir):
    if ".trace." in filename:
        print("mv " + filename)
        call(["mv", os.path.join(base_dir + filename), os.path.join(target_dir + sys.argv[1] + "_" + filename.split("_")[1])])
