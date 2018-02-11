#!/bin/sh
/usr/sbin/smbd -D --configfile=/tmp/smb.conf
/usr/sbin/nmbd -D --configfile=/tmp/smb.conf
mount -o bind /mnt/sda1/opt /opt
/mnt/sda1/opt/sbin/nginx -c /mnt/sda1/opt/etc/nginx/nginx.conf
date >  /mnt/sda1/opt/test.txt
nohup python -u /mnt/sda1/opt/usr/openwrtpytest/utils/webhelper.py 2
>>/mnt/sda1/opt/usr/tmp/log 1>>/mnt/sda1/opt/usr/tmp/log &
/mnt/sda1/opt/bin/mysqld --defaults-file=/opt/etc/mysql/my.cnf
