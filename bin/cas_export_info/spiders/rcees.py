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

class rceesSpider(spiders.MySpider):
    """
    生态环境研究中心
    """
    name = 'rcees'
    start_urls = ['http://www.rcees.cas.cn/rcjy/']
    parse_xpath = './/a[@class="lmh13"]'
    expert_list_xpath_list = [['.//table[@width="725"]//a', './/a']]
    analy_data_conf = [[2, '//table[@class="out12l22"][1]//tr', '//table[@class="out12l22"]//table']]
        
