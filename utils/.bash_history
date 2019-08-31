netstat -atpn
curl -x 192.168.1.122:8083 https://github.com/
curl -x 192.168.1.122:8083 http://www.baidu.com
netstat -atpn
curl -x 192.168.1.122:8000 http://www.baidu.com
curl -x 127.0.0.1:8000 http://www.baidu.com
curl -x localhost:8000 http://www.baidu.com
#-*- coding: UTF-8 -*-
import socket,select
import sys
import thread
from multiprocessing import Process
class Proxy:
def __init__(self,soc):
self.client,_=soc.accept() one
self.request_url=None
self.BUFSIZE=4096
self.method=None
self.targetHost=None
def getClientRequest(self):
request=self.client.recv(self.BUFSIZE)
if not request:;   =request.find('\n')
firstLine=request[:cn]
print firstLine[:len(firstLine)-9]
line=firstLine.split()
self.method=line[0]
self.targetHost=line[1]
return request
def commonMethod(self,request):
tmp=self.targetHost.split('/')
net=tmp[0]+'//'+tmp[2]
request=request.replace(net,'')
self.getTargetInfo(tmp[2])
self.target.send(request)
self.nonblocking() def connectMethod(self,request):
con='HTTP/1.1 200 Connection established\r\nProxy-agent: tinyproxy0.1\r\n\r\n'
self.client.send(con)
self.getTargetInfo(self.targetHost)
self.nonblocking() def run(self):
request=self.getClientRequest()
if request:;  ['GET','POST','PUT',"DELETE",'HAVE']:; Method(request)
elif self.method=='CONNECT':
self.connectMethod(request)
def nonblocking(self,timeout=3):
inputs=[self.client,self.target]
while True:; puts,[],inputs,timeout)
if errs:;  readable:; t:; d(data)
elif soc is self.target:
self.client.send(data)
else:
break
self.client.close() fo(self,host):
port=0
site=None
if ':' in host:; t(tmp[1])
else:
site=host
port=80
try:
(fam,_,_,_,addr)=socket.getaddrinfo(site,port)[0]
except Exception as e:
print e
return
self.target=socket.socket(fam)
self.target.connect(addr)
if __name__=='__main__':; from multiprocessing import Process
netstat -atpn
kill 475
kill 975
netstat -atpn
curl -x 192.168.1.122:8083 http://www.baidu.com
netstat -atpn
netstat -atpn
kill 1012
cat /etc/rc.local
python monitorhelper.py
python monitorhelper.py
python ../refer/tinyproxy.py
python ../refer/tinyproxy.py
python ../refer/tinyproxy.py
python ../refer/tinyproxy.py
python ../refer/tinyproxy@.py
cat /etc/profile
curl -x 192.168.1.1:1080 https://github.com
curl -x 192.168.1.1:1080 http://www.baidu.com
curl -x 192.168.1.1:1080 http://www.baidu.com
curl -x 192.168.1.1:1080 http://www.baidu.com
ifconfig
curl -x 192.168.1.1:1080 http://www.baidu.com
python monitorhelper.py
curl -x 192.168.1.1:1038 "http://www.baidu.com"
curl -x 192.168.1.1:1038 "http://www.baidu.com"
curl -x 192.168.1.1:1038 "http://www.baidu.com"
ping www.baidu.com
curl -x 192.168.1.1:1080 "http://www.baidu.com"
python
curl -x 192.168.1.1:1080 "http://www.baidu.com"
curl -x 192.168.1.1:1080 "http://www.baidu.com"
curl -v --socks5-hostname 192.168.1.1:1080 'http://www.baidu.com'
ausearch -m avc -ts today | audit2allow
/etc/init.d/tinyproxy --help
/etc/init.d/tinyproxy --start
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
apt-get remove --purge tinyproxy
grep mongdb /etc/passwd
/etc/passwd | grep mongdb
/etc/passwd
cat /etc/passwd
ls /etc/
ls /etc/crontab
date > /mnt/sda1/temp/DHCPACK.txt
apt-get install mongodb
pecl search mongo
python monitorhelper.py
/etc/init.d/mongod
/etc/init.d/mongod start
systemctl status mongo.service
journalctl -xe
adduser --firstuid 100 --ingroup nogroup --shell /etc/false --disabled-password --gecos "" --no-create-home mongodb
adduser --firstuid 100 --ingroup nogroup --shell /etc/false --disabled-password --gecos "" --no-create-home mongodb
passwd mongodb
/etc/init.d/mongod start
journalctl -xe
mongod
/usr/mongo/bin/mongodb
/usr/mongo/bin/mongo
chown mongodb:nogroup /var/log/mongodb/
chown mongodb:nogroup /var/lib/mongodb/
chmod u+x /etc/init.d/mongod
/etc/init.d/mongod start
journalctl -xe
systemctl daemon-reload
systemctl list-units --failed
logread
logread
systemctl cat mongod.service
mongod
netstat -atpn
/etc/init.d/tinyproxy
/etc/init.d/tinyproxy start
apt-get remove tinyproxy
apt-get install tinyproxy
chmod u+x /etc/init.d/mongod
apt-get install mongodb
apt-get install mongodb-server
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
/etc/init.d/tinyproxy start
apt-get upgrade -f
apt-get install build-essential libboost-filesystem-dev libboost-program-options-dev libboost-system-dev libboost-thread-dev scons libboost-all-dev python-pymongo git
apt-get remove --purge tinyproxy
ls /var/log/tinyproxy
cat /var/log/tinyproxy/tinyproxy.log
apt-get install tinyproxy
/etc/init.d/tinyproxy start
netstat -atpn
/etc/init.d/tinyproxy stop
nano /etc/tinyproxy.conf
/etc/init.d/tinyproxy start
curl -x 192.168.1.122:8888 'https://github.com'
cd ~
git clone https://github.com/skrabban/mongo-nonx86
cd mongo-nonx86
scons
ls /var/log
ls /var/log/mongodb
cat /var/log/mongodb
cd /var/log/mongodb
ls
/etc/init.d/mongod
/etc/init.d/mongod start
journalctl -xe
git clone https://github.com/mongodb/mongo.git
ls
cd mongo
ls
cd debian
ls
cd ~
git clone git://github.com/RickP/mongopi.git
cd mongopi
scons
curl -x 192.168.1.1:8888 'http://www.baidu.com'
curl -x 192.168.1.1:8888 'http://www.baidu.com'
mysql
mysql
mysql -u root 
mysql -u root -p log
