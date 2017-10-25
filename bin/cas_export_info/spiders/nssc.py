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

class nsscSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'nssc'
    start_urls = ['http://www.nssc.cas.cn/rcdw2015/lyys2015/']
    parse_xpath = './/ul[@id="erji-nav"]//a'
    expert_list_xpath_list = [['.//ul[@class="erji-tupianlist"]//a', './/a']]
    analy_data_conf = [[2, None, './/td[@height="420"]//table//table']]


