import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import yaml
import xmlhelper
import httphelper
import xlshelper
from py_linq import Enumerable
import pickledb
import urlparse
import itertools
import strhelper
import pprint

DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
YAMLF = os.path.join(DIR,'conf/test.yaml')
EXCELF = os.path.join(DIR,'excel/test.xlsx')
DBF = os.path.join(DIR,'data/pickledb/test.db')
XMLPATH = os.path.join(DIR,'xml/%s%s.xml')
with open(YAMLF) as f:
    YAMLDATA=yaml.load(f)
THREADNUM = YAMLDATA.get('threadnum')
WXNameSpace = YAMLDATA.get('webxmlnamespace')
XMLHELPER = xmlhelper.XmlHelper()
HTTPHELPER = httphelper.HttpHelper()
XLSHELPER = xlshelper.XlsHelper(EXCELF)
SHHELPER = strhelper.StrHelper()
TESTDB = pickledb.load(DBF,True)

def GetResult(action,at):
    result = None
    if action == "getDetailInfoByTrainCode":
        if at.get('TrainStation').get('value') <> None:
            result =  {'TrainStation':at.get('TrainStation').get('value'),'ArriveTime':at.get('ArriveTime').get('value'),'StartTime':at.get('StartTime').get('value')
                   ,'KM':at.get('KM').get('value')}
    elif action == "getStationAndTimeByStationName":
        if at.get('TrainCode').get('value') <> None:
            result =  {'TrainCode':at.get('TrainCode').get('value'),'FirstStation':at.get('FirstStation').get('value'),'LastStation':at.get('LastStation').get('value')
                   ,'StartStation':at.get('StartStation').get('value'),'StartTime':at.get('StartTime').get('value'),'ArriveStation':at.get('ArriveStation').get('value')
                   ,'ArriveTime':at.get('ArriveTime').get('value'),'KM':at.get('KM').get('value'),'UseDate':at.get('UseDate').get('value')}
    elif action == "getStationNameDataSet":
        if at.get('station_name').get('value') <> None:
            result =  {'station':at.get('station_name').get('value')}
    elif action == 'getDomesticAirlinesTime':
        if at.get('AirlineCode').get('value') <> None:
            result =  {'Week':at.get('Week').get('value'),'AirlineStop':at.get('AirlineStop').get('value'),'StartDrome':at.get('StartDrome').get('value')
                ,'ArriveTime':at.get('ArriveTime').get('value'),'Company':at.get('Company').get('value'),'AirlineCode':at.get('AirlineCode').get('value')
                ,'StartTime':at.get('StartTime').get('value'),'ArriveDrome':at.get('ArriveDrome').get('value'),'Mode':at.get('Mode').get('value')}
    elif action == 'getDomesticCity':
        if at.get('Abbreviation').get('value') <> None:
            result = {'Abbreviation':at.get('Abbreviation').get('value'),'cnCityName':at.get('cnCityName').get('value'),'enCityName':at.get('enCityName').get('value')}
    elif action == 'Translator':
        if at.get('Trans').get('WordKey') <> None:
            trans = at.get('Trans')
            result = {'WordKey':trans.get('WordKey').get('value'),'Pron':trans.get('Pron').get('value'),'Translation':trans.get('Translation').get('value')}
        if at.get('Refer') <> None and type(at.get('Refer')) is list:
            reflist=[]
            for ref in at.get('Refer'):
                reflist.append(ref.get('Rel').get('value'))
            result['Refer'] = tuple(reflist)
        if at.get('Sentence') <> None and type(at.get('Sentence')) is list:
            senslist = []
            for sens in at.get('Sentence'):
                senslist.append('%s\n%s' % (sens.get('Orig').get('value'),sens.get('Trans').get('value')))
            result['Sentence'] = tuple(senslist)
    elif action == 'getMobileCodeInfo':
        result = {'MobileCodeInfo':at.get('value')}
    elif action == 'toSimplifiedChinese':
        result = {'toSimplifiedChineseResult':at.get('value')}
    elif action == 'toTraditionalChinese':
        result = {'toTraditionalChineseResult':at.get('value')}
    return result

def GetResponse(urlkey,action,*args):
    reqpath = XMLPATH % (action,'Req')
    nsaction= urlparse.urljoin(WXNameSpace,action)
    url= YAMLDATA.get(urlkey)
    reqxml = SHHELPER.ReplaceStringFile(reqpath,*args)
    #resxml = HTTPHELPER.WebServiceResponse(url,nsaction,reqxml)
    resxml = HTTPHELPER.PostXMLRequest(url,reqxml)
    result = XMLHELPER.GetDictsByXStr(resxml)
    if action == "getDetailInfoByTrainCode":
        r = result.get('Envelope').get('Body').get('getDetailInfoByTrainCodeResponse').get('getDetailInfoByTrainCodeResult').get('diffgram').get('getDetailInfo').get('TrainDetailInfo')
    elif action == "getStationAndTimeByStationName":
        r = result.get('Envelope').get('Body').get('getStationAndTimeByStationNameResponse').get('getStationAndTimeByStationNameResult').get('diffgram').get('getStationAndTime').get('TimeTable')
    elif action == "getStationNameDataSet":
        r = result.get('Envelope').get('Body').get('getStationNameDataSetResponse').get('getStationNameDataSetResult').get('diffgram').get('getStationNameDataSet').get('StationName')
    elif action == 'getDomesticAirlinesTime':
        r = result.get('Envelope').get('Body').get('getDomesticAirlinesTimeResponse').get('getDomesticAirlinesTimeResult').get('diffgram').get('Airlines').get('AirlinesTime')
    elif action == 'getDomesticCity':
        r = result.get('Envelope').get('Body').get('getDomesticCityResponse').get('getDomesticCityResult').get('diffgram').get('Airline1').get('Address')
    elif action == 'Translator':
        r = result.get('Envelope').get('Body').get('TranslatorResponse').get('TranslatorResult').get('diffgram').get('Dictionary')
    elif action == 'getMobileCodeInfo':
        r = result.get('Envelope').get('Body').get('getMobileCodeInfoResponse').get('getMobileCodeInfoResult')
    elif action == 'toSimplifiedChinese':
        r = result.get('Envelope').get('Body').get('toSimplifiedChineseResponse').get('toSimplifiedChineseResult')
    elif action == 'toTraditionalChinese':
        r = result.get('Envelope').get('Body').get('toTraditionalChineseResponse').get('toTraditionalChineseResult')
    results = []
    if type(r) is list:
        for at in r:
            result =  GetResult(action,at)
            results.append(result)
    else:
        result =  GetResult(action,r)
        results.append(result)
    return results

def CallSoap(url,action,valuedicts=None):
    reqpath=XMLPATH % (action,'Req')
    respath=XMLPATH % (action,'Res')
    soapaction= urlparse.urljoin(WXNameSpace,action)
    if valuedicts<>None:
        XMLHELPER.SetTagValues(reqpath,valuedicts)
    HTTPHELPER.CallWebService(url,soapaction,reqpath,respath)
    r=XMLHELPER.GetDictsByXFile(respath)
    return r

def QueueToList(queue):
    results= []
    while not queue.empty():
        result = queue.get()
        results.append(result)
    print results
    return results

def GetCollFromXLS(sheetname):
    dicts = XLSHELPER.GetSheetToDicts(sheetname)
    colls=Enumerable(dicts)
    return colls

def SaveToDB(kname,dicts):
    testdb = pickledb.load(DBF,True)
    testdb.set(kname,dicts)

def GetFromDB(kname):
    testdb = pickledb.load(DBF,True)
    dicts = testdb.get(kname)
    return dicts

def GetPermutations(name):
    stas = GetFromDB(name)
    stasper=list(itertools.permutations(stas,2))
    return stasper

#region
def GetAbb(colls,city):
    if city == None:
        cabbs = "ZUH"
    else:
        cabbs = colls.where(lambda x:x.get('cnCityName').find(city)>-1 or x.get('enCityName').find(city)>-1).select(lambda x:x.get('Abbreviation')).first_or_default()
    return cabbs

def GetAbbs(fcity,tcity):
    #dicts = webxmlhelper.XLSHELPER.GetSheetToDicts("citycodes")
    dicts=TESTDB.get('citycodes')
    colls=Enumerable(dicts)
    fabbs=GetAbb(colls,fcity)
    tcabbs=GetAbb(colls,tcity)
    return fabbs,tcabbs

def SaveCityCodes():
    #addcolls=Enumerable(citylist)
    #citycodes=addcolls.select(lambda x:x.get('Abbreviation').get('value')).to_list()
    results = GetResponse('airurl',"getDomesticCity")
    TESTDB.set('citycodes',results)
    XLSHELPER.SaveDictsToSheet("citycodes", results)

def SaveStations():
    results = GetResponse('trainurl',"getStationNameDataSet")
    TESTDB.set('stations',results)
    XLSHELPER.SaveDictsToSheet("stations", results)
#endregion

if __name__ == '__main__':
    # train
    # pass u'广州',u'化州' will cause 400 bad request ,need pass utf8 characters
    #results = GetResponse('trainurl',"getStationAndTimeByStationName",'广州','化州')
    #results = GetResponse('trainurl',"getStationAndTimeByStationName",u'广州'.encode('utf8'),'化州'.encode('utf8'))
    #results = GetResponse('trainurl',"getDetailInfoByTrainCode",'K1232')
    #results = GetResponse('trainurl',"getDetailInfoByTrainCode",'你好')
    #results = GetResponse('trainurl',"getStationNameDataSet")

    #airline
    #results = GetResponse('airurl',"getDomesticCity")
    results = GetResponse('airurl',"getDomesticAirlinesTime",'KWL','ZUH')

    #translator
    #results = GetResponse('translatorurl','Translator','suggest')
    #results = GetResponse('translatorurl','Translator',u'建议'.encode('utf8'))

    #mobile
    #results = GetResponse('mobileurl','getMobileCodeInfo','12345678901')

    #traditional
    #results = GetResponse('traditionurl','toSimplifiedChinese','簡單')
    #results = GetResponse('traditionurl','toTraditionalChinese','简单')
    print results
