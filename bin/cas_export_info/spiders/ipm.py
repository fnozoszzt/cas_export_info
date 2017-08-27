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

class ipmSpider(spiders.MySpider):
    """
    """
    name = 'ipm'
    start_urls = ['http://www.casisd.cn/zkzj/tpzkzj/']
    parse_xpath = './/ul[@class="temp01-wrap-Lmenu"]//a'
    expert_list_xpath_list = [['//li[@class="col-md-2 col-sm-3 col-xs-4"]//a', './/a']]
    analy_data_conf = [[1, './/li[@class="people-info col-md-4 col-sm-12 col-xs-12"]', 'strong', './/div[@class="col-md-12 tem01-people-content"]/ul', 'h4', 'li']]
