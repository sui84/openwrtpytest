#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import json
from pymongo import MongoClient
import base64
import os
import time
import errno
import fcntl
import multiprocessing
import sys
import timehelper
'''
r 只读
w
a 追加
r+b 读写,b是二进制读写
w+b 写读
a+b 追加及读
w+ 打开文件会将原文件内容删除，可以同时对文件进行读写
r+ 打开文件会保持原文件内容不变，同样可以同时对文件进行读写
'''
class FHelper(object):
    def __init__(self, filename=r'd:\temp\test.txt'):
        self.fname = filename

    def SaveResult(self,content,ofile='d:\temp\test.txt',mode='a'):
        with open(ofile,mode) as f:
            f.write(content)

    def DeleteDuplicateLine(self):
        lines=self.GetAllLines()
        df=pd.DataFrame({"line":lines})
        result=df.drop_duplicates()
        with open(self.fname,'w') as f:
            f.writelines(result.line.tolist())

    @timehelper.elapsedtimedeco(True)
    def SearchStrsWithPandas(self,strs):
        searchlines=[]
        lines=self.GetAllLines()
        df=pd.DataFrame({"line":lines})
        for str in strs:
            result=df[df.line.str.contains(str)].drop_duplicates()
            searchlines = searchlines + result.line.tolist()
        return searchlines

    def SearchStrWithPandas(self,str,ofile):
        lines=self.GetAllLines()
        df=pd.DataFrame({"line":lines})
        result=df[df.line.str.contains(str)] #.drop_duplicates()
        with open(ofile,'ab') as f:
            f.write("[%s][%s]:" % (self.fname,str) )
            f.writelines(result.line.tolist())

    #@timehelper.elapsedtimedeco(True)
    def SearchStrs(self,strs):
        # find和in的方法效率都太低,pandas的效率更低。。。
        # use multiple process call the function can't return searchlines
        searchlines=[]
        content=self.GetFileContent()
        for str in strs:
            if str in content:
                print "found ",str
                #self.SearchStrWithPandas(str)
                lines = self.GetAllLines()
                for line in lines:
                    if str in line:
                        searchlines.append(line)
        return searchlines


    def SearchStr(self,str):
        searchlines=[]
        content=self.GetFileContent()
        i=content.find(str)
        if i>0:
            lines = self.GetAllLines()
            for line in lines:
                j = line.find(str)
                if j>0:
                    searchlines.append(line)
        return searchlines

    def GetFileContent(self):
        '''获取文件内容字符串'''
        f = open(self.fname,'r')
        txt = f.read()
        f.close()
        return txt
        
    def GetAllLines(self):
        '''获取文件行数组'''
        f = file(self.fname,'rb')
        data = f.readlines()
        f.close()
        return data

    def GetAllLinesWithoutEnter(self):
        '''获取文件行数组'''
        f = file(self.fname,'rb')
        data = f.read()
        lines=data.splitlines()
        f.close()
        return lines

    def SaveLines(self,lines,mode='w'):
        #不确定哪种写法好
        #newlines = [line+'\n' for line in lines]  #\n换行符（转义字符）
        newlines = '\n'.join(lines)
        dirname=os.path.dirname(self.fname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.fname,mode) as f:
            f.writelines(newlines)

    def SaveFileContent(self,content,mode='w'):
        '''
        f = file(self.fname,'w') #直接清空，不能用f.readline()
        f.write(line)
        #f.flush() #立刻写进去
        f.close() #写进IO
        '''
        #no need cloase with below
        with open(self.fname,mode) as f:
            f.write(content)
            
    def SaveByteStrToFile(self,bytestr):
        '''将字节字符串转成文件'''
        binstr = base64.b64decode(bytestr)
        with open(self.fname,'wb') as f:
            f.write(binstr)
            
    def SaveDict(self,dictObj):
        '''保存字典内容成json文件'''
        jsObj = json.dumps(dictObj)
        fileObject = open(self.fname, 'w')
        fileObject.write(jsObj)
        fileObject.close()
    def SaveDictList(self,dictListObj):
        '''保存字典数组成各种格式'json', 'xls', 'yaml', 'csv', 'dbf', 'tsv', 'html', 'latex', 'xlsx', 'ods'''
        fileObject = open(self.fname, 'w')
        for dictObj in dictListObj:
            jsObj = json.dumps(dictObj)
            fileObject.write(jsObj)
            fileObject.write('\n')
        fileObject.close()
    def SaveContent(self,contents):
        fileObject = open(self.fname, 'w')
        fileObject.write(contents)
        fileObject.close()

    def SaveDictListToFile(self,dictListObj,type,headers=None):
        tplist=[]
        if len(dictListObj)>1:
            headers=tuple(dictListObj[0])
        for dictObj in dictListObj:
            tplist.append(tuple(dictObj.values()))
        self.SaveTupleListToFile(tplist,type,headers)

    def SaveTupleListToFile(self,tplist,type,headers=None):
        data=tablib.Dataset(*tplist,headers=headers)
        types = ('json', 'xls', 'yaml', 'csv', 'dbf', 'tsv', 'html', 'latex', 'xlsx', 'ods')
        validType = False
        typeIndex = 0
        for i in range(0, len(types)):
            if types[i].upper()==type.upper():
                validType = True
                typeIndex =i
                break
        if validType:
                fileObject = open(self.fname, 'w')
                if types[typeIndex].upper()=='json'.upper():
                    fileObject.write(data.json)
                if types[typeIndex].upper()=='xls'.upper():
                    fileObject.write(data.xls)
                if types[typeIndex].upper()=='yaml'.upper():
                    fileObject.write(data.yaml)
                if types[typeIndex].upper()=='csv'.upper():
                    print data.csv
                    fileObject.write(data.csv)
                if types[typeIndex].upper()=='dbf'.upper():
                    fileObject.write(data.dbf)
                if types[typeIndex].upper()=='tsv'.upper():
                    fileObject.write(data.tsv)
                if types[typeIndex].upper()=='html'.upper():
                    fileObject.write(data.html)
                if types[typeIndex].upper()=='latex'.upper():
                    fileObject.write(data.latex)
                if types[typeIndex].upper()=='xlsx'.upper():
                    fileObject.write(data.xlsx)
                if types[typeIndex].upper()=='ods'.upper():
                    fileObject.write(data.ods)
                fileObject.close()

if os.name == 'nt':
    import win32con, win32file, pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0 # The default value
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED(  )

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno(  ))
        win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)

    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno(  ))
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
elif os.name == 'posix':
    from fcntl import LOCK_EX, LOCK_SH, LOCK_NB

    def lock(file, flags):
        fcntl.flock(file.fileno(  ), flags)

    def unlock(file):
        fcntl.flock(file.fileno(  ), fcntl.LOCK_UN)
else:
    raise RuntimeError("File Locker only support NT and Posix platforms!")

def writeLogfile(args):
    try:
        time.sleep(fakerhelper.GetRandomInt(1,5))
        logfile, msg = args
        f = open(logfile, "a+")
        lock(f, LOCK_EX)
        f.write(msg + "\n")
        unlock(f)
    except Exception as ex:
        print("Error Info: %s"%(str(ex)))
    finally:
        f.close()

def writeLogfilewithoutlock(args):
    try:
        time.sleep(fakerhelper.GetRandomInt(1,5))
        logfile, msg = args
        f = open(logfile, "a")
        #lock(f, LOCK_EX)
        f.write(msg + "\n")
        #unlock(f)
    except Exception as ex:
        print("Error Info: %s"%(str(ex)))
    finally:
        f.close()

def multiExecute(logfile, count):
    pool = multiprocessing.Pool(processes = count)
    pool.map(writeLogfile, [(logfile, a * 80) for a in range(1,10000)]) #"abcdefghijklmnopqrstuvwxyz"])

def multiExecutewithoutlock(logfile, count):
    pool = multiprocessing.Pool(processes = count)
    pool.map(writeLogfilewithoutlock, [(logfile, str(a)* 80) for a in range(1,10000)]) #"abcdefghijklmnopqrstuvwxyz"])

if __name__ == '__main__':
    # python fhelper.py testlockfile
    # 两个测试结果一样。。。不知文件锁起作用了没
    if len(sys.argv) > 1 and sys.argv[1]=="testlockfile":
        print sys.argv[1]
        logfile = r"d:\temp\log.txt"
        multiExecute(logfile, 5)
    elif len(sys.argv) > 1 and sys.argv[1]=="testnonlockfile":
        print sys.argv[1]
        logfile = r"d:\temp\log.txt"
        multiExecutewithoutlock(logfile, 5)
    else:
       # fhelper应用
        dictObj = {
        'andy':{
            'age': 23,
            'city': 'shanghai',
            'skill': 'python'
        },
        'william': {
            'age': 33,
            'city': 'hangzhou',
            'skill': 'js'
        }
        }
        dictListObj = [{'name':'andy',"age":23,"city":"shanghai","skill":"python"},{'name':'william',"age":33,"city":"hangzhou","skill":"js"}]
        f = FHelper(filename=r'd:\temp\test.txt')
        f.SaveDict(dictObj)
        f2 = FHelper(filename=r'd:\temp\test.csv')
        f2.SaveDictListToFile(dictListObj,"csv",headers={'name',"age","city","skill"})
        tplist = [('andy',23,"shanghai","python"),('william',23,"shanghai","java"),]
        f2.SaveTupleListToFile(tplist,"csv",headers={'name',"age","city","skill"})
        f.GetAllLines()




