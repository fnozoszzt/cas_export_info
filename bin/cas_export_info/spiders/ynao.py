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

class ynaoSpider(spiders.MySpider):
    """
    生态环境研究中心
    """
    name = 'ynao'
    start_urls = ['http://www.ynao.cas.cn/kydw/ys/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '职称': 'title',
    '学历': 'education',
    '电子邮件': 'email',
    '通讯地址': 'address',
    '电话': 'phone',
    '简历': 'resume',
    '研究方向': 'research_area',
    '专家类别': 'expert_category',
    '研究领域': 'research_field',
    '职务': 'office',
    '承担科研项目': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = '//td[@class="outline_left_02"]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        expert_list = response.selector.xpath('.//table[@class="cn75rightkj"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        expert_list = response.selector.xpath('.//td[@height="26"]//script')
        for expert in expert_list:
            text = expert.extract()
            href = text.split('href=\'')[-1].split('\'')[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        if 'turn_flag' not in response.meta:
            turn_page = response.selector.xpath('.//a[@class="h12"]')
            for s in turn_page:
                import re
                href = s.xpath('@href').extract()
                m = re.match(u'(\d+)', s.xpath('text()').extract()[0])
                if m and len(href) > 0:
                    new_url = urlparse.urljoin(response.url, href[0])
                    yield Request(new_url, callback=self.expert_list_parse, meta={'turn_flag': True})
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//table[@class="hh14"]//tr')
        for sub_info in info_list_1:
            l = sub_info.xpath('td')
            if len(l) % 2 == 1:
                l = l[:-1]
            if len(l) % 2 == 0:
                for i in range(0, len(l), 2):
                    k_dom = self.str2dom(l[i].extract())
                    key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
                    v_dom = self.str2dom(l[i + 1].extract())
                    value = v_dom.text.strip()
                    res[key] = value
        """
        info_list_2 = response.selector.xpath('//table[@class="out12l22"]//table')
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
        """
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
