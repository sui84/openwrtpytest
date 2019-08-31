#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from faker import Faker
from faker.utils import text, decorators
from faker.utils.distribution import choice_distribution
from faker.providers import BaseProvider
import random
import time
import requests
import json
import yaml

def GetRandomInt(start,end):
    data = random.randint(start, end)
    return data

def GetRandomFloat():
    # fake.pyfloat(left_digits=3)  right_digits
    fake = Faker()
    data = fake.pyfloat()
    return data

def GetFakerDataFromList(arr):
    '''arr = ('a', 'b', 'c', 'd') , choose one from list
    '''
    provider = BaseProvider(None)
    data = pick = provider.random_element(arr)
    return

def GetFakerDataAsPercent(arr,arrp):
    '''arr = ('a', 'b', 'c', 'd')
       arrp = (0.5, 0.2, 0.2, 0.1)
    '''
    data = choice_distribution(arr, arrp)
    return

def GetFakerData(seed=0,type="name"):
    # seed>0 : the same with last value
    fake = Faker()
    if seed > 0 :
        fake.seed(4321)
    if type=="useragent":
        fstr = fake.user_agent()
    if type=="password":
        #可以指定长度，也可以不指定
        len = GetRandomInt(8,13)
        password=fake.password(len)
    elif type=="name":
        fstr = fake.name()
    elif type=="email":
        fstr = fake.email()
    elif type=="address":
        fstr = fake.address()
    elif type=="company":
        fstr = fake.company()
    elif type=="job":
        fstr = fake.job()
    elif type=="phonenumber":
        fstr = fake.phone_number()
    elif type=="ssn":
        fstr = fake.ssn()
    elif type=="profile":
        fake.profile()
    elif type=="text":
        fstr = fake.text()
    elif type=="ipv4":
        fstr = fake.ipv4()
    elif type=="ipv6":
        fstr = fake.ipv6()
    elif type=="beforenow":
        fstr = fake.date_time_this_century(before_now=True, after_now=False)
    elif type=="afterrenow":
        fstr = fake.date_time_this_century(before_now=False, after_now=True)
    elif type=="beforenowthisyear":
        fstr = fake.date_time_this_year(before_now=True, after_now=False)
    elif type=="afterrenowthisyear":
        fstr = fake.date_time_this_year(before_now=False, after_now=True)
    elif type=="beforenowthismonth":
        fstr = fake.date_time_this_month(before_now=True, after_now=False)
    elif type=="afterrenowthismonth":
        fstr = fake.date_time_this_month(before_now=False, after_now=True)

    return fstr

def RemoveSlugify(str, allow_dots=False):
    #"a'b/c" => 'abc'
    slug = text.slugify("a'b/c",allow_dots=allow_dots)
    return slug

def GetFakerUserAgent():
    USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    ug = random.choice(USER_AGENTS)
    return ug

def GetFakerHeader():
    HEADER = {
        'User-Agent': GetFakerUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
    return HEADER

def GetProxies(num=10):
    path='../conf/test.yaml'
    with open(path) as f:
        x=yaml.load(f)
    httpproxy = x.get('httpproxy') % num
    httpsproxy = x.get('httpsproxy') % num
    testipurl = x.get('testipurl')
    proxiesfile = x.get('proxiesfile')
    timeout = x.get('timeout,10')
    print httpproxy
    #清空文件
    with open(proxiesfile,'w') as f:
        f.truncate()
    r = requests.get(httpproxy)
    data=json.loads(r.text)
    for item in data.get('proxies'):
        proxystr =  item.get('http')
        ip = proxystr.split(':')[0]
        port = proxystr.split(':')[1]
        ValifyProxy(ip,port,testipurl,timeout,proxiesfile)
    with open(proxiesfile,'r') as f:
        lines = f.readlines()
    return lines

def ValifyProxy(ip,port,testipurl,timeout,proxiesfile):
    proxies={"http": "http://%s:%s"%(ip,port),"https": "http://%s:%s"%(ip,port)}
    start = time.time()
    try:
        r = requests.get(url=testipurl,headers=GetFakerHeader(),timeout=timeout,proxies=proxies)

        if not r.ok or r.text.find(ip)==-1:
            print 'failed %s:%s'%(ip,port)
        else:
            speed = round(time.time()-start, 2)
            print 'success %s:%s, speed=%s'%(ip,port,speed)
            with open(proxiesfile,'ab') as f:
                f.write(proxies.get('http')+'\n')
    except Exception,e:
            print 'failed %s:%s'%(ip,port)

if __name__ == '__main__':
    #获取IP代理
    GetProxies(100)

