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

class ihepSpider(spiders.MySpider):
    """
    """
    name = 'sjziam'
    start_urls = ['http://www.sjziam.cas.cn/yjdw/yszjyjdw/']
    parse_xpath = './/td[@class="jggk_list outline_leftlist"]//a'
    expert_list_xpath_list = [['.//td[@class="news_img"]//a', './/a']]
    analy_data_conf = [[2, '//td[@height="188"]//tr', './/td[@height="420"]//table//table']]
