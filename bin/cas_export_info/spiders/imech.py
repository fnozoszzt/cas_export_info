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

class imechSpider(spiders.MySpider):
    """
    力学研究所
    """
    name = 'imech'
    start_urls = ['http://www.imech.cas.cn/kydw/zgjgwry/']
    #parse_xpath = '/html/body/table[4]/tr/td[1]/table/tr[2]/td/table/tr[2]/td/table/tr/td/table/tr/td[3]/a'
    parse_xpath = './/div[@class="left_nav"]//li/a'
    #parse_xpath = './/a[@class="hei2"]'
    #expert_list_xpath_list = [['.//a[@class="hei2 expe"]', './/td[@class="nrhei"]']]
    expert_list_xpath_list = [['.//a', None]]
    analy_data_conf = [[1, './/div[@class="col-md-10 col-sm-8 col-xs-6"]//li', './/strong', './/div[@class="col-md-12 tem01-people-content"]/ul', 'h4', 'li']]


