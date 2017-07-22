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

class naoSpider(spiders.MySpider):
    """
    国家天文台
    """
    name = 'nao'
    start_urls = ['http://www.nao.cas.cn/yjdw/']
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
    '社会任职': 'office',
    '承担科研项目情况': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = './/ul[@id="column2"]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        expert_list = response.selector.xpath('.//div[@id="expertlist"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//li[@class="people-info col-md-4 col-sm-12 col-xs-12"]')
        for sub_info in info_list_1:
            k_dom = self.str2dom(sub_info.xpath('strong').extract()[0])
            key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
            #v_dom = self.str2dom(sub_info.xpath('text()').extract())
            #value = v_dom.text.strip()
            value = sub_info.xpath('text()').extract()[0].strip()
            res[key] = value
        info_list_2 = response.selector.xpath('//ul[@class="tem01-people-content"]')
        for sub_info_list in info_list_2:
            k_dom = self.str2dom(sub_info_list.xpath('.//h4').extract()[0])
            key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
            #value = sub_info_list.xpath('li').extract()[0].strip()
            v_dom = self.str2dom(sub_info_list.extract())
            value = v_dom.text.strip()
            res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
