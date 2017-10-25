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

class ihnsSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'ihns'
    start_urls = ['http://www.ihns.cas.cn/yjdw_new/']
    parse_xpath = './/ul[@class="chennal"]//a'
    expert_list_xpath_list = [['.//table[@width="670"]//a', './/a']]
    analy_data_conf = [[3, None, None, './/td[@width="730px"]', './/p', None, None, './/ul[@class="second_title"]']]
    some_key = {
        '研究方向': 'research_area',
        '工作经历': 'resume',
        '论著目录': 'works',
        '联系方式': 'address',
    }


