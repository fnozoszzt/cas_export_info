# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class CasExportInfoPipeline(object):
    field_map = [
    ['url', 'url'],
    ['code', '单位代码'],
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
    ['all_info', '全部简历信息'],
    ['resume', '简历'],
    ['research_field', '研究领域'],
    ['research_area', '研究方向'],
    ['works', '代表论著'],
    ['research_projects', '承担科研项目情况'],
    ['page', '网页']
    ]

    institute_name_map = {
    'ihep': '中国科学院高能物理研究所',
    'imech': '中国科学院力学研究所',
    'ipc': '中国科学院理化技术研究所',
    'nanoctr': '国家纳米科学中心',
    'rcees': '中国科学院生态环境研究中心',
    'itp': '中国科学院理论物理研究所',
    'ynao': '中科院云南天文台',
    'nao': '中国科学院国家天文台',
    'cho': '中国科学院国家天文台长春人造卫星观测站',
    'radi': '中国科学院遥感与数字地球研究所',
    'igg': '中国科学院地质与地球物理研究所',
    'lig': '中国科学院地质与地球物理研究所兰州油气资源研究中心',
    'itpcas': '中国科学院青藏高原研究所',
    'iap': '中国科学院大气物理研究所',
    'ioz': '中国科学院动物研究所',
    'psych': '中国科学院心理研究所', #两种网页, analy not new
    'genetics': '中国科学院遗传与发育生物学研究所',   # analy not new
    'ime': '中国科学院微电子研究所',
    'ie': '中国科学院电子学研究所',
    'aoe': '中科院光电研究院',
    'casisd': '中国科学院科技战略咨询研究院',
    'tib': '中国科学院天津工业生物技术研究所',
    'ib': '中国科学院植物研究所', #with risk
    'igsnrr': '中国科学院地理科学与资源研究所',  #with risk
    'im': '中国科学院微生物研究所', #网页种类太多，不好解
    'ipe': '中国科学院过程工程研究所',
    #'ivpp': '中国科学院古脊椎动物与古人类研究所',  无链接
    'niaot': '中国科学院国家天文台南京天文光学技术研究所',  #文本合并在一起
    'amss': '中国科学院数学与系统科学研究院',  #文本合并在一起
    'iop': '中国科学院物理研究所', #有js
    'ioa': '中国科学院声学所',  #只有几个院士，文本合并在一起
    #'ic': '中国科学院化学研究所', #点开都是课题主页，不是专家主页
    #'xao': '中国科学院新疆天文台',  无链接
    'ivpp': '中国科学院古脊椎动物与古人类研究所',
    'ibp': '中国科学院生物物理研究所',
    #'sjziam': '中国科学院遗传与发育生物学研究所农业资源研究中心',  delete
    'semi': '中国科学院半导体研究所',  #文本合并在一起
    'ia': '自动化研究所',
    'iee': '中国科学院电工研究所', #文本合并在一起
    'iet': '中国科学院工程热物理研究所',
    'nssc': '中国科学院国家空间科学中心', #单独解析
    'ihns': '中国科学院自然科学史研究所', #单独解析
    'ipm': '中国科学院科技战略咨询研究院',
    'sxicc': '中国科学院山西煤炭化学研究所',
    #'basic': '中国科学院北京综合研究中心 ', #没找到
    #'iie': '中国科学院信息工程研究所', 网站有问题，百人计划下面没有人
    #'dacas_iie': '中国科学院数据与通信保护研究教育中心', #打开学者后，都是页面没找到
    'csu': '中国科学院空间应用工程与技术中心',
    'ucas': '中国科学院大学',
    }

    def __init__(self, *args, **kwargs):
        sqlite_cx = sqlite3.connect("cas_info.sqlite")
        sqlite_cu = sqlite_cx.cursor()
        self.sqlite_cx = sqlite_cx
        self.sqlite_cu = sqlite_cu

    def sql_in(self, url):
        self.sqlite_cu.execute('select * from data where url = ?', (url,)) 
        res = self.sqlite_cu.fetchall()
        if len(res) > 0:
            return True
        return False

    def process_item(self, item, spider):
        name = spider.name
        #print item
        res = [self.institute_name_map[name].decode('utf8')]
        if not hasattr(self, name):
            #self.name = open('output_' + name, 'w')
            setattr(self, name, open('output_' + name, 'w'))
        #for a, b in self.field_map:
        #    res.append
        if 'name' not in item:
            return
        if not self.sql_in(item['url'][0]):
            flag = 'insert'
            logger.debug('insert op')
            sql = 'insert into data values (? ' + ',?' * 20 + ')'
            sql_arg = [self.institute_name_map[name].decode('utf8')]
        else:
            flag = 'update'
            logger.debug('update op')
            sql = 'update data set institute=?'
            for s in self.field_map:
                sql += ',' + s[0] + '= ?'
            sql += 'WHERE url = ?'
            sql_arg = [self.institute_name_map[name].decode('utf8')]
        item['name'] = (item['name'][0].replace(' ', ''), None)
        for a, b in self.field_map:
            if a in item:
                if a != 'page':
                    res.append(item[a][0].replace('\n', '').replace('\t', '').replace('\r', ''))
                    tmp_data = item[a][0]
                else:
                    tmp_data = sqlite3.Binary(item[a][0])
            else:
                res.append(u'')
                tmp_data = u''
            if flag == 'insert':
                sql_arg.append(tmp_data)
            if flag == 'update':
                sql_arg.append(tmp_data)
        if flag == 'insert':
            self.sqlite_cu.execute(sql, sql_arg)
            self.sqlite_cx.commit()
        if flag == 'update':
            sql_arg.append(item['url'][0])
            self.sqlite_cu.execute(sql, sql_arg)
            self.sqlite_cx.commit()



        print >>getattr(self, name), (u'\t'.join(res)).encode('utf8')
        getattr(self, name).flush()
        return item




