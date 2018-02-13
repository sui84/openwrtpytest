#!/bin/sh
cat /mnt/sda1/opt/var/log/nginx/host.access.log  > "/mnt/sda1/opt/var/log/nginx/nginx`(date +"%Y%m%d%H%M%S").log`"
:> /mnt/sda1/opt/var/log/nginx/host.access.log
cd /mnt/sda1/opt/usr/openwrtpytest/utils
nohup  python -u /mnt/sda1/opt/usr/openwrtpytest/utils/log/nginxhelper.py nginx_db >>/mnt/sda1/opt/var/log/nginx/test.log
