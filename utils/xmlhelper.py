#!/mnt/sda1/opkg/usr/bin/python
# #encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xml.dom.minidom
import xml2dict
import fhelper


class XmlHelper(object):
    def __init__(self):
        pass

    #root
    def GetRootFromFile(self,filename):
        dom1=xml.dom.minidom.parse(filename)
        root=dom1.documentElement
        return root
    def SaveRootToFile(self,root,filename):
        f = fhelper.FHelper(filename)
        f.SaveFileContent(root.toxml())        
    
    #获取某个文本节点的值
    def GetTagValue(self,filename,tagname): 
        root = self.GetRootFromFile(filename)
        nodes= root.getElementsByTagName(tagname) 
        for nodelist in  nodes:
            if nodelist.nodeType in (nodelist.TEXT_NODE,nodelist.CDATA_SECTION_NODE):
                return nodelist.data
            else:
                for node in nodelist.childNodes:
                    if node.nodeType in (node.TEXT_NODE,node.CDATA_SECTION_NODE):
                        return node.data
    
    #改变某个文本节点的值
    def SetTagValue(self,filename,tagname,newvalue):
        root = self.GetRootFromFile(filename)
        nodes= root.getElementsByTagName(tagname) 
        for nodelist in  nodes:
            if nodelist.nodeType in (nodelist.TEXT_NODE,nodelist.CDATA_SECTION_NODE):
                return nodelist.data
            else:
                for node in nodelist.childNodes:
                    if node.nodeType in (node.TEXT_NODE,node.CDATA_SECTION_NODE):
                        oldvalue = node.data
                        node.data = newvalue
                        #print self.root.toxml()

    #改变一些文本节点的值
    def SetTagValues(self,filename,valuedicts):
        root = self.GetRootFromFile(filename)
        for valuedict in valuedicts:
            tagname=valuedict.get("tagname")
            newvalue=valuedict.get("newvalue")
            nodes= root.getElementsByTagName(tagname)
            for nodelist in  nodes:
                if nodelist.nodeType in (nodelist.TEXT_NODE,nodelist.CDATA_SECTION_NODE):
                    return nodelist.data
                else:
                    for node in nodelist.childNodes:
                        if node.nodeType in (node.TEXT_NODE,node.CDATA_SECTION_NODE):
                            oldvalue = node.data
                            node.data = newvalue
        #print root.toxml()
        self.SaveRootToFile(root,filename)

    def ChangeTagValues(self,root,objdicts):
        objkeys = tuple(objdicts)
        for tagname in objkeys:
            newvalue=objdicts.get(tagname)
            nodes= root.getElementsByTagName(tagname)
            for nodelist in  nodes:
                if nodelist.nodeType in (nodelist.TEXT_NODE,nodelist.CDATA_SECTION_NODE):
                    return nodelist.data
                else:
                    for node in nodelist.childNodes:
                        if node.nodeType in (node.TEXT_NODE,node.CDATA_SECTION_NODE):
                            oldvalue = node.data
                            node.data = newvalue
        return root

    def SetTagValues(self,filename,objdicts):
        #改变一些文本节点的值
        root = self.GetRootFromFile(filename)
        root = self.ChangeTagValues(root,objdicts)
        print root.toxml()
        self.SaveRootToFile(root,filename)
                        
    #从xml文件获取字典列表
    def GetDictsByXFile(self,filename):
        f=fhelper.FHelper(filename)
        xmlstr = f.GetFileContent()
        dicts = self.GetDictsByXStr(xmlstr)
        return dicts
    
    #从xml文本获取字典列表
    def GetDictsByXStr(self,xmlstr):
        xml = xml2dict.XML2Dict()
        r = xml.fromstring(xmlstr)
        #pprint(r)
        return r
        
if __name__ == '__main__':
    x= XmlHelper()
    path = r'/mnt/sda1/projects/openwrtpytest/xml/getDomesticCityRes.xml'
    r=x.GetDictsByXFile(path)
    address=r.get('Envelope').get('Body').get('getDomesticCityResponse').get('getDomesticCityResult').get('diffgram').get('Airline1').get('Address')
    print address[0]




