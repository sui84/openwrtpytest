#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import fhelper
import commonhelper
import xmlhelper
import time
import pprint
import urllib
try:
    import requests
except Exception,e:
    import requests
import fakerhelper


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
        headers['User-Agent']=fakerhelper.GetFakerData("useragent")

        self.headers= headers
        self.headers['Content-Type']="text/html; charset=utf-8"
        self.xmlheaders=headers
        self.xmlheaders['Content-Type']="text/xml;charset=UTF-8"
        self.soapxmlheaders=headers
        self.soapxmlheaders['Content-Type']="application/soap+xml;charset=UTF-8"

    # send get request
    def GetResponse(self,host):
        conn=httplib.HTTPConnection(host,url)
        #header error cause data wrong
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
        webservice.putheader("SOAPAction", soapaction)
        webservice.putheader("User-Agent", "Python Post")
        webservice.putheader("Content-type", "application/soap+xml")
        webservice.putheader("Content-length", "%d" % len(xml))
        webservice.endheaders()
        print host,url,soapaction,xml
        webservice.send(xml)
        statuscode, statusmessage, header = webservice.getreply()
        if statuscode == 200:
            data=webservice.getfile().read()
        else:
            data="%d %s %s" % (statuscode,statusmessage,str(header))   
        print data
        webservice.close()
        return data

    # send soap request
    def PostXMLRequest(self,url,xml,proxies={}):
        print url,xml
        response=requests.post(url,data=xml,headers=self.soapxmlheaders,proxies=proxies)
        if response.status_code==200:
            data = response.text
        else:
            data =  str(response.status_code) + response.reason
        pprint.pprint(data)
        return data

    def CallWebService(self,host,url,soapaction,ixml,oxml):
        fh=fhelper.FHelper(ixml)
        xml = fh.GetFileContent()
        result=http.WebServiceResponse(host,url,soapaction,xml)
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

    def DownloadFile(self,url,ofile):
        data = self.GetResponse(url)
        fh=fhelper.FHelper(ofile)
        fh.SaveBytesToFile(data)
    
    def GetDataWithProxy(self,url,user,pwd,proxy,data=None):
        #proxy
        proxystr = 'http://%s:%s@%s' % (user,pwd,proxy)
        proxy = urllib2.ProxyHandler({'http':proxystr})
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(proxy,auth,urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        if data != None:
            #post
            datastr = urllib.urlencode(data)
            nurl = "%s?%s" % (url,datastr)
            req = urllib2.Request(nurl,headers=self.headers,data=datastr)
        else:
            #get
            req = urllib2.Request(url,headers=self.headers)
        html = urllib2.urlopen(req)
        return html.geturl(),html.read()

if __name__ == '__main__':
    http=HttpHelper()
    x=xmlhelper.XmlHelper()
    action = 'getDomesticCity'
    reqpath = r"d:\temp\req.xml"
    ns = r'http://WebXml.com.cn/'
    host='61.147.124.120'
    url='http://ws.webxml.com.cn/webservices/DomesticAirline.asmx'
    #replace xml item value
    #valuedicts = conf.StrToDictList(req["valuedicts"])
    #x.SetTagValues(reqpath,valuedicts)
    soapaction=commonhelper.GetFullUrl(ns,action)
    outfpath=r'd:\temp\response.xml'
    http.CallWebService(host,url,soapaction,reqpath,outfpath)
    #output to PDF file
    '''
    #result=http.GetResponse(host)
    conf=confhelper.ConfHelper()
    confs = conf.GetSectionConfig("soaphttp")
    host=confs["soaphost"]
    url=confs["soapurl"]
    reqs = conf.GetListobjConfig("soaphttp","reqxml")
    ns = confs["namespace"]
    #output xml file
    outxmldir=confs["outxmldir"]
    for req in reqs:
        action = req["action"]
        reqpath = req["reqpath"]
        #replace xml item value
        valuedicts = conf.StrToDictList(req["valuedicts"])
        x.SetTagValues(reqpath,valuedicts)
        soapaction=commonhelper.GetFullUrl(ns,action)
        outfpath=commonhelper.GetDstPath(outxmldir,reqpath)
        http.CallWebService(host,url,soapaction,reqpath,outfpath)
        #output to PDF file
        if req.has_key("filetag"):
            tagname = req["filetag"]
            bytestr = x.GetTagValue(outfpath,tagname)
            fname = action + time.strftime("%y%m%d%H%M%S") +'.PDF'
            ofpath = commonhelper.GetDstPath(outxmldir,fname)
            f = fhelper.FHelper(ofpath)
            f.SaveByteStrToFile(bytestr)
    '''


