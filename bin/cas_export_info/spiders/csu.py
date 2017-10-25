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

class csuSpider(spiders.MySpider):
    """
    声学研究所
    """
    name = 'csu'
    start_urls = ['http://www.csu.cas.cn/yjdw/yjy/']
    parse_xpath = './/table[@background="../../images/csu_cdh_02.gif"]//a'
    expert_list_xpath_list = [['.//td[@class="bk1"]//table//table[1]//a', './/a']]
    analy_data_conf = [[7, './/div[@class="cas_content"]/table//tr', './/div[@class="cas_content"]/p'], [7, './/td[@class="nrhei"]/table//tr', './/div[@class="cas_content"]/p']]


