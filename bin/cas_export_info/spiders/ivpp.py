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

class ivppSpider(spiders.MySpider):
    """
    古脊椎动物与古人类研究所
    """
    name = 'ivpp'
    start_urls = ['http://www.ivpp.cas.cn/kyzc/yjdw/yszj/']
    parse_xpath = './/td[@class="rjlink1"]//a'
    expert_list_xpath_list = [['.//a[@class="t2_link"]', './/a']]
    analy_data_conf = [[2, './/td[@height="188"]//tr', './/table[@class="hh14"]//table[@class="hh14"]']]

