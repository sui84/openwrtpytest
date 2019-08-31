#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import arrow
from utils import cmdhelper,setting
from utils.db import sqlhelper
import requests
from pyquery import PyQuery as pq
import pymysql
import traceback

mysqldb = setting.YAMLDATA.get('mysqldb')
host,user,pwd,db=mysqldb.get('host'),mysqldb.get('user'),mysqldb.get('pwd'),mysqldb.get('logdb')
sh=sqlhelper.SqlHelper(host,user,pwd,db,'mysql')

def root_domain(domain):
    try:
        url="http://whois.chinaz.com/"+domain
        req=requests.get(url)
        d=pq(req.text)
        rootdomain = d('#DomainName').val()
        domaininfo= d('#sh_info').text()
        url2='http://whois.chinaz.com/getTitleInfo.ashx'
        req=requests.post(url2,data={"host":rootdomain,"isupdate":''})
        d=pq(req.text)
        titleinfo = d.text()
    except Exception:
        rootdomain,domaininfo,titleinfo="","",""
    return rootdomain,domaininfo,titleinfo

def ip_info(ip):
    try:
        url="http://site.ip138.com/"+ip+'/'
        d=pq(url)
        info = d('.result2').text()
        domain = d('.result2 li:eq(1) a').text()
        if domain==u'\u6682\u65e0\u7ed3\u679c':
            domain = ""
    except Exception:
        info,domain="",""
    return info,domain

def domain_info(domain):
    try:
        info = ''
        url='http://site.ip138.com/%s/'% domain
        #req=requests.get(url,proxies)
        req=requests.get(url)
        d=pq(req.text)
        #d=pq(url)
        ip = d('.panels p:eq(0) a').text()
        if len(ip)>0:
            info,domain2 = ip_info(ip)
        ips = d('.panels').text()
        '''
        url='http://site.ip138.com/%s/domain.htm'% domain
        domains = d('.panels').text()
        url='http://site.ip138.com/%s/beian.htm'% domain
        beian = d('.panels').text()
        url='http://site.ip138.com/%s/whois.htm'% domain
        whois = d('.panels').text()
        info += '\n'+ips+'\n' + domains+'\n' + beian+'\n' + whois
        '''
        info += '\n'+ips
    except Exception:
        ip,info="",""
    return ip,info

def save_domain(selsql,updsql,updsql2,type):
    results=sh.ExecQuery(selsql)
    for result in results:
        try:
            id = result[0]
            if type=="ip_info":
                info,domain  = ip_info(result[1])
                if info==u'查询频率过高，请稍候查询':
                        break
                elif len(info)>0 or len(domain)>0:
                    sql = updsql % (domain,pymysql.escape_string(info),id)
                    sh.ExecNonQuery(sql)
            elif type=="domain_info":
                ip,info = domain_info(result[1])
                if len(ip)>0:
                    sql=updsql % (ip,id)
                    sh.ExecNonQuery(sql)
                if len(info)>0:
                    if info==u'查询频率过高，请稍候查询':
                        break
                    else:
                        sql=updsql2 % (info,id)
                        sh.ExecNonQuery(sql)
            elif type=="root_domain":
                rootdomain,domaininfo,titleinfo = root_domain(result[1])
                if len(rootdomain)>0:
                    sh.ExecNonQuery("update domain set rootdomain='%s' where id=%d" % (rootdomain,id))
                    if len(domaininfo)>0 or len(titleinfo)>0:
                        sh.ExecNonQuery("insert into rootdomain(rootdomain,domaininfo,titleinfo) select '%s','%s','%s' from dual  where not exists(select 1 from rootdomain where rootdomain='%s')" % (rootdomain,pymysql.escape_string(domaininfo[0:2000]),pymysql.escape_string(titleinfo[0:2000]),rootdomain))
        except Exception,e:
            print 'error:',result[1],e.message,traceback.format_exc()

def domain_db():
    # update domain table and ip field
    sql=' call add_domain'
    sh.ExecNonQuery(sql)

    # get ip info  concat(ifnull(info,''),'%s')
    selsql = "SELECT id,ip FROM domain WHERE length(ip)>0 and ipinfo is null"
    updsql = "update domain set domain='%s',ipinfo='%s'  where id=%d"
    save_domain(selsql,updsql,'',"ip_info")

    # get doamin info
    selsql = "SELECT id,domain from domain where length(domain)>0 and domaininfo is null"
    updsql="update domain set ip='%s' where ip is null and id=%d"
    updsql2="update domain set domaininfo='%s' where id=%d "
    save_domain(selsql,updsql,updsql2,"domain_info")

    # get root domain info
    selsql = "SELECT id,domain from domain where length(domain)>0 and rootdomain is null "
    updsql = "update domain set rootdomain='%s' where id=%d"
    updsql2="insert into rootdomain(rootdomain,domaininfo,titleinfo) select '%s','%s','%s' from dual  where not exists(select 1 from rootdomain where rootdomain='%s')"
    save_domain(selsql,updsql,updsql2,"root_domain")


if __name__ == '__main__':
    if len(sys.argv)>0 and sys.argv[1]=="domain":
        domain_db()
