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

class ibSpider(spiders.MySpider):
    """
    """
    name = 'ib'
    start_urls = ['http://www.ib.cas.cn/duiwu/']
    parse_xpath = './/td[@width="134"]//a'
    expert_list_xpath_list = [['//*[@id="table28"]//a', './/a'], ['//*[@id="listconner"]//table//table//tr/td//a', './/a']]
    analy_data_conf = [[3, './/td[@height="20"]', 'strong', '//div/*[@id="table25"]', './/tr[2]/td//p', './/tr[1]/td/b', './/tr[2]/td//font[1]', '//*[@id="table24"]/tbody/tr[3]/td/p']]
    some_key = {
        '主要研究方向': 'research_area',
        '主要研究工作': 'research_area',
        '研究论文': 'works',
        '代表性论文': 'works',
        '承担的主要科研项': 'research_projects',
    }

