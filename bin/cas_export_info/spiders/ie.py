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

class ieSpider(spiders.MySpider):
    """
    微电子研究所
    """
    name = 'ie'
    start_urls = ['http://www.ie.cas.cn/yjdw2016/yszj2016/']
    parse_xpath = './/ul[@id="nav_er"]//a'
    expert_list_xpath_list = [['.//ul[@class="erji_list "]//a', './/div[@class="gl_fenye"]//a']]
    analy_data_conf = [[2, '//table[@id="table21"]//table//table[1]//tr', '//table[@id="table21"]//table//table//table']]

