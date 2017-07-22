# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CasExportInfoPipeline(object):
    field_map = [
    ['url', 'url'],
    ['name', '姓名'],
    ['gender', '性别'],
    ['expert_category', '专家类别'],
    ['subject_category', '学科类别'],
    ['office', '职务'],
    ['title', '职称'],
    ['education', '学历'],
    ['address', '通讯地址'],
    ['post_code', '邮编'],
    ['phone', '电话'],
    ['email', '电子邮箱'],
    ['resume', '简历'],
    ['research_field', '研究领域'],
    ['research_area', '研究方向'],
    ['works', '代表论著'],
    ['research_projects', '承担科研项目情况']
    ]

    institute_name_map = {
    'ihep': '高能物理研究所',
    'imech': '力学研究所',
    'ioa': '声学研究所',
    'ipc': '理化技术研究所',
    'nanoctr': '国家纳米科学中心',
    'rcees': '生态环境研究中心',
    'itp': '理论物理研究所',
    'ynao': '云南天文台',
    'nao': '国家天文台',
    'cho': '长春人造卫星观测站',
    'radi': '遥感与数字地球研究所',
    'igg': '地质与地球物理研究所',
    'lig': '兰州油气资源研究中心',
    'itpcas': '青藏高原研究所',
    'iap': '大气物理研究所',
    'ioz': '动物研究所',
    'psych': '心理研究所',
    'genetics': '遗传与发育生物学研究所',
    'ime': '中国科学院微电子研究所',
    'ie': '中国科学院电子学研究所',
    'aoe': '中科院光电研究院',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': ''
    }


    def process_item(self, item, spider):
        name = spider.name
        print item
        res = [self.institute_name_map[name].decode('utf8')]
        if not hasattr(self, name):
            #self.name = open('output_' + name, 'w')
            setattr(self, name, open('output_' + name, 'w'))
        #for a, b in self.field_map:
        #    res.append
        #print item
        if 'name' not in item:
            return
        item['name'] = item['name'].replace(' ', '')
        for a, b in self.field_map:
            if a in item:
                res.append(item[a].replace('\n', '').replace('\t', '').replace('\r', ''))
                #print ',,', a
            else:
                res.append(u'')
        print >>getattr(self, name), (u'\t'.join(res)).encode('utf8')
        return item
