#!/bin/bash

#CHECK API
code=$(curl --write-out %{http_code} --silent --output /dev/null http://127.0.0.1:9091/metrics)

if [ $code != 200 ]
then
	#GET service pid
	procID=$(ps -aux | grep run.sh | grep -v "grep" | awk '{print $2}')
		if [ -n procID ]
		then
		 	#KILL service
			kill $procID
		fi
	#Restart service
	/usr/local/bin/python3 /opt/Monitoring/ceilExporter.py &
	echo $(date '+%d/%m/%Y %H:%M:%S')
fi