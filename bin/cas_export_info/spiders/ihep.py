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

class ihepSpider(spiders.MySpider):
    """
    高能物理研究所
    """
    name = 'ihep'
    start_urls = ['http://www.ihep.cas.cn/yjdw/']
    parse_xpath = '//*[@id="wholebody"]/table[3]/tr/td[2]/table/tr[3]/td/table/tr/td/a'
    expert_list_xpath_list = [['.//table[@class="zw_link"]//a[@href]', None], ['.//table[@class="blue12"]//a[@href]', './/a']]
    analy_data_conf = [[2, '//*[@id="wholebody"]/table[2]/tr/td[4]/table[2]/tr/td/table[3]/tr/td/table[2]/tbody/tr/td[1]/table/tbody/tr', '//*[@id="wholebody"]/table[2]/tr/td[4]/table[2]/tr/td/table[3]/tr/td/table[3]//table']]
