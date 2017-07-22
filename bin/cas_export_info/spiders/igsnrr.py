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

class igsnrrSpider(spiders.MySpider):
    """
    地理科学与资源研究所
    """
    name = 'igsnrr'
    start_urls = ['http://www.igsnrr.cas.cn/yjdw/yszj/']
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
    parse_xpath = '//table[@class="left-middle01"]//a'
    need_relative_path = False

    def expert_list_parse(self, response):
        """
        """
        logger.debug('expert list page get reponse')
        url = response.url
        last_text = response.meta['text']
        expert_list1 = response.selector.xpath('.//table[@class="black_12"]//a')
        expert_list2 = response.selector.xpath('.//div[@class="TRS_Editor"]//a')
        expert_list3 = response.selector.xpath('.//td[@align="middle"]//a')
        for expert in expert_list1 + expert_list2 + expert_list3:
            href = expert.xpath('@href').extract()[0]
            url = urlparse.urljoin(response.url, href)
            yield Request(url, callback=self.expert_info_parse)
        
    def analy(self, response):
        """
        """
        res = {'url': response.url}
        info_list_1 = response.selector.xpath('//div[@class="style3"]')
        name_dom = self.str2dom(info_list_1.extract()[0])
        res['name'] = name_dom.text
        info_list_2 = response.selector.xpath('//td[@style="padding-left:8px"]/*')
        last = None
        for sub_info_list in info_list_2:
            l = sub_info_list.xpath('.//strong') + sub_info_list.xpath('.//b')
            dom = self.str2dom(sub_info_list.extract())
            text = dom.text.strip()
            if len(l) == 0:
                pass
            else:
                print text

            
            continue
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
        return
        return res
