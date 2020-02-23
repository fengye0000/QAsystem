#!/usr/bin/env python3
# coding: utf-8
# File: data_spider.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3


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
content = '''
<html>
<body>
<div class="tabs" id="structure-tabs">
<div class="tab tab-y0 prose" id="zero">
<h3 class="year">Year 0</h3>
<p>Foundation</p>
<p>One Year-long double module allocated based on previous maths qualifications:</p>
<ul>
<li>Mathematics A&nbsp; or</li>
<li>Mathematics B</li>
</ul>
<p>Semester 1</p>
<h4><strong>Compulsory</strong></h4>
<ul>
<li>Computing</li>
<li>Essential Foundation Mathematics</li>
<li>Communication in Science and Technology</li>
</ul>
<p>Semester 2</p>
<h4><strong>Compulsory</strong></h4>
<ul>
<li>Digital Electronics and Computer Systems</li>
<li>Introduction to Business Information Systems</li>
<li>Discrete Mathematics</li>
</ul>
<p class="module-change">Please note that all modules are subject to change.</p></div>
<div class="tab tab-y1 prose" id="first">
<h3 class="year">Year 1</h3>
<ul>
<li>Automata and Formal Languages</li>
<li>Calculus I</li>
<li>Calculus II</li>
<li>Geometry I</li>
<li>Numbers, Sets and Functions</li>
<li>Object Oriented Programming</li>
<li>Procedural Programming</li>
<li>Professional and Research Practice</li>
</ul>
<p class="module-change">Please note that all modules are subject to change.</p></div><div class="tab tab-y2 prose" id="second">
<h3 class="year">Year 2</h3>
<h4>Compulsory</h4>
<ul>
<li>Algorithms and Data Structures in an Object Oriented Framework</li>
<li>Database Systems</li>
<li>Introduction to Probability</li>
<li>Linear Algebra I</li>
</ul>
<h4>Choose one from</h4>
<ul>
<li>Calculus III</li>
<li>Internet Protocols and Applications</li>
<li>Probability Models</li>
<li>Software Engineering</li>
</ul>
<h4>Choose&nbsp;from</h4>
<ul>
<li>Introduction to Algebra</li>
<li>Introduction to Statistics</li>
</ul>
<h4>Choose two from</h4>
<ul>
<li>Algebraic Structures I</li>
<li>Complex Variables</li>
<li>Graphical User Interfaces</li>
<li>Operating Systems</li>
<li>Software Engineering Project</li>
</ul>
<p class="module-change">Please note that all modules are subject to change.</p></div><div class="tab tab-y3 prose" id="third">
<h3 class="year">Year 3</h3>
<h4>Compulsory</h4>
<ul>
<li>Computability, Complexity and Algorithms</li>
<li>Project</li>
</ul>
<h4>Choose two from</h4>
<ul>
<li>Big Data Processing</li>
<li>Calculus III</li>
<li>Chaos and Fractals</li>
<li>Combinatorics</li>
<li>Computer Graphics</li>
<li>Entrepreneurship in Information Technology</li>
<li>Linear Algebra II</li>
<li>Semi-Structured Data and Advanced Data Modelling</li>
<li>Web Programming</li>
</ul>
<h4>Choose three from</h4>
<ul>
<li>Algebraic Structures I</li>
<li>Artificial Intelligence</li>
<li>Bayesian Decision and Risk Analysis</li>
<li>C++ for Image processing</li>
<li>Coding Theory</li>
<li>Communicating and Teaching Computing (UAS)</li>
<li>Complex Variables</li>
<li>Digital Media and Social Networks</li>
<li>Distributed Systems</li>
<li>Interaction Design</li>
<li>Number Theory</li>
<li>Security Engineering</li>
</ul>
<p class="module-change">Please note that all modules are subject to change.</p></div></div></div><div class="column-item container container--sm"><h2 class="th-s2 text-blue my-4">Study options</h2><div class="prose"><p>Apply for this degree with any of the following options. Take care to use the correct UCAS code - it may not be possible to change your selection later.</p></div>
</body>
</html>
'''
#url = catagplory_pre + 'business-and-management'
# 获取单个页面
def get_html(url):
    try :
        with request.urlopen(url) as f:
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
        course[i+1]=course[i+1].replace("'","\\'")
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

def get_detail(url,cataglory):
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
    for key in project_dict:
        details=project_dict[key]
        ucas = details.ucas
        error_code = '(1062, "Duplicate entry \'%s\' for key \'PRIMARY\'")'%ucas.upper()
        sql = """INSERT INTO %s(project_name,degree,duration
            , start, ucas, institution_code,typical_Alevel_offer, uk_fees, international_fees, school, courses, entry_requirement, cataglory, program)
            VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """%(table,details.project_name,details.degree,details.duration,details.start,details.ucas,details.institution_code,details.typical_Alevel_offer,details.uk_fees,details.international_fees,details.school,details.courses,details.entry_requirement,details.cataglory,details.program)
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
        for value in values:
        # try:
            project_dict = get_detail(value,cata)
            dbconn(project_dict,dbtable)
        # except Exception as e:
            print('get detail wrong')
            

    fp.close
# except IOError:
#     print('error in open: %s'%filename)
#     fp.close
    

# project_dict = get_detail(' https://www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/chemistry','chemistry')
# dbconn(project_dict,'project')
bunch_parse(catagplory_pre,'project_copy1')