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

class ynaoSpider(spiders.MySpider):
    """
    生态环境研究中心
    """
    name = 'ynao'
    start_urls = ['http://www.ynao.cas.cn/kydw/ys/']
    parse_xpath = '//td[@class="outline_left_02"]//a'
    expert_list_exex_js_xpath = ['.//td[@height="26"]//script']
    expert_list_xpath_list = [['.//table[@class="cn75rightkj"]//a', './/a'], ['.//a[@class="hui12s"]', './/a']]
    analy_data_conf = [[2, '//table[@class="hh14"]//tr', None]]
