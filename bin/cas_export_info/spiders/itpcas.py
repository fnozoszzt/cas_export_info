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

class itpcasSpider(spiders.MySpider):
    """
    青藏高原研究所
    """
    name = 'itpcas'
    start_urls = ['http://www.itpcas.cas.cn/yjdw/']
    parse_xpath = './/div[@class="l2tm"]//a'
    expert_list_xpath_list = [['.//a[@class="black13"]', './/a'], ['.//p[@class="cas_content"]//a', './/a']]
    analy_data_conf = [[2, '//table[@class="h12122"]/tr[1]//table//tr', '//table[@class="h12122"]/tr[2]//table//table']]

