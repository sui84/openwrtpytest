#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import math
from geopy.geocoders import Nominatim
import pprint

class GeoHelper(object):
    def __init__(self):
        self.gps=Nominatim()

    def ConvertGps(self,du,fen,miao):
        num = float(du) + float(fen)/60 + float(miao)/3600
        return num

    def ConvertGoogleToBaidu(self,wdu,jdu):
        #转换为百度标准
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = jdu
        y = wdu
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
        jdu = z * math.cos(theta) + 0.0065
        wdu = z * math.sin(theta) + 0.006
        wdu = str(wdu)
        jdu = str(jdu)
        return {"wdu":wdu,"jdu":jdu}

    def GetWJdu(self,address):
        location=self.gps.geocode(address)
        return (location.latitude,location.longitude)

    def GetLocation(self,wjdu):
        # ti 纬度 la 经度
        #发送http请求获取具体位置信息-不准!
        '''
        url = 'http://api.map.baidu.com/geocoder/v2/'
        ak = 'ak=1aZ2PQG7OXlk9E41QPvB9WjEgq5WO8Do'
        #back='&callback=renderReverse&location='
        back='&location='
        #location='34.992654,108.589507'
        location='%d,%d' % (ti,la)
        output = '&output=json&pois=0'
        url = url + '?' + ak + back + location + output

        temp = urllib2.urlopen(url)
        hjson = json.loads(temp.read())
        locate = hjson["result"]["formatted_address"]
        print locate
        mapinfo = hjson["result"]["sematic_description"]
        '''
        location = self.gps.reverse(wjdu)
        data = location.raw
        pprint.pprint(location.raw)
        '''
        {u'address': {u'country': u'\u65e5\u672c',
                      u'country_code': u'jp',
                      u'state': u'\u6771\u4eac\u90fd',
                      u'state_district': u'\u516b\u4e08\u652f\u5e81'},
         u'boundingbox': [u'29.5936109',
                          u'33.3686498',
                          u'139.4364077',
                          u'140.5727203'],
         u'display_name': u'\u516b\u4e08\u652f\u5e81, \u6771\u4eac\u90fd, \u65e5\u672c',
         u'lat': u'33.1069602',
         u'licence': u'Data \xa9 OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright',
         u'lon': u'139.767310718251',
         u'osm_id': u'3606090',
         u'osm_type': u'relation',
         u'place_id': u'179013016'}
        '''
        return data

if __name__ == '__main__':
    wdu = 30
    jdu = 140
    wjdu="%f,%f" % (wdu,jdu)
    g = GeoHelper()
    g.Getlocation(wjdu)

