#coding:utf8
"""
author:fnozoszzt@gmail.com
"""
import sys
sys.path.append('cas_export_info')
import spiders
import logging
import urlparse
from scrapy.http import Request
import json
import bs4
from lxml import etree
from cas_export_info import items

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#logger.setFormat(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class iopSpider(spiders.MySpider):
    """
    微生物研究所
    """
    name = 'iop'
    start_urls = ['http://www.iop.cas.cn/rcjy/yszj/']
    parse_xpath = './/div[@id="box_side"]//a'
    expert_list_xpath_list = [['.//a', './/a']]
    analy_data_conf = [[3, None, None, './/body', '*', None, None, None]]
    some_key = {
        '简介': 'resume',
        '主要研究方向': 'research_area',
        '代表性论文及专利': 'works',
        '电话': 'phone',
        'Email': 'email',
    }

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if self.expert_list_xpath_list:
            page = self.exec_js(response.body)
            if 'getScript(\'' in response.body:
                link = response.body.split('getScript(\'')[1].split('\'')[0]
                yield Request(link, callback=self.expert_list_parse, meta={'text': last_text, 'flag': True})
                return
            if 'flag' not in response.meta:
                return
            dom = etree.HTML(page, parser=etree.HTMLParser(encoding='utf-8'))
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
                    yield Request(new_url, callback=self.expert_info_parse, meta={'expert_name': self.str2dom(etree.tostring(expert)).text.strip()})
                if next_page_xpath:
                    next_page = dom.xpath(next_page_xpath)
                    for s in next_page:
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
