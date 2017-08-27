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

class naoSpider(spiders.MySpider):
    """
    国家天文台
    """
    name = 'nao'
    start_urls = ['http://www.nao.cas.cn/yjdw/']
    parse_xpath = './/ul[@id="column2"]//a'
    expert_list_xpath_list = [['.//div[@id="expertlist"]//a', './/a']]
    analy_data_conf = [[1, '//li[@class="people-info col-md-4 col-sm-12 col-xs-12"]', 'strong', '//ul[@class="tem01-people-content"]', 'h4', 'li']]

