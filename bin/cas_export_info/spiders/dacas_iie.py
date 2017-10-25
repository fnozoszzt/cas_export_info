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

class dacas_iieSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'dacas_iie'
    start_urls = ['http://www.ioa.cas.cn/rcjy/']
    parse_xpath = './/a[@class="b12"]'
    expert_list_xpath_list = [['.//table[@width="95"]//a', './/a'], ['.//*[@class="TRS_Editor"][1]//a', './/a']]
    analy_data_conf = [[5, './/*[@id="zoom"]']]


