<<<<<<< HEAD
from scapy.all import *
import scapy_http.http as HTTP
from scapy.error import Scapy_Exception
try:
    import scapy.all as scapy
except ImportError:
    import scapy
import commonhelper

try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http

#sniff(iface=conf.iface,count=100)

#python net-creds.py -v

face = conf.iface  #'pppoe-wan'
cnt = 1000
print RandMAC()


def SanPort(ip,ports):
    # ports = (80,83)  SA open , RA not open
    ans=sr(IP(dst=ip)/TCP(dport=ports,flags="S"))
    for an in ans:
        an.summary()

def GetMac():
    ipscan='192.168.1.1/24'
    try:
        ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan),timeout=2,verbose=False)
    except Exception,e:
        print str(e)
    else:
        for snd,rcv in ans:
            list_mac=rcv.sprintf("%Ether.src% - %ARP.psrc%")
            print list_mac

def GetPkgFromFile(pkgpath,cnt=100):
    pkgs = PcapReader(pkgpath)
    npkgs = []
    #for i in range(0,cnt):
    i = 1
    for pkg in pkgs:  
        if(i>cnt):
            break
        npkgs.append(pkg)
        i+=1
    return npkgs
                
def GetPkg(fpath):
    pkgs=rdpcap(fpath)
    return pkgs

def SaveHttp(fpath):
    pkgs=sniff(iface=face,prn=lambda x:x.summary(),filter='tcp port 80',count=cnt)
    pkgs[0].show()
    wrpcap(fpath,pkgs)

def MakePkg(url):   
    host,path = commonhelper.GetUrlPath(url)
    pkt=Ether()/IP(dst=host)/TCP()/"GET %s HTTP/1.0 \n\n" % path
    return pkt
    

def SavePkg(fpath,type):
    # type : tcp , udp ,icmp
    pkgs=sniff(iface=face,filter=type,count=cnt)
    pkgs[0].show()
    wrpcap(fpath,pkgs)
    #PA flag
    #pkg=sniff(iface=face,prn=lambda x:x.summary(),filter='tcp[13:1]==24')

def AppendPkg(fpath,pkg):
    pktdump = PcapWriter(fpath, append=True, sync=True)
    pktdump.write(pkg)


def ShowPayload(pkg):
    if HTTP.HTTPRequest in pkg:
        print 'HTTPRequest'
    if HTTP.HTTPResponse in pkg:
        print 'HTTPResponse'
    print pkg.payload
    
def ShowRawData(pkg):
    if pkg.haslayer(TCP) and (pkt.getlayer(TCP).dport == 80 or pkt.getlayer(TCP).dport == 443) and pkg.haslayer(Raw):
        print pkg.getlayer(Raw).load

def SetRawData(pkg):
    hexdump(Ether()/"1234567891".decode("hex"))

def SendPkg(pkg):
    sendp(pkg)
    #p=srloop(IP(dst="www.baidu.com",ttl=1)/ICMP(),inter=3,count=2)



def ShowPkgInfo(pkg):
    print hexdump(pkg)
    print str(pkg)
    print pkg.summary()
    print pkg.show()
    print pkg.display()
    print pkg.load   # http 
    print pkg.payload
    pkg.sprintf('%load%')
    
    #result=sr1(IP(dst=domain)/TCP(dport=port,flags="S"),timeout=10)
    #pkg[TCP].flags
    
#a=IP()/TCP()/"GET / HTTP/1.0\r\n"



def synscan(domain,port):
    result=sr1(IP(dst=domain)/TCP(dport=port,flags="S"),timeout=10)
    if result:
        print 'got answer'
        if (result[TCP].flags==18):
            print 'port open'
    else:
        print 'not got answer'


def traceroute(): 
    ans,unans=sr(IP(dst="www.baidu.com",ttl=(2,25),id=RandShort())/TCP(flags=0x2),timeout=50)  
    for snd,rcv in ans:  
        print snd.ttl,rcv.src,isinstance(rcv.payload,TCP)
        

    
'''
import pcap
pc=pcap.pcap(face)
pc.setfilter('tcp port 80')
'''

if __name__ == '__main__':
    #pcap = sniff(offline = "xx/xx.pcap")
    #synscan('www.jinglingshu.org',80)
    synscan('www.baidu.com',80)

=======
from scapy.all import *
import scapy_http.http as HTTP
from scapy.error import Scapy_Exception
try:
    import scapy.all as scapy
except ImportError:
    import scapy
import commonhelper

try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http

#sniff(iface=conf.iface,count=100)

#python net-creds.py -v

face = conf.iface  #'pppoe-wan'
cnt = 1000
print RandMAC()


def SanPort(ip,ports):
    # ports = (80,83)  SA open , RA not open
    ans=sr(IP(dst=ip)/TCP(dport=ports,flags="S"))
    for an in ans:
        an.summary()

def GetMac():
    ipscan='192.168.1.1/24'
    try:
        ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan),timeout=2,verbose=False)
    except Exception,e:
        print str(e)
    else:
        for snd,rcv in ans:
            list_mac=rcv.sprintf("%Ether.src% - %ARP.psrc%")
            print list_mac

def GetPkgFromFile(pkgpath,cnt=100):
    pkgs = PcapReader(pkgpath)
    npkgs = []
    #for i in range(0,cnt):
    i = 1
    for pkg in pkgs:  
        if(i>cnt):
            break
        npkgs.append(pkg)
        i+=1
    return npkgs
                
def GetPkg(fpath):
    pkgs=rdpcap(fpath)
    return pkgs

def SaveHttp(fpath):
    pkgs=sniff(iface=face,prn=lambda x:x.summary(),filter='tcp port 80',count=cnt)
    pkgs[0].show()
    wrpcap(fpath,pkgs)

def MakePkg(url):   
    host,path = commonhelper.GetUrlPath(url)
    pkt=Ether()/IP(dst=host)/TCP()/"GET %s HTTP/1.0 \n\n" % path
    return pkt
    

def SavePkg(fpath,type):
    # type : tcp , udp ,icmp
    pkgs=sniff(iface=face,filter=type,count=cnt)
    pkgs[0].show()
    wrpcap(fpath,pkgs)
    #PA flag
    #pkg=sniff(iface=face,prn=lambda x:x.summary(),filter='tcp[13:1]==24')

def AppendPkg(fpath,pkg):
    pktdump = PcapWriter(fpath, append=True, sync=True)
    pktdump.write(pkg)


def ShowPayload(pkg):
    if HTTP.HTTPRequest in pkg:
        print 'HTTPRequest'
    if HTTP.HTTPResponse in pkg:
        print 'HTTPResponse'
    print pkg.payload
    
def ShowRawData(pkg):
    if pkg.haslayer(TCP) and (pkt.getlayer(TCP).dport == 80 or pkt.getlayer(TCP).dport == 443) and pkg.haslayer(Raw):
        print pkg.getlayer(Raw).load

def SetRawData(pkg):
    hexdump(Ether()/"1234567891".decode("hex"))

def SendPkg(pkg):
    sendp(pkg)
    #p=srloop(IP(dst="www.baidu.com",ttl=1)/ICMP(),inter=3,count=2)



def ShowPkgInfo(pkg):
    print hexdump(pkg)
    print str(pkg)
    print pkg.summary()
    print pkg.show()
    print pkg.display()
    print pkg.load   # http 
    print pkg.payload
    pkg.sprintf('%load%')
    
    #result=sr1(IP(dst=domain)/TCP(dport=port,flags="S"),timeout=10)
    #pkg[TCP].flags
    
#a=IP()/TCP()/"GET / HTTP/1.0\r\n"



def synscan(domain,port):
    result=sr1(IP(dst=domain)/TCP(dport=port,flags="S"),timeout=10)
    if result:
        print 'got answer'
        if (result[TCP].flags==18):
            print 'port open'
    else:
        print 'not got answer'


def traceroute(): 
    ans,unans=sr(IP(dst="www.baidu.com",ttl=(2,25),id=RandShort())/TCP(flags=0x2),timeout=50)  
    for snd,rcv in ans:  
        print snd.ttl,rcv.src,isinstance(rcv.payload,TCP)
        

    
'''
import pcap
pc=pcap.pcap(face)
pc.setfilter('tcp port 80')
'''

if __name__ == '__main__':
    #pcap = sniff(offline = "xx/xx.pcap")
    #synscan('www.jinglingshu.org',80)
    synscan('www.baidu.com',80)

>>>>>>> fa76b6b8c0c4837ccf695fb0c78faad35b770297
