#coding:utf8
import BaseHTTPServer  
import urlparse  
import time
from SocketServer import ThreadingMixIn
import threading
import sqlite3
import logging
import urllib
from cas_export_info import pipelines
from cas_export_info import items
import cgi
import os
import scrapy
from lxml import etree as etree
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):  
    
    def do_POST(self):
        print 'post message'
        parsed_path = urlparse.urlparse(self.path) 
        length = self.headers.getheader('content-length');
        nbytes = int(length)
        data = self.rfile.read(nbytes)
        cur_thread = threading.currentThread()
        print 'Thread:%s\tdata:%s' % (cur_thread.getName(), data)
        for i in range(10) :
            print '%s:waiting...' % cur_thread.getName()
            time.sleep(1)


        message_parts = [ 'just a test']  
        message = '\r\n'.join(message_parts)  
        self.send_response(200)  
        self.end_headers()  
        self.wfile.write(message)  

    def show_list(self):
        sqlite_cx = sqlite3.connect("cas_info.sqlite")
        sqlite_cu = sqlite_cx.cursor()
        sqlite_cu.execute('select * from data')
        res = sqlite_cu.fetchall()
        html = '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body><table border="1" width="100%">'
        pipeline = pipelines.CasExportInfoPipeline()
        html += '<tr>'
        html += '<td width="30">' + cgi.escape('机构') + '</td>'
        for s in pipeline.field_map[:-1]:
            html += '<td width="30">' + cgi.escape(s[1]) + '</td>'
        html += '</tr>'
        for s in res:
            html += '<tr>'
            for i in xrange(len(s) - 1):
                ss = s[i]
                if type(ss) == unicode:
                    ss = ss.encode('utf8')[:100]
                else:
                    ss = str(ss)
                if i == 1:
                    html += '<td><a href="/show?url=' + urllib.quote(ss) + '">' + cgi.escape(ss) + '</a></td>'
                else:
                    html += '<td>' + cgi.escape(ss) + '</td>'
            html += '</tr>'
        html += '</body></html>'
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html)
    
    def show_page(self):
        url = urllib.unquote(self.path.split('=', 1)[1])
        sqlite_cx = sqlite3.connect("cas_info.sqlite")
        sqlite_cu = sqlite_cx.cursor()
        sqlite_cu.execute('select * from data where url = ?', [url])
        res = sqlite_cu.fetchall()[0]

        html = '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><frameset cols="50%,50%">'
        html += '<frame src="/display_info?url=' + self.path.split('=', 1)[1] + ' "/>'
        html += '<frame name="display" src="/display_page?url=' + self.path.split('=', 1)[1] + ' "/>'
        html += '</frameset></html>'
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html)

    def display_info(self):
        url = urllib.unquote(self.path.split('=', 1)[1])
        sqlite_cx = sqlite3.connect("cas_info.sqlite")
        sqlite_cu = sqlite_cx.cursor()
        sqlite_cu.execute('select * from data where url = ?', [url])
        res = sqlite_cu.fetchall()[0]
        pipeline = pipelines.CasExportInfoPipeline()
        html = '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body>'
        html += '<ul>'
        html += '<li><strong>' + cgi.escape('机构') + '</strong>' + cgi.escape(res[0].encode('utf8')) + '</li>'
        for i in xrange(len(pipeline.field_map) - 1):
            html += '<li onclick="parent.display.location.href=\'/display_page?url=' + self.path.split('=', 1)[1] + '&hightlight=' + urllib.quote(pipeline.field_map[i][1]) + '\'"><strong>' + cgi.escape(pipeline.field_map[i][1]) + '</strong><br>' + cgi.escape(res[i + 1].encode('utf8')) + '</li>'
        html += '</ul></body></html>'
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html)
    
    def display_page(self):
        url = None
        hightlight = None
        for s in self.path.split('?', 1)[-1].split('&'):
            a, b = s.split('=')
            if a == 'url':
                url = urllib.unquote(b)
            if a == 'hightlight':
                hightlight = urllib.unquote(b)
                print hightlight
        sqlite_cx = sqlite3.connect("cas_info.sqlite")
        sqlite_cu = sqlite_cx.cursor()
        sqlite_cu.execute('select page, institute  from data where url = ?', [url])
        ans = sqlite_cu.fetchall()
        page = str(ans[0][0])
        pipeline = pipelines.CasExportInfoPipeline()
        if hightlight is None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(page)
        else:
            institute = [s for s in pipeline.institute_name_map if ans[0][1].encode('utf8') == pipeline.institute_name_map[s]][0]
            import cas_export_info
            from cas_export_info import spiders
            for f in os.listdir('cas_export_info/spiders'):
                if f.endswith('.py') and not f.startswith('_'):
                    fi = f[: -3]
                    class_list = []
                    for l in open('cas_export_info/spiders/' + f):
                        if l.startswith('class'):
                            class_list.append(l[6:].split('(')[0].strip())
                    c = class_list[0]
                    __import__('cas_export_info.spiders.' + fi)
                    m = getattr(getattr(cas_export_info.spiders, fi), c)
                    name = m.name
                    if name == institute:
                        break
            new_obj = m()
            response = scrapy.http.response.html.HtmlResponse(url=url, body=page)
            ans, dom = new_obj.analy(response)
            item = items.CasExportInfoItem()
            item['url'] = ans['url']
            for f in new_obj.field_map:
                if f.decode('utf8') in ans and ans[f.decode('utf8')] != '' and f != '' and new_obj.field_map[f] != '':
                    item[new_obj.field_map[f]] = ans[f.decode('utf8')]
            main_field = [s[0] for s in pipeline.field_map if s[1] == hightlight][0]
            print main_field
            if main_field in item:
                if type(item[main_field][1]) == list:
                    for s in item[main_field][1]:
                        s.attrib['class'] = 'selected'
                else:
                    item[main_field][1].attrib['class'] = 'selected'
            self.send_response(200)
            self.end_headers()
            page = etree.tostring(dom, encoding = 'utf8')
            page = page.replace('<head>', '''<head><style type="text/css">
            .selected{
            border-style: solid;
            border-width:3px;
            border-color:  red ;
            }</style>''')
            self.wfile.write(page)
            
            

    def do_GET(self):
        print self.path
        if self.path == '/list':
            self.show_list()
        if self.path.startswith('/show?'):
            self.show_page()
        if self.path.startswith('/display_info?'):
            self.display_info()
        if self.path.startswith('/display_page?'):
            self.display_page()

class ThreadingHttpServer( ThreadingMixIn, BaseHTTPServer.HTTPServer ):
    pass

if __name__ == '__main__':
    server = ThreadingHttpServer(('0.0.0.0',18460), WebRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "Server loop running in thread:", server_thread.getName()
    while True:
        pass
