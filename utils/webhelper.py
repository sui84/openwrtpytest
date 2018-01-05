#!/mnt/sda1/opkg/usr/bin/python
#coding:utf-8
import SimpleHTTPServer
import SocketServer
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
import sys
import BaseHTTPServer
import urlparse
import urllib
import traceback
from wechat import app
import commands

PORT = 8001

# 导入我们自己编写的application函数:
#from hello import application
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [  #建立一个想要返回的列表
                'CLIENT VALUES:',    #客户端信息
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),  #返回客户端的地址和端口
                'command=%s' % self.command,  #返回操作的命令，这里比然是'get'
                'path=%s' % self.path,  #返回请求的路径
                'real path=%s' % parsed_path.path, #返回通过urlparse格式化的路径
                'query=%s' % parsed_path.query, #返回urlparse格式化的查询语句的键值
                'request_version=%s' % self.request_version, #返回请求的http协议版本号
                '',
                'SERVER VALUES:', #服务器段信息
                'server_version=%s' % self.server_version, #返回服务器端http的信息
                'sys_version=%s' % self.sys_version, #返回服务器端使用的Python版本
                'protocol_version=%s' % self.protocol_version,  #返回服务器端使用的http协议版本
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):  #返回項添加头信息，包含用户的user-agent信息，主机信息等
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.output(message)
        return

    def do_POST(self):
        mpath,margs=urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.output(datas)

    def output(self, message):
         self.send_response(200)
         self.end_headers()
         self.wfile.write(message)

#avoid error: [Errno 125] Address already in use
def KillPrevBind():
     try:
        pidname= commands.getstatusoutput("netstat -atpn | grep %d | awk '{print $7}'" % PORT)
        print pidname
        if len(pidname) > 1:
            pidname = pidname[1]
        pid=pidname.split('/')[0]
        print pid
        output =  commands.getstatusoutput("kill %s" % pid)
        print output
     except Exception,e:
        print  'Error:',e.message,'\n',traceback.format_exc()

if __name__ == '__main__':
    # socket.error: [Errno 125] Address already in use ??
    try:
        # $ python webhelper.py dir
        #KillPrevBind()
        '''
        urls = ('/weixin', 'weixin',)
        app = web.application(urls, globals())
        app.run()
        '''
        if len(sys.argv) > 1 and sys.argv[1]=="dir":
            #$ 相当于以下命令  python -m SimpleHTTPServer 8001
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(("", PORT), Handler)
        elif len(sys.argv) > 1 and sys.argv[1]=="basehttp":
            httpd = BaseHTTPServer.HTTPServer(('0.0.0.0',PORT), WebRequestHandler)
        else:
            # 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
            httpd = make_server('', PORT, app)

        print "Serving HTTP on port ",PORT
        # need to set the allow_reuse_address before binding.
        httpd.allow_reuse_address = True
        # 开始监听HTTP请求:
        httpd.serve_forever()
    except Exception, e:
        print  'Error:',e.message,'\n',traceback.format_exc()
