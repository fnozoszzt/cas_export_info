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

class ucasSpider(spiders.MySpider):
    """
    """
    name = 'ucas'
    start_urls = ['http://www.gucas.ac.cn/site/74']
    parse_xpath = '//div[@class="menuTitle"]//a'
    expert_list_xpath_list = [['//div[@class="yp_ity"]//a', './/a']]
    analy_data_conf = [[6, './/div[@class="bp-enty"]/text()', './/div[@class="m-itme"]', 'h3']]
