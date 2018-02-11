#!/bin/sh
cat /mnt/sda1/opt/var/log/nginx/host.access.log  > "/mnt/sda1/opt/var/log/nginx/nginx`(date +"%Y%m%d%H%M%S").log`"
