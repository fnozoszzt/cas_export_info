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

class sxiccSpider(spiders.MySpider):
    """
    """
    name = 'sxicc'
    start_urls = ['http://www.sxicc.cas.cn/yjdw/jcqn/']
    parse_xpath = '//table[@width="220"]//a'
    expert_list_xpath_list = [['//table[@width="97%"]//a', './/a']]
    analy_data_conf = [[2, './/table[@height="167"]//tr', './/table[@class="hh14"]']]
