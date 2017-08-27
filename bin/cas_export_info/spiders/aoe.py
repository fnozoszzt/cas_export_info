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

class aoeSpider(spiders.MySpider):
    """
    """
    name = 'aoe'
    start_urls = ['http://www.aoe.cas.cn/yjdw/brjh/']
    parse_xpath = './/td[@class="bk_d"]//a'
    expert_list_xpath_list = [['.//*[@class="nrhei"]/table[1]//a', './/a']]

    analy_data_conf = [[2, '//table[@id="table21"]//table//table[1]//tr', '//table[@id="table21"]//table//table//table']]
        
