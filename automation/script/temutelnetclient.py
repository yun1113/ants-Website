#!/usr/bin/python

import time
import telnetlib
from subprocess import call
from subprocess import Popen
import sys
import os
#import gtk.gdk 
#import wnck

##--------------------------------------------------------------------------------
## Setting part
## In this part, you should fill in every lines in order to make this automation work
## plugin_dir:
#  this points to tracecap.so in you temu folder
#  should be something like /path/to/temu/tracecap/tracecap.so
plugin_dir ="/home/root/temu-ants/tracecap/tracecap.so" 
## trace_tmp_file:
#  This is for collecting data from tmp to result folder,
#  If you are running Mike's version of temu, remember that the output should be the same
#  directory of this script
#  should look like /path/to/automation/*.trace
#  the * is crucial for collecting all correct data, will make you result incorrect if not used
#  hint: this should be the same as ../output/malware.exe_.......... from script's location
trace_tmp_file="/home/root/automation/output/*.trace"

#========================
#Note that pcap is no longer used inside temu in this automation, related stuff will be deleted in the final version
## pcap_tmp_file:
#  This points to the pcap file you wrote from guest os, should locate somewhere in your smb shared folder
#  to see where the default output is, check temuactionlist
#  Should look like /path/to/smbfolder/malware.pcap 
#pcap_tmp_file = "/home/ted/vmresult/malware.pcap"
#=========================
pcap_result_dir = '/home/root/automation/output/'

## png_tmp_file:
#  This points to the screenshot you took in the testing process
#  see where you save it in the screenshot function
png_tmp_dir = "/home/root/automation/script/output/"
png_tmp_file ="/home/root/automation/script/output/*.png"

ppm_tmp_dir = "/home/root/automation/script/output"
ppm_tmp_file = "/home/root/automation/script/output/*.ppm"
##---------------------------------------------------------------------------------




##----------------------------------------------------------------------------------------------------------------------------
##functions:
#def screenshot(filename):
#	print 'taking screenshot...'
#	screen = wnck.screen_get_default()
#	screen.force_update()
#	activeWindow = screen.get_active_window()
#	activeWindowGeometry = activeWindow.get_geometry()
#
#	rootWindow = gtk.gdk.get_default_root_window()    
#	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,activeWindowGeometry[2],activeWindowGeometry[3])
#	pb = pb.get_from_drawable(rootWindow,rootWindow.get_colormap(),activeWindowGeometry[0],activeWindowGeometry[1],0,0,activeWindowGeometry[2],activeWindowGeometry[3])
#	pb.save(png_tmp_dir+filename,"png")
#
def screendump (qemutelnet,filename):
	print 'taking screenshot by qmp'
	#print 'ask for capability, this is said to be a must'
	#qemutelnet.write('qmp_capabilities\n')
	#readresult = qemutelnet.read_until('(qemu)')
	#print readresult

	print 'screendump command'
	qemutelnet.write('screendump ' + ppm_tmp_dir + "/" + filename + ".ppm\n")
	readresult = qemutelnet.read_until('(qemu)')
	print readresult
##----------------------------------------------------------------------------------------------------------------------------	
	
##start up, check input parameters and set telnet host&port
print 'Enter temutelnetclient with three parameters: ' + str(sys.argv)
resultpath =  sys.argv[1]
HOST = "localhost"
PORT = 4444

##wait for temu to enter a stable phase
print 'starting WinXP in 200 seconds.....'  
time.sleep(200)
print 'starting WinXP is done.'

print 'starting tshark on the outside world'
Popen (['tshark', '-i', 'eth0', '-a', 'duration:360', '-w' , pcap_result_dir+sys.argv[2] +'.pcap'])

##launch telnet connection
print 'start interacting with qemu on telnet:localhost:4444'
qemutelnet = telnetlib.Telnet( HOST,PORT )
qemutelnet.open(HOST,PORT)

##check response if connection is connected correctly
print 'successfully telnet connected to qemu.'
readresult = qemutelnet.read_until('(qemu)')
print readresult

##load plugin
qemutelnet.write('load_plugin '+plugin_dir+'\n')
#print 'wrote load_plugin' + plugin_dir 
time.sleep(8)
readresult = qemutelnet.read_until('(qemu)')
print readresult

##set up trace target, note that directory is no longer needed if using temu-1006+
qemutelnet.write('tracebyname malware.exe \"' + trace_tmp_file +'\"\n')
#print 'wrote tracebyname malware.exe "'+ trace_tmp_file +'"'
time.sleep(10)
readresult = qemutelnet.read_until('(qemu)')
print readresult

##load hooks, only work when using temu-1006+
qemutelnet.write('load_hooks \"\" \"\"\n')
#print 'wrote load_hooks \"\" \"\"'
time.sleep(8)
readresult = qemutelnet.read_until('(qemu)')
print readresult


##start emulation
qemutelnet.write('enable_emulation\n')
#print 'wrote enable_emulation'
time.sleep(5)
readresult = qemutelnet.read_until('(qemu)')
print readresult



## Read from action list
print 'reading action list...'
actionlist = open('/home/root/automation/script/temuactionlist','r')
actionarray = actionlist.readlines()
for action in actionarray:
	print 'going to process action = ' + action
	if action[0][0] == 'a':
		qemutelnet.write(action[1:])
		#print 'wrote' + action[1:1] + ' to qemu'
		readresult = qemutelnet.read_until('(qemu)')
		print readresult
		time.sleep(5)
	else:
		print 'not a valid action, skipping line'

## start recording malware behavior, takes screenshot every 1 minute
#screenshot("0min.png")
screendump(qemutelnet,"0min")
print 'Start recording malware behavior'
time.sleep(60)
#screenshot("1min.png")
screendump(qemutelnet,"1min")
time.sleep(60)
#screenshot("2min.png")
screendump(qemutelnet,"2min")
time.sleep(60)
#screenshot("3min.png")
screendump(qemutelnet,"3min")
time.sleep(60)
#screenshot("4min.png")
screendump(qemutelnet,"4min")
time.sleep(60)
#screenshot("5min.png")
screendump(qemutelnet,"5min")

#ending phase
#print 'copy result before ending...'
qemutelnet.write('trace_stop\n')
time.sleep(5)
readresult = qemutelnet.read_until('(qemu)')
print readresult

qemutelnet.write('unload_plugin\n')
time.sleep(10)
readresult = qemutelnet.read_until('(qemu)')
print readresult

#closing temu
print 'quit temu'
qemutelnet.write('quit\n')

#copy result, might create some error because file not found (which should be normal)
# if not os.path.isdir(resultpath):
# 	os.mkdir(resultpath)
# if not "/" in resultpath[0][0]:
# 	resultpath = resultpath + "/"
# call(["mv",trace_tmp_file,resultpath])
# call(["mv",trace_tmp_file+".functions",resultpath])
# call(["mv",trace_tmp_file+".netlog",resultpath])
# call(["mv",trace_tmp_file+".calls",resultpath])
# call(["mv",trace_tmp_file+".hooklog",resultpath])
# call(["mv",ppm_tmp_file,resultpath])

#rename
# for dirpath,dirname,filename in os.walk("/home/root"):
# 	for fn in filename:
# 	  	print(fn)
# 	  	if "malware" in fn:
# 		  	print "result name = " + sys.argv[2] + fn.split("_")[1]
# 		  	call(["mv",os.path.join(dirpath,fn),os.path.join(dirpath,sys.argv[2] +"_"+ fn.split("_")[1])])

for filename in os.listdir("/home/root"):
	if "malware.exe_" in filename:
		print("mv " + filename)
		call(["mv",os.path.join("/home/root/" + filename),os.path.join("/home/root/automation/output/" + sys.argv[2] + "_" + filename.split("_")[1])])
		
qemutelnet.close()
print 'End of program'
sys.exit()