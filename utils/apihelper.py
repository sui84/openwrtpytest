#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import HTMLParser
import requests
import geohelper
import ipinfohelper
import pprint
import pickledb
import yaml
from py_linq import Enumerable
from api import *
import xlshelper
import strhelper

class ApiHelper(object):
    def __init__(self):
        self.sh = strhelper.StrHelper()
        self.hp =HTMLParser.HTMLParser()
        self.gh = geohelper.GeoHelper()
        yamlf = r"../conf/test.yaml"
        with open(yamlf) as f:
            self.yamldata=yaml.load(f)
        self.weatherurl= self.yamldata.get('weatherurl')
        self.ipusls=self.yamldata.get('ipusls')
        self.excelpath = '../excel/test.xlsx'
        testfpath='../data/pickledb/test.db'
        self.testdb = pickledb.load(testfpath,True)


    def weather(self,city):
        (wdu,jdu) = self.gh.GetWJdu(city)
        result = u"纬度:%f\n经度:%f\n" %(wdu,jdu)
        url = self.weatherurl % city
        req = requests.get(url)
        datadict=self.hp.unescape(self.sh.Jsonstr2Obj(req.text))
        pprint.pprint(datadict)
        '''
        {u'city': u'\u73e0\u6d77',
 u'count': 39,
 u'data': {u'forecast': [{u'aqi': 38.0,
                          u'date': u'15\u65e5\u661f\u671f\u65e5',
                          u'fl': u'4-5\u7ea7',
                          u'fx': u'\u4e1c\u5317\u98ce',
                          u'high': u'\u9ad8\u6e29 26.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u5c3d\u91cf\u51cf\u5c11\u6237\u5916\u6d3b\u52a8\uff0c\u9632\u6b62\u610f\u5916\u53d1\u751f',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:01',
                          u'type': u'\u66b4\u96e8'},
                         {u'aqi': 27.0,
                          u'date': u'16\u65e5\u661f\u671f\u4e00',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 27.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u613f\u96e8\u540e\u6e05\u65b0\u7684\u7a7a\u6c14\u7ed9\u60a8\u5e26\u6765\u597d\u5fc3\u60c5\uff01',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:00',
                          u'type': u'\u9635\u96e8'},
                         {u'aqi': 31.0,
                          u'date': u'17\u65e5\u661f\u671f\u4e8c',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u4eca\u65e5\u591a\u4e91\uff0c\u9a91\u4e0a\u5355\u8f66\u53bb\u770b\u770b\u4e16\u754c\u5427',
                          u'sunrise': u'06:22',
                          u'sunset': u'18:00',
                          u'type': u'\u591a\u4e91'},
                         {u'aqi': 59.0,
                          u'date': u'18\u65e5\u661f\u671f\u4e09',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u60a0\u60a0\u7684\u4e91\u91cc\u6709\u6de1\u6de1\u7684\u8bd7',
                          u'sunrise': u'06:22',
                          u'sunset': u'17:59',
                          u'type': u'\u591a\u4e91'},
                         {u'aqi': 74.0,
                          u'date': u'19\u65e5\u661f\u671f\u56db',
                          u'fl': u'<3\u7ea7',
                          u'fx': u'\u65e0\u6301\u7eed\u98ce\u5411',
                          u'high': u'\u9ad8\u6e29 29.0\u2103',
                          u'low': u'\u4f4e\u6e29 24.0\u2103',
                          u'notice': u'\u7ef5\u7ef5\u7684\u4e91\u6735\uff0c\u5f62\u72b6\u5343\u53d8\u4e07\u5316',
                          u'sunrise': u'06:23',
                          u'sunset': u'17:58',
                          u'type': u'\u591a\u4e91'}],
           u'ganmao': u'\u5404\u7c7b\u4eba\u7fa4\u53ef\u81ea\u7531\u6d3b\u52a8',
           u'pm10': 33.0,
           u'pm25': 21.0,
           u'quality': u'\u4f18',
           u'shidu': u'71%',
           u'wendu': u'22',
           u'yesterday': {u'aqi': 45.0,
                          u'date': u'14\u65e5\u661f\u671f\u516d',
                          u'fl': u'3-4\u7ea7',
                          u'fx': u'\u4e1c\u5317\u98ce',
                          u'high': u'\u9ad8\u6e29 28.0\u2103',
                          u'low': u'\u4f4e\u6e29 23.0\u2103',
                          u'notice': u'\u4eca\u65e5\u591a\u4e91\uff0c\u9a91\u4e0a\u5355\u8f66\u53bb\u770b\u770b\u4e16\u754c\u5427',
                          u'sunrise': u'06:21',
                          u'sunset': u'18:02',
                          u'type': u'\u591a\u4e91'}},
 u'date': u'20171015',
 u'message': u'Success !',
 u'status': 200}
       '''
        if datadict["status"] == 200:
            data = datadict["data"]
            yesterday = data['yesterday']
            forecast = data['forecast']
            count = datadict["count"]
            citystr = datadict["city"]
            datestr = datadict["date"]
            shidu = data["shidu"]
            wendu = data["wendu"]
            pm25 = data.get("pm25")
            quality = data["quality"]
            sunrise = yesterday['sunrise']
            sunset = yesterday['sunset']
            result+= u"%s\t%s\n温度:%s\t湿度:%s\tPM25:%d %s\n%s\t%s" % (citystr,datestr,wendu,shidu,pm25,quality,sunrise,sunset)
            result+=u"%s %s %s %s\n %s~%s\n"  % (yesterday['date'],yesterday['type'],yesterday['fx'],yesterday['fl']
                                                  ,yesterday['low'],yesterday['high'])
            for i in range(0,len(forecast)-1):
                result+=u"%s %s %s %s\n %s~%s\n"  % (forecast[i]['date'],forecast[i]['type'],forecast[i]['fx'],forecast[i]['fl']
                                                   ,forecast[i]['low'],forecast[i]['high'])
        else:
            result = datadict["message"]
        return result

    def location(self,wjdu):
        data = self.gh.GetLocation(wjdu)
        result = "纬度:%s\n经度:%s\n%s" % (data.get('lat'),data.get('lon'),data.get('display_name'))
        state_district = data.get('address').get('state_district')
        city = state_district.split('/')[0].strip()
        pprint.pprint(city)
        cweather = self.weather(city)
        result += "\n" + cweather
        return result

    def ip(self,ip=""):
        result = ""
        if len(ip) == 0:
            for url in self.ipusls:
                req = requests.get(url)
                #u"{ip:'***',address:'...'}"
                # prompte error because not correct dict format ValueError: Expecting property name: line 1 column 1 (char 1)
                # the ast.literal_eval not work
                pprint.pprint(req.text)
                ip="ip"
                address="address"
                datadict=eval(req.text)
                #datadict=self.hp.unescape(self.sh.Jsonstr2Obj(req.text))
                result+="%s\n%s" %(datadict.get('ip'),datadict.get('address'))
        else:
            ih=ipinfohelper.IPInfo(self.yamldata.get('ipdat'))
            (address,yunying) = ih.getIPAddr(ip)
            result+="%s\n%s\t%s" % (ip,address,yunying)
        return result

    def airline(self,content):
        if content.startswith(u"航班号"):
            colls = airlinehelper.getaircoll("airlines")
            airlinecodes=colls.select (lambda x:x.get('AirlineCode')).distinct().to_list()
            info = u"珠海机场航班号：%s\n" %(', '.join(airlinecodes))
        elif content.startswith(u"航班"):
            if content == u"航班":
                dicts=testdb.get('airlines')
                if dicts == None:
                    dicts = xlshelper.XlsHelper(self.excelpath).GetSheetToDicts("airlines")
                colls=Enumerable(dicts)
                companys=colls.select (lambda x:x.get('Company')).distinct().to_list()
                modes=colls.select (lambda x:x.get('Mode')).distinct().to_list()
                arrivedromes = colls.select (lambda x:x.get('ArriveDrome')).distinct().to_list()
                '''
                startdromes = colls.select (lambda x:x.get('StartDrome')).distinct().to_list()
                info = u"航空公司：%s\n机型：%s\n到珠海的机场：%s\n从珠海可以到达的机场：%s\n航班号：%s\n" %(companys,modes,startdromes,arrivedromes,airlinecodes)
                '''
                info = u"航空公司：%s\n机型：%s\n从珠海可以到达的机场：%s\n" %(', '.join(companys),', '.join(modes),', '.join(arrivedromes))
            else:
                strs = self.sh.SplitString(content)
                if len(strs) < 3:
                    fcabbs = "ZUH"
                    dicts=testdb.get('citycodes')
                    colls=Enumerable(dicts)
                    tcabbs = airlinehelper.GetAbb(colls,strs[1])
                else:
                    fcabbs,tcabbs = airlinehelper.GetAbbs(strs[1],strs[2])
                results = webxmlhelper.GetResponse('airurl',"getDomesticAirlinesTime",fcabbs,tcabbs)
                print results
                info = ""
                if len(results) > 0:
                    for result in results:
                        info += u"%s\n%s\t%s\t%s\t%s\n%s到%s\n%s-%s\n\n" % (result.get('Company'),result.get('AirlineCode'),result.get('Week'),result.get('Mode') ,result.get('AirlineStop')
                        ,result.get('StartDrome'),result.get('ArriveDrome'),result.get('StartTime'),result.get('ArriveTime'))
                else:
                    info = u"没有航班"



        pprint.pprint(info)
        return info

    def train(self,content):
        strs = self.sh.SplitString(content)
        print strs
        info = ""
        if content.startswith(u"火车号"):
            results = webxmlhelper.GetResponse('trainurl',"getDetailInfoByTrainCode",xh.Convert2UTF8(strs[1]))
            if len(results) > 0 and results[0].get('StartTime')<>None:
                i = 1
                for result in results:
                    time = result.get('ArriveTime') if result.get('StartTime')==None else result.get('StartTime')
                    info += u"%d.%s[%s]\t%sKM\n" % (i,result.get('TrainStation'),time,result.get('KM'))
                    i+=1
            else:
                info = u"没有班次"
        elif content.startswith(u"火车"):
            if len(strs) < 3:
                fsta = u"广州"
            else:
                fsta = strs[1]
            tsta = strs[2]
            results = webxmlhelper.GetResponse('trainurl',"getStationAndTimeByStationName",self.sh.Convert2UTF8(fsta),self.sh.Convert2UTF8(tsta))
            print results
            if len(results) > 0:
                i = 1
                for result in results:
                    info += u"%d.车次:%s\n始:%s\t终:%s\n%s[%s]\t-\t%s[%s]\n行程:%s花费时间:%s\n" % \
                    (i,result.get('TrainCode'),result.get('FirstStation'),result.get('LastStation'),result.get('StartStation') ,result.get('StartTime')
                    ,result.get('ArriveStation'),result.get('ArriveTime'),result.get('KM'),result.get('UseDate'))
                    i+=1
            else:
                info = u"没有班次"


        pprint.pprint(info)
        return info

    def translator(self,content):
        if content.startswith(u"翻译"):
            strs = self.sh.SplitString(content)
            results = webxmlhelper.GetResponse('translatorurl','Translator',self.sh.Convert2UTF8(strs[1]))
            info = ""
            if len(results) > 0:
                for result in results:
                    info += u"%s\t%s\n%s\n" % (result.get('WordKey'),result.get('Pron'),result.get('Translation'))
                    if result.get('Refer') <> None:
                        for ref in result.get('Refer'):
                            info += "%s\n" %ref
                        info += "\n"
                    if result.get('Sentence') <> None:
                        for sen in result.get('Sentence'):
                            info += "%s\n" % sen
            else:
                info = u"没有结果"
        pprint.pprint(info)
        return info

    def mobile(self,content):
        if content.startswith(u"手机"):
            strs = self.sh.SplitString(content)
            results = webxmlhelper.GetResponse('mobileurl','getMobileCodeInfo',self.sh.Convert2UTF8(strs[1]))
            info = ""
            if len(results) > 0:
                for result in results:
                    info += u"%s" % result.get('MobileCodeInfo')
            else:
                info = u"没有结果"
        pprint.pprint(info)
        return info

    def tradition(self,content):
        strs = self.sh.SplitString(content)
        results = webxmlhelper.GetResponse('traditionurl','toSimplifiedChinese',self.sh.Convert2UTF8(strs[1]))
        info = ""
        if len(results) > 0:
            for result in results:
                info = u"%s" % result.get('toSimplifiedChineseResult')
            if info == strs[1]:
                results = webxmlhelper.GetResponse('traditionurl','toTraditionalChinese',self.sh.Convert2UTF8(strs[1]))
                if len(results) > 0:
                    for result in results:
                        info = u"%s" % result.get('toTraditionalChineseResult')
        else:
            info = u"没有结果"
        pprint.pprint(info)
        return info

    def huilv(self,content):
        curs = ['USD','MOP']
        info = ''
        for cur in curs:
            info += (htmlhelper.GetHuiLV('CNY', cur))
        return info

    def domain(self,content):
        strs = self.sh.SplitString(content)
        if len(strs)>1:
            info = htmlhelper.GetDomain(strs[1])
        else:
            info = htmlhelper.GetDomain('116.255.220.141')
        return info

if __name__ == '__main__':
    api = ApiHelper()
    result = api.weather(u'珠海')
    pprint.pprint( result)
