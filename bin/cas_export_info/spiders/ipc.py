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

class ipcSpider(spiders.MySpider):
    """
    理化技术研究所
    """
    name = 'ipc'
    start_urls = ['http://www.ipc.cas.cn/rcdw/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '职务': 'office',
    '职称': 'title',
    '学历': 'education',
    '电子邮件': 'email',
    '邮政编码': 'post_code',
    '通讯地址': 'address',
    '电话': 'phone',
    '简历': 'resume',
    '研究领域': 'research_field',
    '代表论著': 'works'
    }
    parse_xpath = './/td[@class="left1"]/table[2]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        if u'院士' in last_text:
            logger.debug('parse ys')
            expert_list = response.selector.xpath('.//div[@class="TRS_Editor"]//a')
            for expert in expert_list:
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        else:
            logger.debug('parse other')
            expert_list = response.selector.xpath('.//*[@class="TRS_Editor"]//a')
            for expert in expert_list:
                href = expert.xpath('@href').extract()[0]
                url = urlparse.urljoin(response.url, href)
                yield Request(url, callback=self.expert_info_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//td[@width="562"]//tr')
        l = info_list_1.xpath('td')
        if len(l) % 2 == 0:
            for i in range(0, len(l), 2):
                k_dom = self.str2dom(l[i].extract())
                key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
                v_dom = self.str2dom(l[i + 1].extract())
                value = v_dom.text.strip()
                res[key] = value
        info_list_2 = response.selector.xpath('//td[@height=420]/table//table')
        print info_list_2
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//tr')
            text_list = []
            for i in l:
                dom = self.str2dom(i.extract())
                text = dom.text.strip()
                if len(text) > 0:
                    text_list.append(text)
            if len(text_list) == 2:
                key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '')
                value =  text_list[1]
                res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res 
