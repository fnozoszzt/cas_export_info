# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CasExportInfoItem(scrapy.Item):
    # define the fields for your item here like:

    # url
    url = scrapy.Field()
    # 研究所
    institute = scrapy.Field()
    # 姓名
    name = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 专家类别
    expert_category = scrapy.Field()
    # 学科类别
    subject_category = scrapy.Field()
    # 职务
    office = scrapy.Field()
    # 职称
    title = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 通讯地址
    address = scrapy.Field()
    # 邮编
    post_code = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # 电子邮箱
    email = scrapy.Field()
    # 简历
    resume = scrapy.Field()
    # 研究领域
    research_field = scrapy.Field()
    # 研究方向
    research_area = scrapy.Field()
    # 代表论著
    works = scrapy.Field()
    # 承担科研项目情况
    research_projects = scrapy.Field()

