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

class imeSpider(spiders.MySpider):
    """
    微电子研究所
    """
    name = 'ime'
    start_urls = ['http://www.ime.cas.cn/rcjy/yszj/']
    parse_xpath = './/a[@class="yj"]'
    expert_list_xpath_list = [['.//table[@width="96%"]//a', './/a']]
    analy_data_conf = [[2, '//table[@class="font03 tablestyle"]//tr', '//table[@class="font03"]//table[@class="font03"]']]

