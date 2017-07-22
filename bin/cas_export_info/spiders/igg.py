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

class iggSpider(spiders.MySpider):
    """
    地质与地球物理研究所
    """
    name = 'igg'
    start_urls = ['http://www.igg.cas.cn/rcjy/fgjgw/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '职称': 'title',
    '学历': 'education',
    'Email': 'email',
    '邮编': 'post_code',
    '地址': 'address',
    '电话': 'phone',
    '简历': 'resume',
    '学科类别': 'subject_category',
    '研究方向': 'research_area',
    '专家类别': 'expert_category',
    '研究领域': 'research_field',
    '职务': 'office',
    '承担科研项目情况': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = './/div[@class="l2tm"]//a|.//div[@class="l2tm1"]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        expert_list = response.selector.xpath('.//table[@class="font03"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        next_page = response.selector.xpath('.//a[@class="h12"]')
        for s in next_page:
            if s.xpath('text()').extract()[0] == u'下一页':
                new_url = s.xpath('@href').extract()[0]
                new_url = urlparse.urljoin(response.url, new_url)
                print new_url
                yield Request(new_url, callback=self.expert_list_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//table[@class="out12l22"][1]//tr')
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
        info_list_2 = response.selector.xpath('//table[@class="out12l22"]//table[@class="out12l22"]//table[@id]')
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//tr')
            text_list = []
            for i in l:
                dom = self.str2dom(i.extract())
                text = dom.text.strip()
                if len(text) > 0:
                    text_list.append(text)
            if len(text_list) == 2:
                key = text_list[0].replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
                value =  text_list[1]
                res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
