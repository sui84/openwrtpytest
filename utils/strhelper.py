#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import string
import pickle
import json
import re
import chardet
#S.split(str,'')
#S.join(list,'')


class StrHelper(object):
    def __init__(self):
        self.splitchars=re.compile(r",|，| |/|")

    def ReplaceStringFile(self,fpath,*args):
        with  open(fpath,'r') as f:
            str = f.read()
        # pass args will cause error : takes exactly 2 arguments (4 given)
        nstr = self.ReplaceString(str,*args)
        return nstr

    def ReplaceString(self,str,*args):
        # xmldata = re.sub('<web:startCity>(.*?)\</web:startCity>','<web:startCity>%s</web:startCity>' % fcitycode,xmldata)
        nstr = str % (args)
        return nstr

    def ReplaceListsString(self,str,lists):
        nlists=[(lambda x:str % x )(x) for x in lists]
        return nlists

    def SplitString(self,str):
        c=self.splitchars.split(str)
        return c

    def SerializeString(self,obj):
        dumpsed = pickle.dumps(obj)
        return dumpsed

    def SerializeToFile(self,obj,ofile):
        dumpsed = pickle.dumps(obj)
        pickle.dump(obj,open(ofile,'w'))

    def Deserialize(self,dumpsed):
        loadsed = pickle.loads(dumpsed)
        return loadsed

    def DeserializeFromFile(self,ifile):
        loadsed = pickle.load(open(ifile,'r'))
        return loadsed

    def Jsonstr2Obj(self,jsonstr):
        obj =json.loads(jsonstr)
        return obj

    def Obj2JsonStr(self,obj):
        jsonstr =json.dumps(obj)
        return jsonstr

    def Trim(self,str):
        return str.strip()

    def ReplaceIgnorecase(self,istr,str,rstr):
        #replace 函数区分大小写
        #istr 源字符串 , str 查找字符串 , rstr 替换字符串
        #str和rstr都不能以\结尾，不然会报错 SyntaxError: invalid syntax
        reg = re.compile(re.escape(str), re.IGNORECASE)
        ostr = reg.sub(rstr, istr)
        return ostr

    def Convert2UTF8(self,str):
        # detect unicode character cause error : TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>
        ostr=unicode(str).encode('utf8')
        return ostr

    def ConvertToUTF8(self,str):
        #先判断字符编码 for example 'iso-8859-1'
        #但是如果本身是unicode，会报错TypeError: Expected object of type bytes or bytearray, got: <type 'unicode'>
        cset = chardet.detect(str).get('encoding')
        ostr=str.decode(cset).encode('utf8')
        return ostr

    def ConvertToUnicode(self,str):
        cset = chardet.detect(str).get('encoding')
        ostr=unicode(str,cset)
        return ostr


