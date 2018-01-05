#coding=utf-8
import time
import traceback
import sys
sys.path.append("../db/")



import multiprocessing
import os
import fhelper

class Test(object):
    def __init__(self):
        self.outf = '/mnt/sda1/temp/test.txt'
        self.fh = fhelper.FHelper(self.outf)
        self.array = ['YIE', 'AKU', 'AAT', 'NGQ', 'AKA', 'AQG', 'AOG', 'AVA', 'AYN', 'AEB', 'BSD', 'BAV', 'RLK', 'BHY', 'BJS', 'BFU', 'BFJ', 'BPL', 'NBS', 'CGQ', 'CGD', 'BPX', 'CSX', 'CIH', 'CZX', 'CHG', 'CTU', 'CYI', 'CIF', 'CKG', 'DLU', 'DLU', 'DLC', 'DDG', 'DQA', 'DAT', 'DAX', 'DAX', 'LUM', 'DEY', 'DIG', 'DGM', 'DOY', 'DNH', 'DSN', 'ERL', 'ENH', 'FUO', 'FUG', 'FYN', 'FOC', 'KOW', 'GOQ', 'GHN', 'LHK', 'GYS', 'CAN', 'KWL', 'KWE', 'GYU', 'HRB', 'HAK', 'HLD', 'HMI', 'HMI', 'HDG', 'HGH', 'HZG', 'HFE', 'HEK', 'HNY', 'HTN', 'HTN', 'HKG', 'HIA', 'HJJ', 'HUN', 'TXN', 'XAA', 'HYN', 'HET', 'HUZ', 'JGD', 'JMU', 'KNC', 'JGN', 'SWA', 'JIL', 'TNA', 'JIC', 'JDZ', 'JGS', 'JHG', 'JNG', 'JJN', 'JNZ', 'JUH', 'JIU', 'JZH', 'JXA', 'KJI', 'KGT', 'KHH', 'KHG', 'KHG', 'KRY', 'KNH', 'KCA', 'KRL', 'KMG', 'LHW', 'LXA', 'LCX', 'LIA', 'LYG', 'LLB', 'LJG', 'LNJ', 'LXI', 'LYI', 'LZY', 'HZH', 'LZH', 'LCX', 'LYA', 'LZO', 'MFM', 'MZG', 'LUM', 'NZH', 'MXZ', 'MXZ', 'MIG', 'OHE', 'MDG', 'NLT', 'KHN', 'NAO', 'NKG', 'NNG', 'NTG', 'NNY', 'NGB', 'PZI', 'SYM', 'HSN', 'JIQ', 'IQM', 'TAO', 'IQN', 'SHP', 'NDG', 'JJN', 'JUZ', 'RKZ', 'SYX', 'SHA', 'SHP', 'SWA', 'SHS', 'SHE', 'SZX', 'SJW', 'JJN', 'SYM', 'SZV', 'TCG', 'TXG', 'TPE', 'TTT', 'TYN', 'HYN', 'TVS', 'TCZ', 'TSN', 'THQ', 'TNH', 'TGO', 'TEN', 'TEN', 'TLQ', 'WXN', 'WEF', 'WEH', 'WNH', 'WNH', 'WNZ', 'WUA', 'WUH', 'WHU', 'HLH', 'URC', 'WUX', 'WUS', 'WUZ', 'XMN', 'SIA', 'XFN', 'DIG', 'XFN', 'XIC', 'XIL', 'XNT', 'ACX', 'XNN', 'JHG', 'XUZ', 'ENY', 'YNZ', 'YTY', 'YNJ', 'YNT', 'YBP', 'YIH', 'YIC', 'LDS', 'YIN', 'INC', 'YIN', 'YIW', 'LLF', 'UYN', 'YCU', 'YUS', 'YUS', 'DYG', 'ZQZ', 'YZY', 'ZHA', 'ZAT', 'CGO', 'HJJ', 'ZGN', 'ZHY', 'HSN', 'ZUH', 'ZUZ', 'ZYI']

    def test(self):
        record1 = []   # store input processes
        record2 = []   # store output processes
        lock  = multiprocessing.Lock()    # To prevent messy print
        queue = multiprocessing.Queue()

        #citycodes = self.yamldata.get('citycodes')
        # input processes
        for i in range(len(self.array)):
            process = multiprocessing.Process(target=self.inputQ,args=(queue,i))
            process.start()
            record1.append(process)

        for process in record1:
            process.join()

        # output processes
        for i in range(len(self.array)):
            process = multiprocessing.Process(target=self.outputQ,args=(queue,lock,i))
            process.start()
            record2.append(process)

        for process in record2:
            process.join()

    def inputQ(self,queue,i):
        info = "进程号 %s : 时间: %s"%(os.getpid(),int(time.time()))
        print info
        valuedicts={"web:startCity":self.array[i],"web.lastCity":"ZUH"}
        queue.put(valuedicts)

    # 获取 worker
    def outputQ(self,queue,lock,i):
        info = queue.get()
        self.fh.SaveFileContent(str(info),'a')
        print str(os.getpid()) , '(get):' , info


if __name__ == '__main__':
    '''
    print time.ctime(), 'Start...'
    try:
        if len(sys.argv) > 1:
            print sys.argv[1]
    except Exception,e:
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
    finally:
        print time.ctime(), 'Done!'
    '''
    #print os.path.abspath('../../conf/test.yaml')'
    print os.path.realpath(__file__),os.path.dirname(os.path.realpath(__file__))
    #t = Test()
    #t.test()
