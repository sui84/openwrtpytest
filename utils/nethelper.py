
#!/usr/bin/env python2

from os import geteuid, devnull
import logging
# shut up scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import scapy_http.http as HTTP
conf.verb=0
from sys import exit
import binascii
import struct
import argparse
import signal
import base64
from urllib import unquote
from subprocess import Popen, PIPE
from collections import OrderedDict
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from urllib import unquote
import time
import scapyhelper
import os
from scapy.all import TCP,IP,IPv6,Dot11Beacon,SNMP,ARP,DHCP,ICMP,Raw,X509_Cert,X509_AccessDescription,TFTP,SMBNetlogon_Protocol_Response_Header,SCTP,PPPoE,PPP,NetBIOS_DS,MobileIP,ICMP,DNS,RadioTap,Dot11,LLC
from db import mghelper
import yaml
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import arrow
#import binascii    #already imported on line 10
# Debug
#from IPython import embed

##########################
# Potention ToDo:
# MySQL seed:hash
# VNC
# Oracle?
# Add file carving from dissectors.py
#########################

# Unintentional code contributors:
#     Laurent Gaffie
#     psychomario

iface=conf.iface
fmt='%Y/%m/%d %H:%M:%S'
logfile='/mnt/sda1/temp/credentials.txt'
cappath = '/mnt/sda1/cap/'
udpfile = '/mnt/sda1/cap/protocol/udp.cap'
tcpfile = '/mnt/sda1/cap/protocol/tcp.cap'
etherfile = '/mnt/sda1/cap/protocol/ether.cap'
imagefile = '/mnt/sda1/cap/protocol/image.cap'
otherfile = '/mnt/sda1/cap/protocol/other.cap'
mail= {"ports":[25,110],"file":'protocol/mail.cap'}
terminal= {"ports":[22,23,3389],"file":'protocol/terminal.cap'}
http= {"ports":[80,443,8080,3128,8081,9080],"file":'protocol/http.cap'}
tftp= {"ports":[69],"file":'protocol/tftp.cap'}
oracle= {"ports":[1521,1158,2100],"file":'protocol/oracle.cap'}
mssql= {"ports":[1433,1434],"file":'protocol/mssql.cap'}
qq= {"ports":[1080],"file":'protocol/qq.cap'}
snmp= {"ports":[161,162],"file":'protocol/snmp.cap'}
netbios= {"ports":[137,139],"file":'protocol/netbios.cap'}
as400= {"ports":[449,8470,9470,8471,9471,8472,9472,8473,9473,8474,9474,8475,9475,8476,9476,992,2001,2010,5010,397,942,512],"file":'protocol/as400.cap'}
protocols = [mail,terminal,http,tftp,oracle,mssql,qq,snmp,netbios,as400]
layers = [Raw,Dot11Beacon,SNMP,ARP,DHCP,ICMP,X509_Cert,X509_AccessDescription,TFTP,SMBNetlogon_Protocol_Response_Header,SCTP,PPPoE,PPP,NetBIOS_DS,MobileIP,ICMP,DNS,RadioTap,Dot11,LLC]
images = ['jpg', 'jpeg', 'gif', 'png','bmp']



logging.basicConfig(filename=logfile,level=logging.INFO)
DN = open(devnull, 'w')
pkt_frag_loads = OrderedDict()
challenge_acks = OrderedDict()
mail_auths = OrderedDict()
telnet_stream = OrderedDict()


# Prone to false+ but prefer that to false-
http_search_re = '((search|query|&q|\?q|search\?p|searchterm|keywords|keyword|command|terms|keys|question|kwd|searchPhrase)=([^&][^&]*))'
YAMLF = '../conf/test.yaml'
with open(YAMLF) as f:
    YAMLDATA=yaml.load(f)
mh=mghelper.MgHelper(server=YAMLDATA.get('mongoserver'),port=YAMLDATA.get('mongoport'),dbname=YAMLDATA.get('mongodb'))


def SaveHttpFromFile(pkgpath):
    pkgs = PcapReader(pkgpath)
    SaveHttpFromPkgs(pkgs)
            
def SaveHttpFromPkgs(pkgs):
    i=0
    for pkt in pkgs:  
        if pkt.haslayer(Raw):
            pkgtime = str(arrow.get(pkt.time))
            load = pkt[Raw].load
            print i,load
            handle_http_payload(pkgtime,load)
        i+=1

def pkgs_split(pkgs,pkgtype):
    ports,file = pkgtype.get('ports'),pkgtype.get('file')
    file = os.path.join(cappath,file)
    newpkgs=coll.where(lambda x:x[IP].sport in ports or x[IP].dport in ports).to_list()
    scapyhelper.AppendPkg(file,newpkgs)

def pkg_split(pkt):
    if pkt.haslayer(Ether) and pkt.haslayer(Raw) and not pkt.haslayer(IP) and not pkt.haslayer(IPv6):
        scapyhelper.AppendPkg(etherfile,pkt)

    if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
        scapyhelper.AppendPkg(udpfile,pkt)    
    elif pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):    
        scapyhelper.AppendPkg(tcpfile,pkt)
        
    if  pkt.haslayer(TCP):
        for pro in protocols:
            ports,file = pro.get('ports'),pro.get('file')
            file = os.path.join(cappath,file)
            if pkt[TCP].sport in ports or pkt[TCP].dport in ports:
                scapyhelper.AppendPkg(file,pkt)

    
    haslayer = False;    
    for layer in layers:
        if pkt.haslayer(layer):
            haslayer = True
            file = os.path.join(cappath,'protocol',layer.__name__+'.cap')
            scapyhelper.AppendPkg(file,pkt)
            if layer == 'DNS':
                for i in range(0,pkt[DNS].ancount):
                    dnsdict = {'host':pkt[DNS].an[i].rrname,'url':pkt[DNS].an[i].rdata}
                    save_dns(pkgtime,dnsdict)
                for i in range(0,pkt[DNS].arcount):
                    dnsdict = {'host':pkt[DNS].ar[i].rrname,'url':pkt[DNS].ar[i].rdata}
                    save_dns(pkgtime,dnsdict)
    
    if haslayer == False:
        scapyhelper.AppendPkg(otherfile,pkt)

def save_dns(pkgtime,dnsdict):
    if mg.GetDictObjsCnt('dnsinfo',dnsdict)==0:
        dnsdict['pkgtime']=pkgtime
        mh.SaveDictObj(dnsdict,'dnsinfo')
            
def pkt_parser(pkt):
    '''
    Start parsing packets here
    '''
    try:
        pkgtime = str(arrow.get(pkt.time))
        pkg_split(pkgtime,pkt)

        if pkt.haslayer(Raw):
            load = pkt[Raw].load

            handle_http_payload(pkgtime,load)
    except Exception,e:
        pkt.show()
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

def get_http_searches(http_url_req, body, host):
    '''
    Find search terms from URLs. Prone to false positives but rather err on that side than false negatives
    search, query, ?s, &q, ?q, search?p, searchTerm, keywords, command
    '''
    false_pos = ['i.stack.imgur.com']

    searched = None
    if http_url_req != None:
        searched = re.search(http_search_re, http_url_req, re.IGNORECASE)
        if searched == None:
            searched = re.search(http_search_re, body, re.IGNORECASE)

    if searched != None and host not in false_pos:
        searched = searched.group(3)
        # Eliminate some false+
        try:
            # if it doesn't decode to utf8 it's probably not user input
            searched = searched.decode('utf8')
        except UnicodeDecodeError:
            return
        # some add sites trigger this function with single digits
        if searched in [str(num) for num in range(0,10)]:
            return
        # nobody's making >100 character searches
        if len(searched) > 100:
            return
        msg = 'Searched %s: %s' % (host, unquote(searched.encode('utf8')).replace('+', ' '))
        return msg




def Decode_Ip_Packet(s):
    '''
    Taken from PCredz, solely to get Kerb parsing
    working until I have time to analyze Kerb pkts
    and figure out a simpler way
    Maybe use kerberos python lib
    '''
    d={}
    d['header_len']=ord(s[0]) & 0x0f
    d['data']=s[4*d['header_len']:]
    return d

def handle_http_payload(pkgtime,load):
    httptype = guess_payload_class(load)
    if httptype=='HTTPRequest' or httptype=='HTTPResponse':
        firstline,headers,body = parse_headers_and_body(load)
        host = headers.get('host','')
        referer = headers.get('referer','')
        cookie = headers.get('cookie','')
        contenttype = headers.get('content-type','')
        searched = ''
        status = ''
        user_msg = ''
        pass_msg = ''
        url=''
        body=''
        ftype = contenttype.split('/',1)
        if len(ftype)>1 and ftype[0].lower()=="image":
            imagesuffix = ftype[1]
            scapyhelper.AppendPkg(imagefile,pkt)
    
        s=firstline.split(' ',2)
        if httptype == 'HTTPRequest':
            url=s[1]    
            # Print search terms
            searched = get_http_searches(url, body, host)
            
        elif httptype == 'HTTPResponse':
            status = s[1]
            
        if body != '':
            user_msg,pass_msg = get_login_pass(body)

        
        httpdict = {'pkgtime':pkgtime,'host':host,'url':url,'referer':referer,'cookie':cookie,'type':contenttype,'searched':searched,'body':body
        ,'status':status,'load':load,'user_msg':user_msg,'pass_msg':pass_msg}
        mh.SaveDictObj(httpdict,'httpinfo')
        
def guess_payload_class(payload):
    ''' Decides if the payload is an HTTP Request or Response, or
        something else '''
    try:
        prog = re.compile(
            r"^(?:OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT) "
            r"(?:.+?) "
            r"HTTP/\d\.\d$"
        )
        if "\r\n".encode() in payload:
            crlfIndex = payload.index("\r\n".encode())
            req = payload[:crlfIndex].decode("utf-8")
            result = prog.match(req)
            if result:
                return 'HTTPRequest'
            else:
                prog = re.compile(r"^HTTP/\d\.\d \d\d\d .*$")
                result = prog.match(req)
                if result:
                    return 'HTTPResponse'
        return ''
    except Exception,e:
        pass
        #print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

def parse_headers_and_body(s):
    ''' Takes a HTTP packet, and returns a tuple containing:
      - the first line (e.g., "GET ...")
      - the headers in a dictionary
      - the body '''
    first_line = ''
    headers = ''
    body = ''
    try:
        crlfcrlf = b"\x0d\x0a\x0d\x0a"
        crlfcrlfIndex = s.find(crlfcrlf)
        headers = s[:crlfcrlfIndex + len(crlfcrlf)].decode("utf-8")
        body = s[crlfcrlfIndex + len(crlfcrlf):]
        if "\r\n" in headers:
            first_line, headers = headers.split("\r\n", 1)
    except Exception,e:
        print s
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
        headers = s
        body = ''
    return first_line.strip(), parse_headers(headers), body

def parse_headers(s):
    # split header string to dict
    headers = s.split("\r\n")
    headers_found = {}
    for header_line in headers:
        try:
            if ':' in header_line:
                key, value = header_line.split(':', 1)
                headers_found[key.strip().lower()]=value.strip()
        except Exception,e:
            print s
            print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
            continue     
    return headers_found

def get_login_pass(body):
    '''
    Regex out logins and passwords from a string
    '''
    user = ''
    passwd = ''

    # Taken mainly from Pcredz by Laurent Gaffie
    userfields = ['log','login', 'wpname', 'ahd_username', 'unickname', 'nickname', 'user', 'user_name',
                  'alias', 'pseudo', 'email', 'username', '_username', 'userid', 'form_loginname', 'loginname',
                  'login_id', 'loginid', 'session_key', 'sessionkey', 'pop_login', 'uid', 'id', 'user_id', 'screename',
                  'uname', 'ulogin', 'acctname', 'account', 'member', 'mailaddress', 'membername', 'login_username',
                  'login_email', 'loginusername', 'loginemail', 'uin', 'sign-in', 'usuario']
    passfields = ['ahd_password', 'pass', 'password', '_password', 'passwd', 'session_password', 'sessionpassword', 
                  'login_password', 'loginpassword', 'form_pw', 'pw', 'userpassword', 'pwd', 'upassword', 'login_password'
                  'passwort', 'passwrd', 'wppassword', 'upasswd','senha','contrasena']

    for login in userfields:
        login_re = re.search('(%s=[^&]+)' % login, body, re.IGNORECASE)
        if login_re:
            user = login_re.group()
    for passfield in passfields:
        pass_re = re.search('(%s=[^&]+)' % passfield, body, re.IGNORECASE)
        if pass_re:
            passwd = pass_re.group()

    return user, passwd
    
def printer(src_ip_port, dst_ip_port, msg):
   print_str = '[%s][%s > %s] %s%s%s' % (time.strftime(fmt),src_ip_port, dst_ip_port, T, msg, W)


if __name__ == "__main__":
   #sniff(iface=conf.iface, prn=pkt_parser, store=0)
   sniff( prn=pkt_parser, store=0)