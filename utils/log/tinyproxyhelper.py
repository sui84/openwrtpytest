import requests
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from utils.db import sqlhelper
from utils import setting
import time
import requests
import pymysql
import urllib
import traceback
import pprint

proxies={"http":"http://118.193.107.80:80"}
#proxies={"http":"http://118.193.107.115:80"}
mysqldb = setting.YAMLDATA.get('mysqldb')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('logdb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')


def urlencode():
    results=sh.ExecQuery("SELECT id,url from tinyproxy where urlencode is null and length(url)>0")
    for result in results:
        try:
            url=result[1]
            if type(url) is unicode:
                newurl=urllib.unquote(url.encode('utf-8'))
            else:
                newurl=urllib.unquote(url).encode('utf-8')
            #print newurl
            if newurl<>result[1]:
                #pprint.pprint(newurl)
                sh.ExecNonQuery("update tinyproxy set urlencode='%s' where id=%d" % (pymysql.escape_string(newurl),result[0]))
        except Exception,e:
            print 'error:',result[1],e.message,traceback.format_exc()

'''
 req.headers.get('Content-Type')  'application/json'
jobj=json.loads(req.content.decode())
jobj.viewkeys()
jobj["data"]["title"]
'''

if __name__ == '__main__':
    #get_ipdomain()
    urlencode()
