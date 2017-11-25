#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from flask import Flask, request,make_response,render_template
import hashlib
import xml.etree.ElementTree as ET
import loghelper
import traceback
import requests
import os
import pprint
import uniout
import apihelper
import yaml
import pickledb


app = Flask(__name__)
app.debug=True
logger = loghelper.create_logger(r'/mnt/sda1/temp/log')
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates/reply_text.xml')
api = apihelper.ApiHelper()
cachefpath='../data/cache.db'
cachedb = pickledb.load(cachefpath,True)


@app.route('/',methods=['GET','POST'])
def wechat_auth():
    msg = "funcname : %s , request.args : %s" % (__name__ ,request.args)
    logger.info(msg)
    response = make_response("")
    try:
        if request.method == 'GET':
            token='weixintest'
            data = request.args
            signature = data.get('signature','')
            timestamp = data.get('timestamp','')
            nonce = data.get('nonce','')
            echostr = data.get('echostr','')
            s = [timestamp,nonce,token]
            s.sort()
            s = ''.join(s)
            if (hashlib.sha1(s).hexdigest() == signature):
                response  = make_response(echostr)
            else:
                response  = make_response("Not Valid!")
        else:
            rec = request.stream.read()
            print "Request post data:",rec
            xml_rec = ET.fromstring(rec)
            datadict = get_replydata(xml_rec)
            pprint.pprint(datadict)
            render = render_template("reply_text.xml",dict=datadict)
            response = make_response(render)
            #xml_rep = get_response(xml_rec)
            #response = make_response(xml_rep)
            response.content_type='application/xml;charset=utf-8'
    except Exception,e:
            type =xml_rec.find("MsgType").text
            tou = xml_rec.find('ToUserName').text
            fromu = xml_rec.find('FromUserName').text
            datadict = {"to":fromu,"from":tou,"time":str(int(time.time())),"type":type,"msg":e.message}
            render = render_template("reply_text.xml",dict=datadict)
            response = make_response(render)
            # log the exception
            err = "exception : %s , %s" % (e.message ,traceback.format_exc())
            logger.exception(err)
    finally:
        #pprint.pprint( request.__dict__)
        pprint.pprint( response.__dict__)
        return response

def get_replydata(xml_rec):
    '''
    import xml2dict
    xml = xml2dict.XML2Dict()
    r = xml.fromstring(textdata)
    r.get('xml').get('FromUserName').get('value')
    '''
    type =xml_rec.find("MsgType").text
    tou = xml_rec.find('ToUserName').text
    fromu = xml_rec.find('FromUserName').text
    datadict = {"to":fromu,"from":tou,"time":str(int(time.time())),"type":type,"msg":""}
    if type == 'image' or type == 'voice':
        dmedia_id = xml_rec.find('MediaId').text
        purl = xml_rec.find('PicUrl').text
        fname = xml_rec.find('CreateTime').text
        import urllib
        urllib.urlretrieve(purl,'/mnt/sda1/data/image/%s.jpg' % fname)
        print purl
    elif type == 'location':
        locx = xml_rec.find('Location_X').text
        locy = xml_rec.find('Location_Y').text
        scale = xml_rec.find('Scale').text
        location = xml_rec.find('Label').text
        wjdu="%s,%s" % (locx,locy)
        data = api.location(wjdu)
        datadict["msg"]=data
    else:
        content = xml_rec.find("Content").text
        data = get_replytext(content)
        datadict["msg"]=data
    print datadict.get("msg")
    return datadict

def get_replytext(content):
    content = content.strip()
    print 'enter content :',content
    cvalue = cachedb.get(content)
    cvalue =None
    if cvalue<>None:
        print 'get it from cache'
        data=cvalue
    else:
        if content.lower().startswith("ip"):
            content=content.replace("ip","").strip()
            data = api.ip(content)
        elif content.startswith(u"航班"):
            data=api.airline(content)
        elif content.startswith(u"火车"):
            data=api.train(content)
        elif content.startswith(u"翻译"):
            data=api.translator(content)
        elif content.startswith(u"手机"):
            data=api.mobile(content)
        elif content.startswith(u"简体") or content.startswith(u"繁体"):
            data=api.tradition(content)
        elif content.startswith(u"汇率"):
            data=api.huilv(content)
        elif content.startswith(u"域名"):
            data=api.domain(content)
        else:
            data = api.weather(content)
        cachedb.set(content,data)
    return data

if __name__ == '__main__':
    path='../conf/test.yaml'
    with open(path) as f:
        x=yaml.load(f)
    textdata = x.get('textdata')
    wxlink = x.get('wxlink')
    r=requests.get(wxlink)
    print r.text
    r=requests.post(wxlink,textdata)
    print r.text

