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

class ipeSpider(spiders.MySpider):
    """
    过程工程研究所
    """
    name = 'ipe'
    start_urls = ['http://www.ipe.cas.cn/rcjy/yjdwgsh/']
    field_map = {
    '姓名': 'name',
    '性别': 'gender',
    '职称': 'title',
    '学历': 'education',
    'Email': 'email',
    '地址': 'address',
    '电话': 'phone',
    '简历': 'resume',
    '研究方向': 'research_area',
    '专家类别': 'expert_category',
    '研究领域': 'research_field',
    '职务': 'office',
    '承担科研项目情况': 'research_projects',
    '代表论著': 'works'
    }
    parse_xpath = './/a[@class="menu13w"]'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        expert_list = response.selector.xpath('.//*[@class="TRS_Editor"]//a')
        for expert in expert_list:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//table[@height="184"]//tr')
        for sub_info in info_list_1:
            l = sub_info.xpath('td')
            if len(l) % 2 == 0:
                for i in range(0, len(l), 2):
                    k_dom = self.str2dom(l[i].extract())
                    key = k_dom.text.replace(u'：', '').strip().replace(' ', '').replace(':', '').replace(u'\xa0', '')
                    v_dom = self.str2dom(l[i + 1].extract())
                    value = v_dom.text.strip()
                    res[key] = value
        info_list_2 = response.selector.xpath('//td[@id="td0"]//p')
        last = 'resume'
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//b').extract()
            text = self.str2dom(sub_info_list.extract()).text.strip()

            if len(l) == 0:
                print '!!', last, text
            else:
                text = text.replace(u'：', '').strip().replace(' ', '').replace(':', '')
                print '###', text
                if text.encode('utf8') in self.field_map:
                    last = self.field_map[text.encode('utf8')]
                else:
                    last = None
        logging.error('get json\t' + json.dumps(res, ensure_ascii=False).encode('utf8'))
        return None
        return res
