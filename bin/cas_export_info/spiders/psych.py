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

class psychSpider(spiders.MySpider):
    """
    心理研究所
    """
    name = 'psych'
    start_urls = ['http://www.psych.cas.cn/yjdw/kezuoyjy/']
    parse_xpath = './/td[@width="194"]//a'
    expert_list_frame_xpath = True
    expert_list_xpath_list = [['.//td[@height="26"]//a', './/a'], ['.//td[@style="background: #f8f8f8;"]//a', './/a']]
    #analy_data_conf = [[2, '//table[@class="hh14"]//tr', '//table[@class="hh14"][position()>2]'], [2, '', '']]

    '''
    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        expert_list = response.selector.xpath('.//td[@height="26"]//a') + response.selector.xpath('.//td[@style="background: #f8f8f8;"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        next_page = response.selector.xpath('.//a[@class="fy"]')
        for s in next_page:
            if s.xpath('text()').extract()[0] == u'下一页':
                new_url = s.xpath('@href').extract()[0]
                new_url = urlparse.urljoin(response.url, new_url)
                print new_url
                yield Request(new_url, callback=self.expert_list_parse)
        iframe_list = response.xpath('//iframe')
        for iframe in iframe_list:
            href = iframe.xpath('@src').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_list_parse)
        
    '''
    def analy(self, response):
        """
        """
        res = {'url': (response.url, '')}
        if not '助研个人网页' in response.body:
            info_list_1 = response.selector.xpath('//table[@class="hh14"]//tr')
            if len(info_list_1) == 0:
                return None, None
            name = self.str2dom(info_list_1[0].extract()).text
            res[u'姓名'] = (name, '')
            for s in info_list_1[1:]:
                text = self.str2dom(s.extract()).text
                ar = text.split(':')
                if len(ar) == 2:
                    key = ar[0].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                    value = ar[1]
                    res[key] = (value, '')
            info_list_2 = response.selector.xpath('//table[@class="hh14"][position()>2]')
            for sub_info_list in info_list_2:
                l = sub_info_list.xpath('.//tr')
                text_list = []
                for i in l:
                    dom = self.str2dom(i.extract())
                    text = dom.text.strip()
                    if len(text) > 0:
                        text_list.append(text)
                if len(text_list) == 2:
                    key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                    value =  text_list[1]
                    res[key] = (value, '')
        else:
            info_list_1 = response.selector.xpath('//table[@class="hh14"]//tr')
            for sub_info in info_list_1:
                l = sub_info.xpath('td')
                if len(l) % 2 == 1:
                    l = l[:-1]
                if len(l) % 2 == 0:
                    for i in range(0, len(l), 2):
                        k_dom = self.str2dom(l[i].extract())
                        key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                        v_dom = self.str2dom(l[i + 1].extract())
                        value = v_dom.text.strip()
                        res[key] = (value, '')
            info_list_2 = response.selector.xpath('//table[@class="hh14"]/tbody/tr/td/span/font/p')
            for sub_info_list in info_list_2:
                if len(sub_info_list.xpath('.//strong')) == 0:
                    continue
                title = self.str2dom(sub_info_list.xpath('.//strong').extract()[0]).text
                text = self.str2dom(sub_info_list.extract()).text
                text = text.replace(title, '')
                text_list = []
                title = title.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
                res[title] = (text, '')
            #for i in l:
            #    dom = self.str2dom(i.extract())
            #    text = dom.text.strip()
            #    if len(text) > 0:
            #        text_list.append(text)
            #if len(text_list) == 2:
            #    key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
            #    value =  text_list[1]
            #    res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res, None
