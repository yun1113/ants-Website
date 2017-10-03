#!/bin/bash
if $2
then
    echo $1 $3 $4
    python /home/root/automation/script/watch.py $1 $3 $4 &
fi
(python /home/root/automation/script/winmalware.py /home/root/malware/$1 /home/root/automation/output/; python /home/root/automation/script/moving.py $1)
