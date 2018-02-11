#!/mnt/sda1/opkg/usr/bin/python
# #encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import httplib
import fhelper
#import xmlhelper
import urlparse
import urllib
import fakerhelper
import pprint

class HttpHelper(object):
    def __init__(self):
        headers = {}
        headers['Accept']='*/*'
        headers['Connection']='Keep-Alive'
        headers['Accept-Encoding']='gzip, deflate, sdch'
        headers['Accept-Language']='zh-CN,zh;q=0.8'
        headers['Cache-Control']='no-cache'
        headers['Connection']='keep-alive'
        #headers['Cookie']='Hm_lvt_f8bdd88d72441a9ad0f8c82db3113a84=1449819861; Hm_lpvt_f8bdd88d72441a9ad0f8c82db3113a84=1449819967'
        headers['User-Agent']=fakerhelper.GetFakerUserAgent()

        self.headers= headers
        self.headers['Content-Type']="text/html; charset=utf-8"
        self.xmlheaders=headers
        self.xmlheaders['Content-Type']="text/xml;charset=UTF-8"
        self.soapxmlheaders=headers
        self.soapxmlheaders['Content-Type']="application/soap+xml;charset=UTF-8"
        self.hs = {'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch' , 'Accept': '*/*'
            , 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
            , 'Connection': 'keep-alive', 'Cache-Control': 'no-cache', 'Content-Type': 'text/xml;charset=UTF-8'}
    
    # send get request
    def GetResponse(self,host):
        conn=httplib.HTTPConnection(host,url)
        #header错误会导致得到的数据乱码
        conn.request('GET',url,'',self.headers)
        res=conn.getresponse()
        if res.status == 200:
            data=res.read()
        else:
            data="%d %s %s" % (res.status,res.reason,str(res.msg))
        conn.close()
        return data
    
    # send post request    
    def PostResponse(self,host,parasdict,url):
        params = urllib.urlencode(parasdict)
        conn=httplib.HTTPConnection(host)
        #header错误会导致得到的数据乱码
        conn.request('POST',url,params,self.headers)
        res=conn.getresponse()
        if res.status == 200:
            data=res.read()
        else:
            data="%d %s %s" % (res.status,res.reason,str(res.msg))
        conn.close()
        return data
    
    # send soap request
    def WebServiceResponse(self,url,soapaction,xml):
        host = self.GetHost(url)
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", url)
        webservice.putheader("Host", host)
        webservice.putheader("Accept", "*/*")
        webservice.putheader("SOAPAction", soapaction)
        webservice.putheader("User-Agent",fakerhelper.GetFakerUserAgent())
        webservice.putheader("Content-type", "text/xml;charset=UTF-8")#"application/soap+xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(xml))
        webservice.endheaders()
        pprint.pprint([host,url,soapaction,xml])
        webservice.send(xml)
        statuscode, statusmessage, header = webservice.getreply()
        if statuscode == 200:
            data=webservice.getfile().read()
        else:
            #data="%d %s %s" % (statuscode,statusmessage,str(header))
            import requests
            response=requests.post(url,data=xml,headers=self.xmlheaders)
            if response.status_code==200:
                data = response.text
            else:
                data = "%d %s" %  response.status_code,response.reason
        pprint.pprint(data)
        webservice.close()
        return data

    # send soap request
    def PostXMLRequest(self,url,xml):
        import requests
        response=requests.post(url,data=xml,headers=self.hs)
        if response.status_code==200:
            data = response.text
        else:
            data = "%d %s" %  (response.status_code,response.reason)
        pprint.pprint(data)
        return data

    def CallWebService(self,url,soapaction,ixml,oxml):
        fh=fhelper.FHelper(ixml)
        xml = fh.GetFileContent()
        result=self.WebServiceResponse(url,soapaction,xml)
        print oxml
        with open(oxml, 'w') as f:
            f.write(result)

    def GetHostPort(self,url):
        proto,rest=urllib.splittype(url)
        host,rest=urllib.splithost(rest)
        host,port=urllib.splitport(host)
        if port is None:
           port = 80
        return host ,port

    def GetHost(self,url):
        proto,rest=urllib.splittype(url)
        host,rest=urllib.splithost(rest)
        return host


if __name__ == '__main__':
    http=HttpHelper()
    #x=xmlhelper.XmlHelper()
    action = 'getDomesticCity'
    reqpath = r"/mnt/sda1/projects/openwrtpytest/xml/getDomesticCityReq.xml"
    ns = r'http://WebXml.com.cn/'
    #host='61.147.124.120'
    host='ws.webxml.com.cn'
    url='http://ws.webxml.com.cn/webservices/DomesticAirline.asmx'
    #replace xml item value
    #valuedicts = conf.StrToDictList(req["valuedicts"])
    #x.SetTagValues(reqpath,valuedicts)
    soapaction= urlparse.urljoin(ns,action)
    outfpath=r'/mnt/sda1/projects/openwrtpytest/xml/getDomesticCityRes.xml'
    http.CallWebService(url,soapaction,reqpath,outfpath)



