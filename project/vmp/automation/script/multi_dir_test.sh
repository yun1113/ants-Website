FILES=/home/root/malware/*
for f in $FILES
do
	python winmalware.py $f /home/root/automation/output/
	sleep 30s
	rm /home/root/automation/output/*.trace	
	sleep 10s
	rm /home/root/automation/output/*.pcap
	sleep 10s
done
