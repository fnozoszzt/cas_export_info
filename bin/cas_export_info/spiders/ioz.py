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

class iozSpider(spiders.MySpider):
    """
    动物研究所
    """
    name = 'ioz'
    start_urls = ['http://www.ioz.cas.cn/rcjy/']
    parse_xpath = './/a[@class="menu13w"]'
    expert_list_xpath_list = [['.//td[@class="black_14"]//a', './/a[@class="blue12182"]'], ['.//td[@style="background: #f8f8f8;"]//a', './/a[@class="blue12182"]']]
    analy_data_conf = [[2, '//table[@width="540px"]//tr', '//td[@height="420"]//table//table']]

