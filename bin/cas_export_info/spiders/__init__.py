#coding:utf8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
"""
author:fnozoszzt@gmail.com
"""

import scrapy
import re
import os
import sys
import urlparse
from scrapy.http import Request
import logging
import bs4
import json
import lxml.etree as etree
from cas_export_info import items

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#logger.setFormat(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class MySpider(scrapy.Spider):
    """
    通用信息获取基类
    """
    name = None
    expert_url = {}
    #need_relative_path = True
    # main_page_xpath
    parse_xpath = None

    expert_list_exex_js_xpath = []
    expert_list_frame_xpath = False
    # 研究员xpath列表
    # 格式为研究员xpath, next_page xpath
    expert_list_xpath_list = []

    need_relative_path = False
    analy_data_conf = []

    self_parse_field = []

    # 网页上关键字对应
    field_map = {
    'name': 'name',
    '姓名': 'name',
    '性别': 'gender',
    '职称': 'title',
    '职务/职称': 'title',
    '学历': 'education',
    '电子邮件': 'email',
    '电子信箱': 'email',
    'email': 'email',
    'Email': 'email',
    '邮政编码': 'post_code',
    '邮编': 'post_code',
    '通讯地址': 'address',
    '地址': 'address',
    '电话': 'phone',
    '电话/传真': 'phone',
    '学科类别': 'subject_category',
    '联系电话': 'phone',
    '简历': 'resume',
    '简历介绍': 'resume',
    '个人简况': 'resume',
    'resume': 'resume',
    '教育和工作经历': 'resume',
    '研究方向': 'research_area',
    '研究领域与研究方向': 'research_area',
    'research_area': 'research_area',
    '专家类别': 'expert_category',
    '类别': 'expert_category',
    '研究领域': 'research_field',
    '研究兴趣与领域': 'research_field',
    '职务': 'office',
    '社会任职': 'office',
    '承担科研项目情况': 'research_projects',
    'research_projects': 'research_projects',
    '参与的科研项目': 'research_projects',
    '承担科研项目': 'research_projects',
    '部分在研项目': 'research_projects',
    '代表论著': 'works',
    '代表性著作': 'works',
    '部分代表性论著': 'works',
    '发表文章': 'works',
    '近年来代表性学术论著': 'works',
    'works': 'works',
    'all_info': 'all_info',
    'page': 'page'
    }

    def parse(self, response):
        """
        解析研究团队主页
        """
        logger.debug('main page get reponse')
        expert_cata = response.xpath(self.parse_xpath)
        for cata in expert_cata:
            if len(cata.xpath('@href').extract()) > 0:
                href = cata.xpath('@href').extract()[0]
                text = cata.xpath('text()').extract()[0]
                logger.debug('main page get cat : %s ; link : %s' % (text, href))
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_list_parse, meta={'text': text})
            
    def get_js_res(self, text):
        import subprocess
        text = text.encode('utf8')
        child = subprocess.Popen('node', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        child.stdin.write('document=process.stdout;' + text)
        child.stdin.close()
        output = child.stdout.read()
        return output

    def exec_js(self, page):
        dom = etree.HTML(page)
        for xpath in self.expert_list_exex_js_xpath:
            item_list = dom.xpath(xpath)
            for s in item_list:
                text = s.text
                res = self.get_js_res(text)
                s.text = ""#res.decode('utf8')
                for ss in etree.HTML(res).find('body'):
                    s.getparent().append(ss)
        return etree.tostring(dom)


    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if self.expert_list_xpath_list:
            page = self.exec_js(response.body)
            dom = etree.HTML(page)
            num = 0
            for item in self.expert_list_xpath_list:
                if len(item) >= 1:
                    expert_xpath = item[0]
                if len(item) >= 2:
                    next_page_xpath = item[1]
                if len(item) >= 3:
                    _ = item[2]

                expert_list = dom.xpath(expert_xpath)
                for expert in expert_list:
                    if len(expert.xpath('@href')) == 0:
                        continue
                    href = str(expert.xpath('@href')[0])
                    new_url = urlparse.urljoin(url, href)
                    num += 1
                    yield Request(new_url, callback=self.expert_info_parse)
                if next_page_xpath:
                    next_page = dom.xpath(next_page_xpath)
                    for s in next_page:
                        #print self.str2dom(s.extract())
                        if len(s.xpath('text()')) > 0 and s.xpath('text()')[0].strip() == u'下一页':
                            new_url = str(s.xpath('@href')[0])
                            new_url = urlparse.urljoin(response.url, new_url)
                            logger.debug('go next page, link : %s' % new_url)
                            if 'turn_flag' in response.meta:
                                yield Request(new_url, callback=self.expert_list_parse, meta={'text': last_text, 'turn_flag': response.meta['turn_flag'] + 1})
                            else:
                                yield Request(new_url, callback=self.expert_list_parse, meta={'text': last_text, 'turn_flag': 1})
            logger.debug('list page url : %s gen %d expert' % (url, num))

            if self.expert_list_frame_xpath:
                iframe_list = dom.xpath('//iframe')
                for iframe in iframe_list:
                    if len(iframe.xpath('@src')) == 0:
                        continue
                    href = str(iframe.xpath('@src')[0])
                    new_url = urlparse.urljoin(response.url, href)
                    yield Request(new_url, callback=self.expert_list_parse, meta={'text': last_text, 'frame': True})
            return
        last_text = response.meta['text']
        if last_text == u'院士':
            logger.debug('parse ys')
            expert_list = response.xpath('.//div[@class="TRS_Editor"]/table[1]//a[@href]')
            for expert in expert_list:
                name = expert.xpath('text()').extract()[0]
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
                #print name, href
        elif last_text == u'研究团队':
            logger.debug('parse yj')
            expert_list = response.xpath('.//div[@class="Custom_UnionStyle"]//a[@href]')
            for expert in expert_list:
                name_list = expert.xpath('text()').extract()
                href_list = expert.xpath('@href').extract()
                if len(name_list) > 0 and len(href_list) > 0:
                    name = name_list[0]
                    href = href_list[0]
                    #print name, href
                else:
                    continue
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        else:
            logger.debug('parse other')
            expert_list = response.xpath('.//div[@class="TRS_Editor"]//a[@href]')
            for expert in expert_list:
                name_list = expert.xpath('text()').extract()
                href_list = expert.xpath('@href').extract()
                if len(name_list) > 0 and len(href_list) > 0:
                    name = name_list[0]
                    href = href_list[0]
                else:
                    name_list = expert.xpath('.//font/text()').extract()
                    href_list = expert.xpath('@href').extract()
                    name = name_list[0]
                    href = href_list[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
                #print name, href

    def str2dom(self, text):
        dom = bs4.BeautifulSoup(text)
        delete_name = ['script', 'style']
        for n in delete_name:
            for node in dom.findAll(n):
                node.extract()
        return dom
        
    def expert_info_parse(self, response):
        """
        """
        logger.debug('expert info page get reponse')
        url = response.url
        logger.debug('info url : %s' % url)
        if url in self.expert_url:
            logging.debug('url repeat')
            return
        self.expert_url[url] = None
        logger.debug('to analy url : %s' % url)
        res, dom_obj = self.analy(response)
        if res is None:
            return
        item = items.CasExportInfoItem()
        item['url'] = res['url']
        for f in self.field_map:
            sys.stdout.flush()
            if f.decode('utf8') in res and res[f.decode('utf8')] != '' and f != '' and self.field_map[f] != '':
                item[self.field_map[f]] = res[f.decode('utf8')]
        #print json.dumps(item, ensure_ascii=False)
        return item

    # type 1: http://sourcedb.ipm.cas.cn/zw/zjrc/200908/t20090814_2401631.html
    # main info : list, key -> value, hightlight key
    # more info : list, item: key and value

    # type 2: http://sourcedb.aoe.cas.cn/zw/rck/201004/t20100408_2815646.html
    # main info : table
    # more info : two tr

    # type 3: http://sourcedb.ib.cas.cn/cn/expert/201112/t20111208_3409961.html
    # main info : list, key -> value, hightlight key
    # more info : many <p>, some empty line and <b> main next key
    # .. some info has single xpath
    # 5 basic info 6 resume 7 name

    # type 4: http://sourcedb.igsnrr.cas.cn/zw/zjrck/200906/t20090626_1842553.html 
    # strong is key other is value
    analy_data_conf = []

        
    def analy(self, response):
        #res = {'url': response.url}
        dom = etree.HTML(response.body)
        res = {'url': (response.url, '')}
        for item in self.analy_data_conf:
            if len(item) >= 1:
                conf_type = item[0]
            if conf_type == 1:
                res = self.analy_1(res, response, item, dom)
            if conf_type == 2:
                res = self.analy_2(res, response, item, dom)
            if conf_type == 3:
                res = self.analy_3(res, response, item, dom)
            if conf_type == 4:
                res = self.analy_4(res, response, item, dom)

        return res, dom

    def analy_1(self, res, response, item, dom):
        x1, x2, x3, x4, x5 = item[1: 6]
        info_list_1 = dom.xpath(x1)
        for sub_info in info_list_1:
            l = sub_info.xpath(x2)
            if len(l) == 1:
                k_dom = self.str2dom(etree.tostring(l[0]))
                key = l[0].text
                text_dom = self.str2dom(etree.tostring(sub_info))
                text = text_dom.text.replace(key, '')
                key = key.strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '').replace(u'：', '')
                res[key] = (text, sub_info)
        all_info = ''
        info_list_2 = dom.xpath(x3)
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath(x4)
            l2 = sub_info_list.xpath(x5)
            if len(l) > 0 and len(l2) > 0:
                key = self.str2dom(etree.tostring(l[0])).text.strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '').replace(u'：', '')
                value = self.str2dom(etree.tostring(l2[0])).text.strip()
                res[key] = (value, sub_info_list)
                if len(key) > 0 and len(value.strip()) > 0:
                    all_info += key.strip() + '\n' + value + '\n\n'
        res['all_info'] = (all_info, info_list_2)
        res_output = {k: v[0] for k, v in res.iteritems()}
        logging.error('get json\t' + json.dumps(res_output, ensure_ascii=False).encode('utf8'))
        res['page'] = (response.body, dom)#.decode('utf8', 'ignore')
        return res

    def analy_2(self, res, response, item, dom):
        x1, x2 = item[1: 3]
        info_list_1 = dom.xpath(x1)

        all_info = ''
        for sub_info in info_list_1:
            l = sub_info.xpath('td')
            if len(l) % 2 == 1:
                l = l[:-1]
            for i in range(0, len(l), 2):
                k_dom = self.str2dom(etree.tostring(l[i]))
                key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                v_dom = self.str2dom(etree.tostring(l[i + 1]))
                value = v_dom.text.strip()
                res[key] = (value, l[i])

                all_info += key + '\n' + value + '\n\n'
                res['all_info'] = (all_info, info_list_1)
        if x2:
            all_info = ''
            info_list_2 = dom.xpath(x2)
            for sub_info_list in info_list_2:
                l = sub_info_list.xpath('.//tr')
                text_list = []
                for i in l:
                    dom2 = self.str2dom(etree.tostring(i))
                    text = dom2.text.strip()
                    if len(text) > 0:
                        text_list.append(text)
                if len(text_list) == 2:
                    key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                    value =  text_list[1]
                    res[key] = (value, sub_info_list)
                    all_info += text_list[0] + '\n' + text_list[1] + '\n\n'
            
            res['all_info'] = (all_info, info_list_2)
        res_output = {k: v[0] for k, v in res.iteritems()}
        logging.error('get json\t' + json.dumps(res_output, ensure_ascii=False).encode('utf8'))
        res['page'] = (response.body, dom)#.decode('utf8', 'ignore')
        return res

    def analy_3(self, res, response, item, dom):
        x1, x2, x3, x4, x5, x6, x7 = item[1: 8]
        info_list_1 = dom.xpath(x1)
        for sub_info in info_list_1:
            l = sub_info.xpath(x2)
            if len(l) == 1:
                k_dom = self.str2dom(etree.tostring(l[0]))
                key = l[0].text
                text_dom = self.str2dom(etree.tostring(sub_info))
                text = text_dom.text.replace(key, '')
                key = key.strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '').replace(u'：', '')
                res[key] = (text, sub_info)
        info_list_2 = dom.xpath(x3)
        res['all_info'] = (self.str2dom(etree.tostring(info_list_2[0])).text, info_list_2[0])

        key = None
        value = ''
        dom_list = []
        for sub_info_list in info_list_2[0].xpath(x4):
            dom2 = self.str2dom(etree.tostring(sub_info_list))
            text = dom2.text.strip()
            if len(text) > 0:
                flag = None
                for s in self.some_key:
                    if s in text.encode('utf8'):
                        flag = self.some_key[s]
                if flag is not None:
                    if key is not None:
                        res[key] = (value, dom_list)
                    value = ''
                    dom_list = []
                    key = flag
                    key = key.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                else:
                    value += text + '\n'
                    dom_list.append(sub_info_list)

        if key is not None:
            res[key] = (value, dom_list)

        dom_resume = dom.xpath(x6)
        if len(dom_resume) == 1:
            res['resume'] = (self.str2dom(etree.tostring(dom_resume[0])).text, dom_resume[0])
        dom_name = dom.xpath(x7)
        if len(dom_name) == 1:
            res['name'] = (self.str2dom(etree.tostring(dom_name[0])).text, dom_name[0])
        dom_info = dom.xpath(x5)
        if len(dom_info) == 1:
            text = self.str2dom(etree.tostring(dom_info[0])).text
            if u'女' in text:
                res['gender'] = (u'女', dom_info[0])
            if u'男' in text:
                res['gender'] = (u'男', dom_info[0])
            if u'博士' in text:
                res['education'] = (u'博士', dom_info[0])
            if u'硕士' in text:
                res['education'] = (u'硕士', dom_info[0])
            
        res_output = {k: v[0] for k, v in res.iteritems()}
        logging.error('get json\t' + json.dumps(res_output, ensure_ascii=False).encode('utf8'))
        logging.error(json.dumps(list(res_output), ensure_ascii=False))
        res['page'] = (response.body, dom)
        return res

    def analy_4_expansion(self, dom, tag, flag):
        ans = []
        for s in dom:
            if type(s) == unicode:
                ans.append([flag, s])
            elif type(s) == bs4.element.Tag:
                if s.name == tag:
                    res = self.analy_4_expansion(s, tag, 1)
                else:
                    res = self.analy_4_expansion(s, tag, flag)
                    if s.name == 'p' and 1 not in [ss[0] for ss in res]:
                        text = s.text.strip()
                        spl = re.split(u'：|:', text)
                        if len(spl) == 2:
                            if ' ' not in spl[0]:
                                res = [[1, spl[0]], [0, spl[1]]]
                ans += [[a[0], a[1], s] if len(a) == 2 else a for a in res]
            elif type(s) == bs4.element.NavigableString:
                ans.append([flag, unicode(s)])
        return ans

    def analy_4(self, res, response, item, dom):
        x1, x2, x3 = item[1: 4]
        info_list_1 = dom.xpath(x1)
        if len(info_list_1) == 1:
            #print res['url']
            #print json.dumps(self.analy_4_expansion(self.str2dom(etree.tostring(info_list_1[0])), x2, 0), ensure_ascii = False)
            ans = self.analy_4_expansion(self.str2dom(etree.tostring(info_list_1[0])), x2, 0)
            ans = [[a[0], a[1], info_list_1[0]] if len(a) == 2 else a for a in ans]

        key = None
        value = ''
        dom_list = []
        for sub_info_list in ans:
            if sub_info_list[0] == 1:
                if key is not None:
                    res[key] = (value, dom_list)
                #print '---', json.dumps(key, ensure_ascii = False).encode('utf8'), json.dumps(value, ensure_ascii = False).encode('utf8')#, json.dumps(dom_list, ensure_ascii = False)
                value = ''
                dom_list = []
                key = sub_info_list[1].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
            else:
                value += sub_info_list[1] + '\n'
                dom_list.append(sub_info_list[2])
        if key is not None:
            res[key] = (value, dom_list)

        dom_name = dom.xpath(x3)
        if len(dom_name) == 1:
            res['name'] = (self.str2dom(etree.tostring(dom_name[0])).text, dom_name[0])
            
        res_output = {k: v[0] for k, v in res.iteritems()}
        logging.error('get json\t' + json.dumps(res_output, ensure_ascii=False).encode('utf8'))
        logging.error(json.dumps(list(res_output), ensure_ascii=False))
        res['page'] = (response.body, dom)
        return res




