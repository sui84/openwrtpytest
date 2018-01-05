import urlparse
import urllib

def GetUrlPath(self,url):
    proto,rest=urllib.splittype(url)
    host,rest=urllib.splithost(rest)
    return host,rest