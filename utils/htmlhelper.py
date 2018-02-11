#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from HTMLParser import HTMLParser
import json
from sgmllib import SGMLParser
import urllib2

#For python 3.x
#from html.parser import HTMLParser

#定义HTMLParser的子类,用以复写HTMLParser中的方法
class MyHTMLParser(HTMLParser):

    #构造方法,定义data数组用来存储html中的数据
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.links = []

    #覆盖starttag方法,可以进行一些打印操作
    def handle_starttag(self, tag, attrs):
        pass
        #print("Start Tag: ",tag)
        for attr in attrs:
            self.links.append(attr[1])

    #覆盖endtag方法
    def handle_endtag(self, tag):
        pass

    #覆盖handle_data方法,用来处理获取的html数据,这里保存在data数组
    def handle_data(self, data):
        if data.count('\n') == 0:
            self.data.append(data)

class TD(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_td = ""
        self.name = []

    def start_td(self, attrs):
        self.is_td = 1

    def end_td(self):
        self.is_td = ""

    def handle_data(self, text):
        if self.is_td == 1:
            self.name.append(text.strip().decode('gbk').encode('utf8'))

def GetHuiLV(fcur,tcur):
    content = urllib2.urlopen('http://qq.ip138.com/hl.asp?from=%s&to=%s&q=100' % (fcur,tcur)).read()
    td = TD()
    td.feed(content)
    return "%s %s 兑换 %s %s %s %s\n" % (td.name[0],td.name[3],td.name[2],td.name[5],td.name[1],td.name[4])

if __name__ == "__main__":

    curs = ['USD','EUR','JPY','HKD','MOP','GBP']
    results=[]
    for cur in curs:
        results.append(GetHuiLV('CNY',cur))


    '''
    #读取本地html文件.(当然也可以用urllib.request中的urlopen来打开网页数据并读取,这里不做介绍)
    #htmlFile = open(r"/Users/xualvin/Downloads/TFS.htm",'r')
    #content = htmlFile.read()
    html_code = """
        <a href="www.google.com"> google.com</a>
        <A Href="www.pythonclub.org"> PythonClub </a>
        <A HREF = "www.sina.com.cn"> Sina </a>
        """

    #创建子类实例
    parser = MyHTMLParser()

    #将html数据传给解析器进行解析
    parser.feed(html_code)

    print parser.data
    print parser.links
    '''


