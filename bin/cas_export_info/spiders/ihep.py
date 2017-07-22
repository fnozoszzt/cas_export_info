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

class ihepSpider(spiders.MySpider):
    """
    高能物理研究所
    """
    name = 'ihep'
    start_urls = ['http://www.ihep.cas.cn/yjdw/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '学历': 'education',
    'Email': 'email',
    '邮编': 'post_code',
    '地址': 'address',
    '简历介绍': 'resume',
    '专家类别': 'expert_category',
    '社会任职': 'office',
    '研究方向': 'research_area',
    '承担科研项目情况': 'research_projects',
    '类别': 'expert_category'
    }
    parse_xpath = '//*[@id="wholebody"]/table[3]/tr/td[2]/table/tr[3]/td/table/tr/td/a'

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if last_text == u'院士专家':
            logger.debug('parse ys')
            expert_list = response.selector.xpath('.//table[@class="zw_link"]//a[@href]')
            for expert in expert_list:
                #name = expert.xpath('strong/text()').extract()[0]
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        else:
            logger.debug('parse other')
            expert_list = response.selector.xpath('.//table[@class="blue12"]//a[@href]')
            num_text = response.selector.xpath('.//table[@class="h12"]//td[1]/text()').extract()[0]
            import re
            m = re.search(u'共(\d+)页', num_text)
            if m:
                num = int(m.group(1))
            else:
                num = 0
            for expert in expert_list:
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse, meta={'text': last_text})
            if 'turn_flag' not in response.meta:
                for i in range(1, num):
                    new_url = 'http://www.ihep.cas.cn/yjdw/zgjgwry/index_%d.html' % i
                    yield Request(new_url, callback=self.expert_list_parse, meta={'turn_flag': True, 'text': last_text})
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//*[@id="wholebody"]/table[2]/tr/td[4]/table[2]/tr/td/table[3]/tr/td/table[2]/tbody/tr/td[1]/table')
        for sub_info_list in info_list_1.xpath('.//tr'):
            l = sub_info_list.xpath('td')
            if len(l) % 2 == 0:
                for i in range(0, len(l), 2):
                    k_dom = self.str2dom(l[i].extract())
                    key = k_dom.text.replace(u'：', '').strip()
                    v_dom = self.str2dom(l[i + 1].extract())
                    value = v_dom.text.strip()
                    res[key] = value
        info_list_2 = response.selector.xpath('//*[@id="wholebody"]/table[2]/tr/td[4]/table[2]/tr/td/table[3]/tr/td/table[3]//table')
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//tr')
            text_list = []
            for i in l:
                dom = self.str2dom(i.extract())
                text = dom.text.strip()
                if len(text) > 0:
                    text_list.append(text)
            if len(text_list) == 2:
                key = text_list[0].replace(u'：', '').strip()
                value =  text_list[1]
                res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        #return None
        return res 
