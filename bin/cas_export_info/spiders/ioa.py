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

class ioaSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'ioa'
    start_urls = ['http://www.ioa.cas.cn/rcjy/']
    field_map = {
    '姓名': 'name',
    'resume': 'resume'
    }
    parse_xpath = './/a[@class="b12"]'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if u'院士' in last_text:
            logger.debug('parse ys')
            expert_list = response.selector.xpath('.//table[@width="95"]//a')
            for expert in expert_list:
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        else:
            logger.debug('parse other')
            expert_list = response.selector.xpath('.//*[@class="TRS_Editor"][1]//a')
            for expert in expert_list:
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//tr[@height=41][1]')
        l = info_list_1.xpath('td')
        if len(l) % 2 == 0:
            for i in range(0, len(l), 2):
                k_dom = self.str2dom(l[i].extract())
                key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '')
                v_dom = self.str2dom(l[i + 1].extract())
                value = v_dom.text.strip()
                res[key] = value
        resume_list = response.selector.xpath('//tr[@height="40"]')
        resume = ""
        for sub_info_list in resume_list:
            l = sub_info_list.xpath('.//td')
            text_list = []
            for i in l:
                dom = self.str2dom(i.extract())
                text = dom.text.strip()
                if len(text) > 0:
                    text_list.append(text)
            if len(text_list) == 3:
                #key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '')
                #value =  text_list[1]
                #res[key] = value
                resume += text_list[0] + ' - ' + text_list[1] + ' : ' + text_list[2] + ';'
        res['resume'] = resume
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
