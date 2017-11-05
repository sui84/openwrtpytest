#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def ListsToDicts(listkey,listvalues):
    dicts = []
    for listvalue in listvalues:
        dictobj = dict(zip(listkey,listvalue))
        dicts.append(dictobj)
    return dicts

def ListToDict(listkey,listvalue):
    # list1 = ['key1','key2','key3'] list2 = ['1','2','3']
    # {'key3': '3', 'key2': '2', 'key1': '1'}
    dictobj = dict(zip(listkey,listvalue))
    return dictobj

def SetToDict(keys):
    # keys = {'a','b','c'} => {'a':[],'b':[],'c':[]}
    value = []
    d = dict.fromkeys(keys,value)
    return d

def StrToDict(dictstr):
    #也适用于list字符串转换成list
    d = eval(a)
    return d

def StrToDict2(dictstr):
    exec ("d=" + a)
    return d
