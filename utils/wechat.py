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
import json
import pickledb
import urllib2

app = Flask(__name__)
app.debug=True
logger = loghelper.create_logger(r'/usr/log/log')
templates_root = './templates/reply_text.xml'
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
            if type(datadict) is dict:
                pprint.pprint(datadict)
                render = render_template("reply_text.xml",dict=datadict)
            else:
                render = datadict
            response = make_response(render)
            #xml_rep = get_response(xml_rec)
            #response = make_response(xml_rep)
            response.content_type='application/xml;charset=utf-8'
    except Exception,e:
            mtype =xml_rec.find("MsgType").text
            tou = xml_rec.find('ToUserName').text
            fromu = xml_rec.find('FromUserName').text
            datadict = {"to":fromu,"from":tou,"time":str(int(time.time())),"type":mtype,"msg":e.message}
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
        media_id = xml_rec.find('MediaId').text
        purl = xml_rec.find('PicUrl').text
        fname = xml_rec.find('CreateTime').text
        import urllib
        imagepath=api.yamldata.get('imagepath')
        urllib.urlretrieve(purl,os.path.join(imagepath,'%s.jpg' % fname))
        datadict['media_id'] = media_id
        #xmlTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId>%s</MediaId></Image></xml>"
        #xmlstr = xmlTpl % ('or0iKv0sQHnLvqHyuDP9V29IciE0','gh_aa51bd9e39d7','1511629377','iCAGChBV08JYpQwwc-RfgxEoPl1cKQsJrWOTr0F58gbJCOjLNRGmMvuKQGBZxBLG')
        #return xmlstr
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

#{u'errcode': 48001, u'errmsg': u'api unauthorized hint: [Rgcvsa0045hsz3!]'}
def get_token():
    #获取微信access_token
    payload_access_token={
        'grant_type':'client_credential',
        'appid':'wx675d68299018008f',
        'secret':'87e1dbcf4b8170bb259e6bf0fdbc4a94'
    }
    token_url='https://api.weixin.qq.com/cgi-bin/token'
    r=requests.get(token_url,params=payload_access_token)
    dict_result= (r.json())
    print dict_result['access_token']
    return dict_result['access_token']
#获取上传文件的media_ID
#群发图片的时候，必须使用该api提供的media_ID
def get_media_ID(path):
    img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img={
        'access_token':get_token(),
        'type':'image'
    }
    data ={'media':open(path,'rb')}
    r=requests.post(url=img_url,params=payload_img,files=data)
    dict =r.json()
    print dict
    return dict['media_id']
#查询所有用户分组信息
def get_group_id():
    url="https://api.weixin.qq.com/cgi-bin/groups/get"
    payload_id={
        'access_token':get_token()
    }
    r=requests.get(url=url,params=payload_id)
    result=r.json()
    print result
    return result['groups']
#返回第一个有效的group 分组id
def get_first_group_id():
    groups =get_group_id()
    group_id =0
    for group in groups:
        if(group['count']!=0):
            group_id=group['id']
            break;
    return group_id
def send_img_to_first_group(path='/home/fit/Desktop/test.jpg'):
    group_id =get_first_group_id()
    pay_send_all={
        "filter":{
            "is_to_all":False,
           "group_id":group_id
        },
        "image":{
            "media_id":get_media_ID(path)
        },
        "msgtype":"image"
    }
    url="https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token="+get_token()
    r=requests.post(url=url,data=json.dumps(pay_send_all))
    result=r.json()
    print result
    #根据返回码的内容是否为０判断是否成功
    return result['errcode']==0

def send_txt_to_first_group(str='Hello World!'):
    group_id =get_first_group_id()
    pay_send_all={
        "filter":{
            "is_to_all":False,
            "group_id":group_id
        },
        "text":{
            "content":str
        },
        "msgtype":"text"
    }
    url="https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token="+get_token()
    #需要指定json编码的时候不会对中文转码为unicode，否则群发的消息会显示为unicode码,不能正确显示
    r=requests.post(url=url,data=json.dumps(pay_send_all,ensure_ascii=False,indent=2))#此处的必须指定此参数
    result=r.json()
    #根据返回码的内容是否为０判断是否成功
    return result['errcode']==0

def getMenu():
    getMenuResult = urllib2.urlopen(r'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + get_token())
    menuDict = json.loads(getMenuResult.read())
    menu = json.dumps(menuDict, ensure_ascii=False, encoding='utf-8').encode('utf-8')
    print(menu)

def createMenu():
  url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % get_token()
  data = {
   "button":[
   {
      "name":"看美图",
      "sub_button":[
      {
        "type":"click",
        "name":"美图",
        "key":"meitu"
      },
      {
        "type":"view",
        "name":"精选",
        "url":"http://m.jb51.net/photos"
      },
  {
        "type":"view",
        "name":"回顾",
        "url":"http://m.qzone.com/infocenter?g_f=#2378686916/mine"
      },
  {
        "type":"view",
        "name":"美图app",
        "url":"http://jb51.net/app/app.html"
      }]
 },
 {
      "name":"看案例",
      "sub_button":[
      {
        "type":"click",
        "name":"全部风格",
        "key":"style"
      },
      {
        "type":"click",
        "name":"全部户型",
        "key":"houseType"
      },
  {
        "type":"click",
        "name":"全部面积",
        "key":"area"
      },
  {
        "type":"view",
        "name":"更多案例",
        "url":"http://m.jb51.net/projects"
      }]
 },
 {
      "type":"view",
      "name":"设计申请",
      "url":"http://jb51.net/zhuanti/freedesign.jsp?src=3"

 }

 ]
}
  #data = json.loads(data)
  #data = urllib.urlencode(data)
  req = urllib2.Request(url)
  req.add_header('Content-Type', 'application/json')
  req.add_header('encoding', 'utf-8')
  response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False))
  result = response.read()
  return result


if __name__ == '__main__':
    print getMenu()
    createMenu()
    '''
    if(send_img_to_first_group(path='/usr/image/1511629377.jpg')):
        print 'success!'
    else:
        print 'fail!'


    path='../conf/test.yaml'
    with open(path) as f:
        x=yaml.load(f)
    textdata = x.get('textdata')
    wxlink = x.get('wxlink')
    r=requests.get(wxlink)
    print r.text
    r=requests.post(wxlink,textdata)
    print r.text
    '''

