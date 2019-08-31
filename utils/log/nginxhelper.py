#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import arrow
from utils import setting
from utils.db import sqlhelper
import time
import re
import urllib
import traceback
import chardet
import pprint
import pymysql
import os
import shutil

smbserver = setting.YAMLDATA.get('smbserver')
#sqlserverdb = setting.YAMLDATA.get('sqlserverdb')
#server,user,pwd,logdb,dsn=sqlserverdb.get('server'),sqlserverdb.get('user'),sqlserverdb.get('pwd'),sqlserverdb.get('logdb'),sqlserverdb.get('dsn')
#sh=sqlhelper.SqlHelper(dsn,user,pwd,logdb,'dsn')
mysqldb = setting.YAMLDATA.get('mysqldb')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('logdb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')
# search one : searched = re.search(http_search_re, body, re.IGNORECASE)
userfields = ['name','log','login', 'wpname', 'ahd_username', 'unickname', 'nickname', 'user', 'user_name',
              'alias', 'pseudo', 'email', 'username', '_username', 'userid', 'form_loginname', 'loginname',
              'login_id', 'loginid', 'session_key', 'sessionkey', 'pop_login', 'uid', 'id', 'user_id', 'screename',
              'uname', 'ulogin', 'acctname', 'account', 'member', 'mailaddress', 'membername', 'login_username',
              'login_email', 'loginusername', 'loginemail', 'uin', 'sign-in', 'usuario']
passfields = ['ahd_password', 'pass', 'password', '_password', 'passwd', 'session_password', 'sessionpassword',
              'login_password', 'loginpassword', 'form_pw', 'pw', 'userpassword', 'pwd', 'upassword', 'login_password'
              'passwort', 'passwrd', 'wppassword', 'upasswd','senha','contrasena']
searchfields = ['dsp','wd','bs','plate_url','url_key','source','target','title','ti','ltu','query','tt','sn','en',
                'client_type','fname','un','bq','qry','pq','wifi_ssid','wifi_ip_address','channel','app_name',
                'version_name','device_platform','carrier','mcc_mnc','access','device','device_id','device_name',
                'answer','con','pf','ac','an','geo'
                'data','type','pageurl','USER_ID','P_INFO']
httpre = '((search|query|&q|\?q|search\?p|searchterm|keywords|keyword|command|terms|keys|question|kwd|searchPhrase|Carrier|device_id|%s|%s|%s)=([^&][^&]*))' % ('|'.join(userfields),'|'.join(passfields),'|'.join(searchfields))
httprec=re.compile(httpre, re.IGNORECASE)
typere='.+\.(css|img|js|jpg|png|swf|bmp|gif|mp4|zip|jpeg|deb|rar|ipk|pdf|avi|mp3|txt|exe|doc|docx|xls|xlsx|xml|dll|html|ppt)$'
typerec=re.compile(typere,re.IGNORECASE)
MaxKWordLen = 5000
KWordFile = r"d:\temp\kword.txt"

def keyword(url):
    searched = httprec.findall(url)
    msgs=[]
    if searched <> None:
        for search in searched:
            try:
                msgs.append(search[0])
            except Exception,e:
                pass
        msgstr = '\n'.join(msgs)
        return msgstr
    else:
        return ''

def urltype(url):
    searched=typerec.findall(url)
    if len(searched)>0:
        return searched[0]
    else:
        return ''

def encode(url):
    try:
        if type(url) is unicode:
            newurl=urllib.unquote(url.encode('utf-8'))
        else:
            newurl=urllib.unquote(url).encode('utf-8')
        return newurl
    except Exception,e:
        print 'error:',url,e.message,traceback.format_exc()

def request_info(selsql,updsql):
    results=sh.ExecQuery(selsql)
    url,urldecode,urlkword,utype,bodyword,cookiekword="","","","","",""
    for result in results:
        try:
            id,url,body,cookie=result[0],result[1],result[2],result[3]
            urldecode = encode(url)
            urlkword = keyword(urldecode)#.encode('utf-8')
            utype = urltype(url)
            bodydecode = encode(body)#.encode('utf-8')
            bodyword = keyword(bodydecode)
            cookiedecode = encode(cookie)
            cookiekword = keyword(cookiedecode)#.encode('utf-8')
            #try:
            sql = updsql % (pymysql.escape_string(urldecode),pymysql.escape_string(urlkword[0:MaxKWordLen]),pymysql.escape_string(utype),pymysql.escape_string(bodydecode),pymysql.escape_string(bodyword[0:MaxKWordLen]),pymysql.escape_string(cookiedecode),pymysql.escape_string(cookiekword[0:MaxKWordLen]),id)
            #except:
                #urlkword = ''
                #sql = updsql % (pymysql.escape_string(urldecode),pymysql.escape_string(urlkword[0:MaxKWordLen]),pymysql.escape_string(utype),pymysql.escape_string(bodydecode),pymysql.escape_string(bodyword[0:MaxKWordLen]),pymysql.escape_string(cookiedecode),pymysql.escape_string(cookiekword[0:MaxKWordLen]),id)
                #pprint.pprint(newurl)
            sh.ExecNonQuery(sql)
        except Exception,e:
            print 'error:',result[1],e.message,traceback.format_exc()

def nginx_info():
    strsql = "select id,url,body,cookie from url where decode is null"
    updsql = "update url set decode='%s',urlkword='%s',type='%s',bodydecode='%s',bodykword='%s',cookiedecode='%s',cookiekword='%s' where id=%d"
    request_info(strsql,updsql)

def nginx_log():
    # move nginx.log to bk/nginxYYYYMMDDHHmmss.log
    # mv /mnt/sda1/temp/nginx.log /mnt/sda1/temp/bk/nginx20180120221100.log
    # restart nginx
    # /mnt/sda1/opkg/etc/init.d/nginx restart
    # write nginx.log to sql server
    # logparser -i:CSV -iHeaderFile:"D:\TEMP\nginx.header" -headerRow:OFF -o:SQL  "SELECT * into Nginx from D:\TEMP\nginx20180120221100.log" -server:localhost\SQLEXPRESS -database:log -driver:"SQL Server" -username:sa -password:P@ssw0rd -createTable:OFF
    from utils import cmdhelper
    host,user,pwd,smbdir,srcf,dstf = smbserver.get('host'),smbserver.get('user'),smbserver.get('pwd'),smbserver.get('smbdir'),smbserver.get('srcf'),smbserver.get('dstf')
    dt = arrow.now().format('YYYYMMDDHHmmss')
    logfile = "/temp/bk/nginx%s.log" % dt
    cmdhelper.SSHExecCmd(host,user,pwd,["mv %s /mnt/sda1%s" % (srcf,logfile) ,"/mnt/sda1/opkg/etc/init.d/nginx restart"])
    cmdhelper.GetFile(host,user,pwd,smbdir,logfile,dstf % dt)
    '''
    to sql server
    server,user,pwd,logdb=sqlserverdb.get('server'),sqlserverdb.get('user'),sqlserverdb.get('pwd'),sqlserverdb.get('logdb')
    cmdstr=r'logparser -i:CSV -iHeaderFile:"D:\TEMP\nginx.header" -headerRow:OFF -o:SQL  "SELECT * into Nginx from %s" -server:%s -database:%s -driver:"SQL Server" -username:%s -password:%s -createTable:OFF'\
           % (dstf % dt,server,logdb,user,pwd)
    time.sleep(60)
    cmdhelper.ExecCmd("cd C:\Program Files (x86)\Log Parser 2.2")
    print cmdhelper.ExecCmd(cmdstr)
    '''
    nginx_db(dt)

def logfoldere_db(logdir):
    files=os.listdir(logdir)
    for f in files:
        ifile = os.path.join(logdir,f)
        if os.path.isfile(ifile) and 'nginx' in f:
            logfile_db(ifile)
            ofile = os.path.join(logdir,'bk',f)
            shutil.copyfile(ifile,ofile)
            os.remove(ifile)

def logfile_db(ifile):
    sql = r"LOAD DATA LOCAL INFILE  '%s' INTO TABLE nginx FIELDS  terminated by ',' enclosed by '\"' LINES TERMINATED BY '\n' (remote_addr,time_local,host,request,status,body_bytes_sent,http_referer,http_user_agent,request_body,http_cookie,remote_user,http_x_forwarded_for)" % ifile
    sh.ExecNonQuery(sql)

def nginx_db(logdir):
    logfoldere_db(logdir)
    sql = 'call nginx_url'
    sh.ExecNonQuery(sql)

def out_kword():
    sql ='''select distinct kword from( select  distinct urlkword as kword from url union select  distinct bodykword from url
    union select  distinct cookiekword from url) as t where length(kword)>0 order by kword'''
    results=sh.ExecQuery(sql)
    lines = []
    for result in results:
        reslist = result[0].split('\n')
        #reslist = map(str.strip, reslist)
        lines.extend(reslist)
    nlines = list(set(lines))
    nlines.sort()
    print len(results),'=>',len(lines),'=>',len(nlines)
    with open(KWordFile,'w') as f:
        sys.stdout = f
        for line in nlines:
            #pprint.pprint( line)
            f.write(str(line)+'\n')

if __name__ == '__main__':
    if len(sys.argv)>0 and sys.argv[1]=="nginx_db":
        nginx_db('/mnt/sda1/opt/var/log/nginx')
    elif len(sys.argv)>0 and sys.argv[1]=="nginx_info":
        nginx_info()
    else:
        pass
        #out_kword()
