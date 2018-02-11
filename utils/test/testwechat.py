#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
from utils import setting,loghelper
import requests
import pprint
import traceback

txtmsg = '''<xml><ToUserName><![CDATA[gh_aa51bd9e39d7]]></ToUserName>
<FromUserName><![CDATA[or0iKv0sQHnLvqHyuDP9V29IciE0]]></FromUserName>
<CreateTime>1512571679</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<MsgId>6496445894585042944</MsgId>
</xml>'''
imagemsg = '''<xml><ToUserName><![CDATA[gh_aa51bd9e39d7]]></ToUserName>
<FromUserName><![CDATA[or0iKv0sQHnLvqHyuDP9V29IciE0]]></FromUserName>
<CreateTime>1512653299</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<PicUrl><![CDATA[%s]]></PicUrl>
<MsgId>6496796449815779275</MsgId>
<MediaId><![CDATA[%s]]></MediaId>
</xml>'''
locmsg = '''<xml><ToUserName><![CDATA[gh_aa51bd9e39d7]]></ToUserName>
<FromUserName><![CDATA[or0iKv0sQHnLvqHyuDP9V29IciE0]]></FromUserName>
<CreateTime>1512648333</CreateTime>
<MsgType><![CDATA[location]]></MsgType>
<Location_X>%f</Location_X>
<Location_Y>%f</Location_Y>
<Scale>16</Scale>
<Label><![CDATA[测试]]></Label>
<MsgId>6496775121008184811</MsgId>
</xml>'''
logger = loghelper.create_logger(setting.LOGPATH)
url='http://1889d8t892.iok.la/'

def TestWechat():
    SendTxtMsg('汽车 珠海 惠州 2017-12-09')
    '''
    SendTxtMsg('帮助')
    SendTxtMsg('珠海')
    SendTxtMsg('ip')
    SendTxtMsg('航班')
    SendTxtMsg('航班号')
    SendTxtMsg('航班 珠海 西安')
    SendTxtMsg('火车 广州 九江')
    SendTxtMsg('火车号 D7505')
    SendTxtMsg('翻译 建议')
    SendTxtMsg('翻译 advice')
    SendTxtMsg('简体 简体')
    SendTxtMsg('繁体 简体')
    SendTxtMsg('汇率 ')
    SendTxtMsg('域名 116.255.220.141 ')
    SendTxtMsg('手机 1376300002700')
    SendLoctMsg(22.5640211,113.01865)
    SendImageMsg('http://mmbiz.qpic.cn/mmbiz_jpg/BWyYmYdBMcjm9DToScfYsbMeiaopa22YtpLKxibeeGChMPkXbNq4gSywOiaMjLCLLBpyE9e07SnEbO31Z0z0bFnXQ/0','fJQv9eI5Sg-yjYHPrvGJJvq1ZFJwNWSQgvARKtMcAdjn1-H5dFyyy0SB3ZeyeeZC')
    '''

@loghelper.exception(logger)
def SendTxtMsg(str):
    msgstr = txtmsg %(str.encode('utf8'))
    req = requests.post(url,data=msgstr)
    if req.status_code == 200 and req.text<>'':
        logger.info(req.text)
        print len(req.text)
        print str,u'\n测试结果:\n'.encode('utf8'),req.text.encode('utf8')
    else:
        print str,u'测试失败!'.encode('utf8')

@loghelper.exception(logger)
def SendImageMsg(url,mediaid):
    msgstr = imagemsg %(url,mediaid)
    req = requests.post(url,data=msgstr)
    if req.status_code == 200 and req.text<>'':
        logger.info(req.text)
        print u'图片 测试结果:\n',req.text
    else:
        print u'图片 测试失败!'

@loghelper.exception(logger)
def SendLoctMsg(locx,locy):
    msgstr = locmsg %(locx,locy)
    req = requests.post(url,data=msgstr)
    if req.status_code == 200 and req.text<>'':
        logger.info(req.text)
        print locx,locy,u'测试结果\n',req.text
    else:
        print u'位置 测试失败!'


if __name__ == '__main__':
    TestWechat()
