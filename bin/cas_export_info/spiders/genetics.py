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

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#logger.setFormat(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class geneticsSpider(spiders.MySpider):
    """
    遗传与发育生物学研究所
    """
    name = 'genetics'
    start_urls = ['http://www.genetics.cas.cn/rcjy/']
    parse_xpath = './/a[@class="CurrChnlCls"]'
    expert_list_xpath_list = [['.//a[@class="t2_link"]', './/a']]
        
    def analy(self, response):
        """
        """
        res = {'url': (response.url, '')}
        name = response.selector.xpath('//h1/text()').extract()[0]
        res['name'] = (name, '')
        info_list_1 = response.selector.xpath('//td[@class="people_intro"]//div[@id]')
        email_text = response.selector.xpath('//div[@id="dzyj"]//script/text()').extract()[0]
        email = email_text.split('="')[1].split('"')[0]
        res['email'] = (email, '')
        for sub_info in info_list_1:
            title = self.str2dom(sub_info.xpath('.//strong').extract()[0]).text
            text = self.str2dom(sub_info.extract()).text
            text = text.replace(title, '')
            text_list = []
            title = title.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
            res[title] = (text, '')
        info_list_2 = response.selector.xpath('//td[@class="people_intro"]//div')
        text_list = []
        for sub_info_list in info_list_2:
            if len(sub_info_list.xpath('@id')) > 0:
                continue
            dom = self.str2dom(sub_info_list.extract())
            text_list.append(dom.text)
        res['resume'] = (text_list[0], '')
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res, ''
