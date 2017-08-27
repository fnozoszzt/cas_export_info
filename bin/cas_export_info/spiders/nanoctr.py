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

class nanoctrSpider(spiders.MySpider):
    """
    国家纳米科学中心
    """
    name = 'nanoctr'
    start_urls = ['http://www.nanoctr.cas.cn/yjdw/brjh/']
    parse_xpath = './/a[@class="w12l20"]'
    expert_list_xpath_list = [['.//div[@class="TRS_Editor"]//a', './/a']]
    analy_data_conf = [[2, '//td[@width="562"]//tr', '//td[@height=420]/table//table']]

