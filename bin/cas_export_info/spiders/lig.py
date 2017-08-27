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

class ligSpider(spiders.MySpider):
    """
    兰州油气资源研究中心
    """
    name = 'lig'
    start_urls = ['http://www.lig.cas.cn/kydw/zgjgwry/', 'http://www.lig.cas.cn/kydw/fgjgwry/fy/']
    parse_xpath = './/td[@class="leftlink"]//a'
    expert_list_xpath_list = [['.//td[@class="link"]//a', './/a'], ['.//td[@class="hei"]/a[@class="hei"]', './/a']]
    analy_data_conf = [[2, '//table[@class="out12l22"][1]//tr', '//table[@class="out12l22"]//table[@class="out12l22"]//table[@id]']]

