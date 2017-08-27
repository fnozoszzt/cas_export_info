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

class igsnrrSpider(spiders.MySpider):
    """
    地理科学与资源研究所
    """
    name = 'igsnrr'
    start_urls = ['http://www.igsnrr.cas.cn/yjdw/yszj/']
    parse_xpath = '//table[@class="left-middle01"]//a'
    expert_list_xpath_list = [['.//table[@class="black_12"]//a', './/a'], ['.//div[@class="TRS_Editor"]//a', './/a'], ['.//td[@align="middle"]//a', './/a']]
    analy_data_conf = [[4, './/table[@class="bg"]', 'strong', './/div[@class="style3"]']]
