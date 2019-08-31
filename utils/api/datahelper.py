#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from db import mghelper
import mathhelper
import multiprocessing
import urlparse
from py_linq import Enumerable
import pprint
import timehelper
import traceback
import webxmlhelper
import timehelper



citycodes=webxmlhelper.YAMLDATA.get('citycodes')
airurl= webxmlhelper.YAMLDATA.get('airurl')
action='getDomesticAirlinesTime'
airreqpath= webxmlhelper.XMLPATH % (action, 'Req')
airsoapaction= urlparse.urljoin(webxmlhelper.WXNameSpace, action)
queue = multiprocessing.Queue()
mh=mghelper.MgHelper(server=webxmlhelper.YAMLDATA.get('mongoserver'),port=webxmlhelper.YAMLDATA.get('mongoport'),dbname=webxmlhelper.YAMLDATA.get('mongodb'))


def getairlines(reqxml):
    try:
        print reqxml
        #resxml = webxmlhelper.HTTPHELPER.WebServiceResponse(airurl, airsoapaction, reqxml)
        resxml = webxmlhelper.HTTPHELPER.PostXMLRequest(airurl,reqxml)
        result = webxmlhelper.XMLHELPER.GetDictsByXStr(resxml)
        r = result.get('Envelope').get('Body').get('getDomesticAirlinesTimeResponse').get('getDomesticAirlinesTimeResult').get('diffgram').get('Airlines').get('AirlinesTime')
        print r
        if type(r) is list:
            for at in r:
                #putinqueue(queue,at)
                mh.SaveDictObj(at,'citycodes')
        else:
            #putinqueue(queue,r)
            mh.SaveDictObj(r,'citycodes')
    except Exception,e:
        print  'Error:',e.message,'\n',traceback.format_exc()

def SaveDB(at):
    mh.SaveDictObj(at,'citycodes')

def putinqueue(queue,at):
    result = getresult(at)
    queue.put(result)

def getresult(at):
    if at.get('AirlineCode').get('value') <> None:
        result =  {'Week':at.get('Week').get('value'),'AirlineStop':at.get('AirlineStop').get('value'),'StartDrome':at.get('StartDrome').get('value')
            ,'ArriveTime':at.get('ArriveTime').get('value'),'Company':at.get('Company').get('value'),'AirlineCode':at.get('AirlineCode').get('value')
            ,'StartTime':at.get('StartTime').get('value'),'ArriveDrome':at.get('ArriveDrome').get('value'),'Mode':at.get('Mode').get('value')}
        print result
        return result

@timehelper.elapsedtimedeco(True)
def airline():
    with  open(airreqpath,'r') as f:
        xmldata = f.read()

    citycodes = webxmlhelper.TESTDB.get('citycodes')
    citylists = mathhelper.GetPermu(citycodes)
    reqxmls = webxmlhelper.SHHELPER.ReplaceListsString(xmldata,citylists)

    num = len(reqxmls)
    print "Process start ",len(reqxmls)

    from multiprocessing import Pool
    pool = Pool(processes = webxmlhelper.THREADNUM)
    for i in range(num):
        pool.apply_async(getairlines, args=(reqxmls[i],))

    pool.close()
    pool.join()
    print "Process end , save data start:"

    #results= webxmlhelper.QueueToList(queue)
    #webxmlhelper.XLSHELPER.SaveDictsToSheet("airlines", results)
    #joblib.dump(results,airlinespath)


if __name__ == '__main__':
    airline()
    #setcitycodes()
