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

class tibSpider(spiders.MySpider):
    """
    """
    name = 'tib'
    start_urls = ['http://www.tib.cas.cn/kydw/fyjy/']
    parse_xpath = './/div[@class="l2tm"]//a'
    expert_list_xpath_list = [['.//table[@class="black_12"]//a', './/a']]
    analy_data_conf = [[2, '//td[@height="188"]/table//tr', '//td[@height="420"]/table//table']]

