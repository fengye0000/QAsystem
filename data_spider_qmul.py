#!/usr/bin/env python3
# coding: utf-8
# author: fengye
# Date: 20-02-20


#import urllib.request
import urllib.parse
from lxml import etree
import pymongo
import re
from urllib import request
import pymysql
import project_bean

catagplory_list = {'computer-and-data-science','business-and-management',}
catagplory_pre = 'https://www.qmul.ac.uk/study/'
content_pre = 'https://www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/'
url = 'https://www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/biochemistry/'

# 获取单个页面
def get_html(url):
    try :
        headers = {'User-Agent':'Mozilla/5.0'}
        res = request.Request(url=url, headers =headers)
        # prin(url)
        with request.urlopen(res) as f:
            print('Enter url: ' + url)
            data = f.read()
            content = data.decode('UTF-8')
            # print('Data:', content)
            return content
    except :
        pass

# 解析目录页，获取内容页list
def list_parser(content):
    html = etree.HTML(content)
    programs = html.xpath('/html/body/nav/div/div/div[2]/div[1]/div/div[1]/ul/li/a')
    concatURL = list()  
    for i in programs:
        program = i.text
        program = program.lower()
        program = program.replace(' ','-')
        concatURL.append(catagplory_pre + program)
    print(concatURL)
    return concatURL
    
# 解析抽象方法
def myparser(content,full_xpath,pre):
    html = etree.HTML(content)
    courses = html.xpath(full_xpath)
    concatURL = list()
    for i in courses:
        tmp = i.text
        tmp = tmp.lower()
        tmp = tmp.replace(' ','-')
        concatURL.append(pre + tmp)
    return concatURL

# 解析内容页,最终返回list
def content_parser(content,full_xpath):
    html = etree.HTML(content)
    courses = html.xpath(full_xpath)
    # for i in courses:
    #     print(i)
    return courses

def content_obj_parser(content,full_xpath,details):
    html = etree.HTML(content)
    courses = html.xpath(full_xpath)
    for i in range(len(courses)-1):
        if courses[i] == 'Degree': 
            details.degree = courses[i+1]
        elif courses[i]=='Duration':
            details.duration=courses[i+1]
        elif courses[i]=='Start':
            details.start=courses[i+1]
        elif courses[i]=='UCAS code':
            details.ucas=courses[i+1]
        elif courses[i]=='Institution code':
            details.institution_code=courses[i+1]
        elif courses[i]=='Typical A-Level offer':
            details.typical_Alevel_offer=courses[i+1].replace("'","\'")
        elif courses[i]=='UK/EU fees':
            details.uk_fees=courses[i+1]
        elif courses[i]=='International fees':
            details.international_fees=courses[i+1]
        i=i+2
        #text = course[i].lower()

    return courses
#解析i:i+1 一一对应的
def content_pair_parser(content,full_xpath):
    html = etree.HTML(content)
    courses = html.xpath(full_xpath)
    pair = ''
    for i in range(len(courses)-1):
        courses[i+1]=courses[i+1].replace("'","\\'")
        pair= pair+'%s:%s|'%(courses[i],courses[i+1])
        i=i+2
    pair = str(pair)
    return pair

#存进文件
def store(filename,str,mode):
    f = open(filename,mode)
    f.write(str)
    f.close

#找出所有courses
def get_full_courses(url):
    content = get_html(url)
    areas = list_parser(content)#获得所有study areas 的url
    areas_courses = dict()
    for area in areas:
        try:
            content = get_html(area)
            courses = myparser(content,'/html/body/section/div[5]/div/div/ol/li/a/h4',content_pre)
            areas_courses[area] = courses
            print(areas_courses)
        except :
            continue
    store('areas_courses.json', str(areas_courses),'w+')

def get_detail(url,cataglory,desc):
    try:
        content = get_html(url)
        #解析一下URL当projectname
        program = url[len(content_pre):]
        project_dict = dict()
        courses_name = content_parser(content,'//div[@id="study-options-group"]/*/h3/text()')
        schools = content_parser(content,'//*[@id="about"]//*[@data-component="school-info-card"]/div/h4/a/text()')#当前page所属school
        structure = content_parser(content,'//*[@id="structure-tabs"]/div/ul/*/text()') 
        print('cata:'+cataglory)
        i = 1
        for course in courses_name:
            #project对象
            tmp = course.lower()
            tmp = tmp.strip()
            tmp = tmp.replace(' ','-')
            p = project_bean.Project(tmp)
            p.cataglory_desc = desc#/html/body/section[6]/div/div/div[1]/p[1]/text()grid grid--offset-xl-2-l
            project_desc = content_parser(content,'//*[@class="grid grid--offset-xl-2-l"]/*/p/text()')
            # print(project_desc)
            p.project_desc = ' '.join(project_desc)
            entryrequirement = content_pair_parser(content,'//*[@id="entry-requirements"]/div/div[2]/div/div[%s]/div[2]//*/tbody/tr/td/text()'%i)
            content_obj_parser(content,'/html/body/section[3]/div/div[1]/section[%s]/div/div/dl/*/text()'%i,p)
            p.cataglory = cataglory
            p.program = program
            p.school = ','.join(schools)
            p.courses = ','.join(structure)
            p.entry_requirement = entryrequirement
            project_dict[tmp]=p
            i=i+1
        return project_dict
    except:
        print('error in detail')

def dbconn(project_dict,table):
    db = pymysql.connect('localhost','root','FengYe2020!','raw_data')
    cursor = db.cursor()
    # SQL 插入语句
    j=0
    if type(project_dict) == 'NoneType':
        return 
    for key in project_dict:
        details=project_dict[key]
        ucas = details.ucas
        error_code = '(1062, "Duplicate entry \'%s\' for key \'PRIMARY\'")'%ucas.upper()
        sql = """INSERT INTO %s(project_name,degree,duration
            , start, ucas, institution_code,typical_Alevel_offer, uk_fees, international_fees, school, courses, entry_requirement, cataglory, program, cataglory_desc, project_desc)
            VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """%(table,details.project_name,details.degree,details.duration,details.start,details.ucas,details.institution_code,details.typical_Alevel_offer,details.uk_fees,details.international_fees,details.school,details.courses,details.entry_requirement,details.cataglory,details.program, details.cataglory_desc,details.project_desc)
        try:
            # 执行sql语句
            print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e)
            print(error_code)
            if (str(e) == error_code):
                print('enter')
                try:
                    sql = '''SELECT school, cataglory from %s where ucas = '%s'
                    '''%(table,details.ucas)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    school = result[0]
                    cataglory = result[1]
                    print(result)
                    if (school.find(details.school) != -1 & cataglory.find(details.cataglory) != -1):
                        continue
                    if(school.find(details.school) == -1):
                        field = 'school'
                        concated_str = details.school + ', ' +school
                        update_sql = '''UPDATE %s set %s = '%s' where ucas = '%s'
                        '''%(table,field,concated_str,ucas)
                        cursor.execute(update_sql)
                        db.commit()
                    if(cataglory.find(details.cataglory) == -1):
                        field = 'cataglory'
                        concated_str = details.cataglory + ', ' +cataglory
                        update_sql = '''UPDATE %s set %s = '%s' where ucas = '%s'
                        '''%(table,field,concated_str,ucas)
                        cursor.execute(update_sql)
                        db.commit()
                    
                except Exception as e:
                    print(e)
                    continue
                continue
    # 关闭数据库连接 
    db.close()

def cata_desc(url,xpath1,xpath2):
    content = get_html(url)
    descs = content_parser(content,xpath1)  
    # print(descs)
    if len(descs)==0:
        descs = content_parser(url,xpath2)
        return ' '.join(descs)
    else:
        return ' '.join(descs)
def bunch_parse(catagplory_pre,dbtable):
    filename = 'areas_courses.json'
#try:
    fp = open(filename,'r')
    content = fp.read()
    #print(content)
    content = eval(content)
    for key in content:
        values = content[key]
        cata = key[len(catagplory_pre):]
        # print(key)
        desc = cata_desc(key,'/html/body/section/div[3]/div[2]/section/p/text()','/html/body/section/div[3]/div[2]/section/p/*/text()')
        # print(desc)
        for value in values:
            try:
                project_dict = get_detail(value,cata,desc)
                dbconn(project_dict,dbtable)
            except Exception as e:
                print('get detail wrong')
            

    fp.close


# project_dict = get_detail(' https://www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/biochemistry','chemistry','ss')
# # dbconn(project_dict,'project')
bunch_parse(catagplory_pre,'project_copy1')