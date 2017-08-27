#coding:utf8
"""
author:fnozoszzt@gmail.com
"""
import sys
sys.path.append('cas_export_info')
import spiders
import logging
import bs4
import json

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#logger.setFormat(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class itpSpider(spiders.MySpider):
    """
    理论物理研究所
    """
    name = 'itp'
    start_urls = ['http://www.itp.cas.cn/rcjy/']
    parse_xpath = './/div[@class="l2tm"]/a'
    expert_list_xpath_list = [['.//div[@class="TRS_Editor"]/table[1]//a[@href]', './/a'], ['.//div[@class="Custom_UnionStyle"]//a[@href]', './/a'], ['.//div[@class="TRS_Editor"]//a[@href]', './/a']]
    analy_data_conf = [[2, './/table[@width="710"]//table[@width="465"]//tr', './/table[@width="710"]//table[@id]']]

