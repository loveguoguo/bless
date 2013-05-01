#!/usr/bin/env python
#-*- coding:utf8 -*-

import httplib

url = 'http://localhost:8000/weixin/'
HOST = 'localhost'
PORT = 8000
data = '''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>'''

data2 = '''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[m]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>'''

def test(d):
    #pdata = urllib.urlencode(data)
    conn = httplib.HTTPConnection(HOST, PORT, False)
    conn.request('POST', '/weixin/', d, headers={'Content-Type': 'application/xml'})
    res = conn.getresponse()
    if res.status!= 200:
        f = open('test.html', 'w')
        f.write(res.read())
        f.close()
    else:
        import xml.etree.ElementTree as ET
        et = ET.fromstring(res.read())
        msg = {}
        if et.tag == 'xml':
            for child in et:
                msg[child.tag] = child.text
        for k, v in msg.iteritems():
            print k, v 


if __name__ == '__main__':
    test(data)
    test(data2)
