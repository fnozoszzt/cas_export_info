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

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#logger.setFormat(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class imSpider(spiders.MySpider):
    """
    微生物研究所
    """
    name = 'im'
    start_urls = ['http://www.im.cas.cn/rcdw/qkjj/201507/t20150708_4386927.html']
    parse_xpath = './/a[@class="font01"]'
    expert_list_xpath_list = [['.//table[@style="border-collapse: collapse"]//a', './/a']]
    analy_data_conf = [[5, './/table[width="95%"]'], [5, './/div[@class="m2Con_fck"]']]

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if self.expert_list_xpath_list:
            page = self.exec_js(response.body)
            if 'getScript(\'' in response.body:
                link = response.body.split('getScript(\'')[-1].split('\'')[0]
                yield Request(link, callback=self.expert_info_parse, meta={'text': last_text})
                return
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
                    yield Request(new_url, callback=self.expert_info_parse, meta={'expert_name': self.str2dom(etree.tostring(expert)).text.strip()})
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
