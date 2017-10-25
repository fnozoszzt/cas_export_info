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

class ibpSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'ibp'
    start_urls = ['http://www.ibp.cas.cn/kydw/cjxz/']
    parse_xpath = './/a[@class="white12"]'
    expert_list_xpath_list = [['.//*[@class="TRS_Editor"]//a', './/a']]
    analy_data_conf = [[5, './/*[@class="TRS_Editor"]']]


