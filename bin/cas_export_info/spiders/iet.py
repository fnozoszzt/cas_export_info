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

class ietSpider(spiders.MySpider):
    """
    """
    name = 'iet'
    start_urls = ['http://www.iet.cas.cn/kydw/ys/']
    parse_xpath = '//td[@class="outline_leftlist_wrap"]//a'
    expert_list_xpath_list = [['//td[@width="150"]//a', './/a']]
    analy_data_conf = [[2, './/td[@height="188"]//tr', './/td[@width="420"]//table//table']]
