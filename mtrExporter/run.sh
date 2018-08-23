#!/bin/bash

cat <(crontab -e) <(echo "*/1 * * * * /opt/Monitoring/checkservice.sh >> /var/log/task.log 2>&1") | crontab - & \
cron & \
python3 /opt/Monitoring/ceilExporter.py & \
tail -f /dev/null