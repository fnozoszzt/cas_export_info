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

class choSpider(spiders.MySpider):
    """
    长春人造卫星观测站
    """
    name = 'cho'
    start_urls = ['http://www.cho.cas.cn/kydw/kytd/']
    parse_xpath = './/td[@class="outline_leftlist"]/a'
    expert_list_xpath_list = [['.//td[@width="115"]/a', None]]
    analy_data_conf = [[2, '//td[@class="detail_content"]/table/tr[1]//table/tbody/tr', '//td[@class="detail_content"]/table/tr[2]//td[@height="420"]/table//table']]
