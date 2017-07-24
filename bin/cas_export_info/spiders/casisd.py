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

class casisdSpider(spiders.MySpider):
    """
    """
    name = 'casisd'
    start_urls = ['http://www.casisd.cn/zkzj/yjy/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '职称': 'title',
    '学历': 'education',
    '电子邮件': 'email',
    '邮政编码': 'post_code',
    '通讯地址': 'address',
    '电话': 'phone',
    '简历': 'resume',
    '研究方向': 'research_area',
    '专家类别': 'expert_category',
    '研究领域': 'research_field',
    '职务': 'office',
    '承担科研项目情况': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = './/ul[@class="temp01-wrap-Lmenu"]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        expert_list = response.selector.xpath('.//li[@class="col-md-2 col-sm-3 col-xs-4"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        next_page = response.selector.xpath('.//a[@id="pagenav_1"]')
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
        info_list_1 = response.selector.xpath('//li[@class="people-info col-md-4 col-sm-12 col-xs-12"]')
        for sub_info in info_list_1:
            l = sub_info.xpath('strong')
            if len(l) == 1:
                k_dom = self.str2dom(l[0].extract())
                key = k_dom.text
                text_dom = self.str2dom(sub_info.extract())
                text = text_dom.text.replace(key, '')

                key = key.strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '').replace(u'：', '')
                res[key] = text
        info_list_2 = response.selector.xpath('//ul[@class="tem01-people-content"]')
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//h4')
            l2 = sub_info_list.xpath('.//li')
            if len(l) > 0 and len(l2) > 0:
                key = self.str2dom(l[0].extract()).text.strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '').replace(u'：', '')
                value = self.str2dom(l2[0].extract()).text.strip()
                res[key] = value
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
