#!/bin/bash
service cron start
service apache2 start
tail -f /dev/null
