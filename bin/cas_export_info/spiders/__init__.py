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
    高能物理研究所
    """
    name = None
    expert_url = {}
    need_relative_path = True

    parse_xpath = None
    def parse(self, response):
        """
        解析研究团队主页
        """
        logger.debug('main page get reponse')
        expert_cata = response.selector.xpath(self.parse_xpath)
        for cata in expert_cata:
            href = cata.xpath('@href').extract()[0]
            text = cata.xpath('text()').extract()[0]
            logger.debug('main page get cat : %s ; link : %s' % (text, href))
            if not self.need_relative_path or href.startswith('.'):
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_list_parse, meta={'text': text})
            
    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if last_text == u'院士':
            logger.debug('parse ys')
            expert_list = response.selector.xpath('.//div[@class="TRS_Editor"]/table[1]//a[@href]')
            for expert in expert_list:
                name = expert.xpath('text()').extract()[0]
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
                #print name, href
        elif last_text == u'研究团队':
            logger.debug('parse yj')
            expert_list = response.selector.xpath('.//div[@class="Custom_UnionStyle"]//a[@href]')
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
            expert_list = response.selector.xpath('.//div[@class="TRS_Editor"]//a[@href]')
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
        logging.debug('expert info page get reponse')
        url = response.url
        logging.debug('info url : %s' % url)
        if url in self.expert_url:
            logging.debug('url repeat')
            return
        self.expert_url[url] = None
        res = self.analy(response)
        if res is None:
            return
        item = items.CasExportInfoItem()
        item['url'] = res['url']
        for f in self.field_map:
            if f.decode('utf8') in res and res[f.decode('utf8')] != '' and f != '' and self.field_map[f] != '':
                item[self.field_map[f]] = res[f.decode('utf8')]
        #print json.dumps(item, ensure_ascii=False)
        return item
    """
    def analy(self, response)
        res = {}
        if 'sourcedb.itp.cas.cn/zw/zjrck/' in url or 'sourcedb.cas.cn/sourcedb_itp_cas/zw/zjrck/' in url:
            info_list_1 = response.selector.xpath('.//table[@width="710"]//table[@width="465"]')
            #print info_list_1
            for sub_info_list in info_list_1.xpath('.//tr'):

                l = sub_info_list.xpath('td')
                if len(l) % 2 == 0:
                    for i in range(0, len(l), 2):
                        key = bs4.BeautifulSoup(l[i].extract()).text.replace(u'：', '').strip()
                        value =  bs4.BeautifulSoup(l[i + 1].extract()).text.strip()
                        res[key] = value
            info_list_2 = response.selector.xpath('.//table[@width="710"]//table[@id]')
            for sub_info_list in info_list_2:
                l = sub_info_list.xpath('.//tr')
                if len(l) == 2:
                    key = bs4.BeautifulSoup(l[0].extract()).text.replace(u'：', '').strip()
                    value =  bs4.BeautifulSoup(l[1].extract()).text.strip()
                    res[key] = value
            #logger.debug('output json : %s' % json.dumps(res, ensure_ascii=False))
            item = items.CasExportInfoItem()
            for f in self.field_map:
                if f.decode('utf8') in res and res[f.decode('utf8')] != '' and f != '' and self.field_map[f] != '':
                    item[self.field_map[f]] = res[f.decode('utf8')]
            #print json.dumps(item, ensure_ascii=False)
            return item
        else:
            #print url
            pass
            
                name_list = expert.xpath('text()').extract()
                href_list = expert.xpath('@href').extract()
                if len(name_list) > 0 and len(href_list) > 0:
                    name = name_list[0]
                    href = href_list[0]
                else:
                    name_list = expert.xpath('.//font/text()').extract()
                    href_list = expert.xpath('@href').extract()
                """
