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

class radiSpider(spiders.MySpider):
    """
    遥感与数字地球研究所
    """
    name = 'radi'
    start_urls = ['http://www.radi.cas.cn/rcdw/gcjsgg/zg/', 'http://www.radi.cas.cn/rcdw/kygg/yszj/']
    parse_xpath = './/td[@class="bk3"]//a[@class="hei"]'
    expert_list_xpath_list = [['.//table[@class="bk5"]//a', './/a']]
    analy_data_conf = [[2, '//td[@class="nrhei"]/table[1]//tr', '//td[@class="nrhei"]/table']]

