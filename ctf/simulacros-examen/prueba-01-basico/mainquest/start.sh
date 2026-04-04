#!/bin/bash
service cron start
service apache2 start
vsftpd /etc/vsftpd.conf &
cd /opt/webapp && python3 app.py
