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

class iggSpider(spiders.MySpider):
    """
    地质与地球物理研究所
    """
    name = 'igg'
    start_urls = ['http://www.igg.cas.cn/rcjy/fgjgw/']
    parse_xpath = './/div[@class="l2tm"]//a|.//div[@class="l2tm1"]//a'
    expert_list_xpath_list = [['.//table[@class="font03"]//a', './/a[@class="h12"]']]
    analy_data_conf = [[2, '//table[@class="out12l22"][1]//tr', '//table[@class="out12l22"]//table[@class="out12l22"]//table[@id]']]
