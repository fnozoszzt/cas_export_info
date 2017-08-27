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

class iaSpider(spiders.MySpider):
    """
    """
    name = 'ia'
    start_urls = ['http://www.ia.cas.cn/rcjy/brjh/']
    parse_xpath = '//ul[@class="column-list"]//a'
    expert_list_xpath_list = [['//h5//a', './/a']]
    analy_data_conf = [[2, './/table[@width="724"]//table[1]//tr', './/table[@width="724"]//table[2]//table']]
