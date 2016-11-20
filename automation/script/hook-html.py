import sys

#input_dir="/mnt/container_storage/webapp/automation/output/"
#output_dir="/mnt/container_storage/webapp/vmp/malwaredb/templates/"

input_dir="/home/profile/website/automation/output/"
output_dir="/home/profile/website/project/vmp/malwaredb/templates/"

output = '<html>\n'

fin = open(input_dir+sys.argv[1],"rt")
#output += '<html>\n'
#with open("D:\f73a5ae9590342c6f77276690508ec510d5ccf4bbd24fb9bab9a03c3d9c2eecb_3132.trace.hooklog","r") as fin:

for line in fin:
    output += line
    output += '</br>'
output += '\n</html>'

fout = open(output_dir+sys.argv[1].split('_')[0]+'.html',"wt")
size = len(output)
offset = 0
chunk = 100

#finish = False

while offset <= size:
    fout.write(output[offset:offset+chunk])
    offset += chunk

fout.write(output)
fout.close()

#fout.write(output)
#fout.close()