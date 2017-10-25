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

class ieeSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'iee'
    start_urls = ['http://www.iee.cas.cn/rcjy/']
    parse_xpath = './/td[@class="suojin"]//a'
    expert_list_xpath_list = [['.//div[@class="cas_content"]//a', './/a']]
    analy_data_conf = [[6, './/td[@width="580"]//td', './/td[@colspan="2"]', './/b']]


