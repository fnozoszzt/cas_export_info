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

class niaotSpider(spiders.MySpider):
    """
    南京天文光学技术研究所
    """
    name = 'niaot'
    start_urls = ['http://www.niaot.cas.cn/zjdw/yszj/']
    parse_xpath = './/td[@class="table42"]//a'
    expert_list_xpath_list = [['.//table[@width="80%"]//a', './/a']]
    analy_data_conf = [[5, './/td[@height="420"]']]


