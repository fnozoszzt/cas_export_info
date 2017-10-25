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

class semiSpider(spiders.MySpider):
    """
    """
    name = 'semi'
    start_urls = ['http://sourcedb.semi.cas.cn/zw/rczj/yszj/']
    parse_xpath = './/li[@id="subnav"]//a'
    expert_list_xpath_list = [['.//li[@class="news_list"]//a', './/a']]
    analy_data_conf = [[5, './/div[@class="article-body"]']]


