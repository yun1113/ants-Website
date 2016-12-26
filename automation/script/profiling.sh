#!/bin/bash
python /home/root/automation/script/winmalware.py /home/root/malware/$1 /home/root/automation/output/
python /home/root/automation/script/moving.py $1
