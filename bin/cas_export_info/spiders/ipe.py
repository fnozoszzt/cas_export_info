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

class ipeSpider(spiders.MySpider):
    """
    过程工程研究所
    """
    name = 'ipe'
    start_urls = ['http://www.ipe.cas.cn/rcjy/yjdwgsh/']
    parse_xpath = './/a[@class="menu13w"]'
    expert_list_xpath_list = [['.//*[@class="TRS_Editor"]//a', None]]
    analy_data_conf = [[2, '//table[@height="184"]//tr', '//td[@id="td0"]//p']]
