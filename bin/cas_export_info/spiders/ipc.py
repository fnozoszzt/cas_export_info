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

class ipcSpider(spiders.MySpider):
    """
    理化技术研究所
    """
    name = 'ipc'
    start_urls = ['http://www.ipc.cas.cn/rcdw/']
    parse_xpath = './/td[@class="left1"]/table[2]//a'
    expert_list_xpath_list = [['.//div[@class="TRS_Editor"]//a', None], ['.//*[@class="TRS_Editor"]//a', None]]
    analy_data_conf = [[2, '//td[@width="562"]//tr', '//td[@height=420]/table//table']]

