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
    field_map = {
    'name': 'name',
    '性别': 'gender',
    '职称': 'title',
    '学历': 'education',
    'email': 'email',
    '邮编': 'post_code',
    '通讯地址': 'address',
    '联系电话': 'phone',
    'resume': 'resume',
    '研究方向': 'research_area',
    '专家类别': 'expert_category',
    '研究领域': 'research_field',
    '职务': 'office',
    '承担科研项目情况': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = './/a[@class="CurrChnlCls"]'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        expert_list = response.selector.xpath('.//a[@class="t2_link"]')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        next_page = response.selector.xpath('.//a[@class="blue12182"]')
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
        name = response.selector.xpath('//h1/text()').extract()[0]
        res['name'] = name
        info_list_1 = response.selector.xpath('//td[@class="people_intro"]//div[@id]')
        email_text = response.selector.xpath('//div[@id="dzyj"]//script/text()').extract()[0]
        email = email_text.split('="')[1].split('"')[0]
        res['email'] = email
        for sub_info in info_list_1:
            title = self.str2dom(sub_info.xpath('.//strong').extract()[0]).text
            text = self.str2dom(sub_info.extract()).text
            text = text.replace(title, '')
            text_list = []
            title = title.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '').replace(u'　', '')
            res[title] = text
        info_list_2 = response.selector.xpath('//td[@class="people_intro"]//div')
        text_list = []
        for sub_info_list in info_list_2:
            if len(sub_info_list.xpath('@id')) > 0:
                continue
            dom = self.str2dom(sub_info_list.extract())
            text_list.append(dom.text)
        res['resume'] = text_list[0]
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return res
