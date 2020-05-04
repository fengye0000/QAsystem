import os
import json
from py2neo import Graph,Node
import pymysql

class GraphModel:
    def __init__(self):
        self.table = 'project'
        self.g = Graph(
        host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
        http_port=7474,  # neo4j 服务器监听的端口号
        user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
        password="FengYe1998__")

    # 读取数据
    def read_nodes(self):
        # 节点
        schools = [] 
        cataglories = []
        programs = []
        program_options = []
        modules = []

        program_option_infos = []
        
        # 构建节点关系
        rels_program_contain_module = []
        rels_has_option = []
        rels_belongsto_cataglory = []
        rels_belongsto_school = []
        
        # get school list
        sql1= 'SELECT %s from %s '%('school', self.table)
        result = self.dbconn(sql1)
        for school in result:
            schools += school
        
       # get project description
        sql3 = 'SELECT %s,%s from %s '%("project_name", 'project_desc', "viewwithdesc")
        result = self.dbconn(sql3)
        for row in result:
            pro = {}
            pro['name'] = row[0]
            pro['desc'] = row[1]
            programs.append(pro)

        # get project_option list
        sql4 = 'SELECT %s from %s '%('project_name', self.table)
        result = self.dbconn(sql4)
        for program_option in result:
            program_options += program_option
        
        # get project_option details
        sql5 = 'SELECT %s from %s '%('project_name, degree, duration, start, ucas, institution_code, uk_fees, international_fees, entry_requirement, project_desc','viewwithdesc')
        result = self.dbconn(sql5)
        print(len(result))
        for row in result:
            program_option_info = {}
            program_option_info['name'] = row[0]
            program_option_info['degree'] = row[1]
            program_option_info['duration'] = row[2]
            program_option_info['start'] = row[3]
            program_option_info['ucas'] = row[4]
            program_option_info['insititution_code'] = row[5]
            program_option_info['uk_fees'] = row[6]
            program_option_info['international_fees'] = row[7]
            program_option_info['entry_requirement'] = row[8]
            program_option_info['project_desc'] = row[9]
            program_option_infos.append(program_option_info)
            print(len(program_option_infos))

        # get relation between programs and schools
        sql6 = 'SELECT %s from %s '%(' program, school',self.table)
        result = self.dbconn(sql6)
        for row in result:
            rels_belongsto_school.append([row[0],row[1]])
        
        # get relation between programs and courses
        sql7 = 'SELECT %s from %s '%('program, courses',self.table)
        result = self.dbconn(sql7)
        for row in result:
            module = row[1].split(',')
            for m in module:
                if m[-2:] == 'or':
                    m = m[:-2]
                m = m.strip()
                m = m.lower()
                m = m.replace(" ","-")
                modules += [m]
                rels_program_contain_module.append([row[0],m])

        sql8 = 'SELECT %s from %s '%('program, project_name',self.table)
        result = self.dbconn(sql8)
        for row in result:
            rels_has_option.append([row[0],row[1]])

        sql9 = 'SELECT %s from %s '%('program, cataglory',self.table)
        result = self.dbconn(sql9)
        for row in result:    
            c = row[1].split(',')
            tmp = c
            for ci in tmp:
                ci = ci.strip()
                if ci == 'foundation':
                    continue
                cataglories += [ci]
                rels_belongsto_cataglory.append([row[0],ci])
        # remove duplicate items
        return set(schools), set(cataglories), programs, set(program_options), set(modules),rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos

    def dbconn(self,sql):
        db = pymysql.connect('localhost','root','FengYe2020!','raw_data')
        cursor = db.cursor()
        result = ''
        try:
            # 执行sql语句
            print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            result = cursor.fetchall()
            
        except Exception as e:
            print(e)
        # 关闭数据库连接 
        db.close()
        return result
    
    '''创建节点'''
    def create_node(self,label,nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建program节点'''
    def create_node_for_program(self,label,nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name["name"], desc=node_name["desc"])
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (start_node, end_node, p, q, rel_type, rel_name)
            print(query)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建知识图谱中心疾病的节点'''
    def create_program_option_nodes(self, program_option_infos):
        count = 0
        for program_option_info in program_option_infos:
            node = Node("Program_option", name = program_option_info['name'], degree = program_option_info['degree'],
                        duration = program_option_info['duration'] ,start = program_option_info['start'],
                        uca = program_option_info['ucas'],insititution_code = program_option_info['insititution_code'],
                        uk_fees = program_option_info['uk_fees']
                        ,international_fees = program_option_info['international_fees'] , entry_requirement = program_option_info['entry_requirement'])
            self.g.create(node)
            count += 1
            print(count)
        return

    def create_filter(self):
        str1 = "with-year-abroad"
        str2 = "year-in-industry"
        str3 = "integrated-foundation-year"
        node1 = Node("Filter",name = "with-year-abroad")
        node2 = Node("Filter",name = "year-in-industry")
        node3 = Node("Filter",name = "integrated-foundation-year")
        self.g.create(node1)
        self.g.create(node2)
        self.g.create(node3)
        rels_filter1 = []
        rels_filter2 = []
        rels_filter3 = []
        for line in open("datadict/program_option.txt","r"):
            line = line[:-1]
            if str1 in line:
                rels_filter1.append([str1,line])
            elif str2 in line:
                rels_filter2.append([str2,line])
            elif str3 in line:
                rels_filter3.append([str3,line])
        rels_filter1.append(["with-year-abrod","dental-materials-with-year-abrod"])
        self.create_relationship('Filter', 'Program_option', rels_filter1, 'filtered_by', 'filtered_by')
        self.create_relationship('Filter', 'Program_option', rels_filter2, 'filtered_by', 'filtered_by')
        self.create_relationship('Filter', 'Program_option', rels_filter3, 'filtered_by', 'filtered_by') 
        return
    def change_school_nodes(self, schools):
        count = 0
        for school in schools:
            cql = "MATCH (n:School) where n.name ='%s' set n.english_requirement = '%s'"%(school["name"],school["requirement"])
            print(cql)
            self.g.run(cql)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        schools, cataglories, programs, program_options, modules, rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos = self.read_nodes()
        self.create_program_option_nodes(program_option_infos)
        self.create_node('School', schools)
        print('School:',len(schools))
        self.create_node('Cataglory', cataglories)
        print('Cataglory',len(cataglories))
        self.create_node_for_program('Program', programs)
        print('Program',len(programs))
        self.create_node('Module', modules)
        print('Module',len(modules))
        return



    '''创建实体关系边'''
    def create_graphrels(self):
        schools, cataglories, programs, program_options, modules, rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos = self.read_nodes()
        self.create_relationship('Program', 'School', rels_belongsto_school, 'belongs_to', 'belongsto_school')
        self.create_relationship('Program', 'Program_option', rels_has_option, 'has', 'has_option')
        self.create_relationship('Program', 'Module', rels_program_contain_module, 'taught', 'taught')
        self.create_relationship('Program', 'Cataglory', rels_belongsto_cataglory, 'belongs_to', 'belongsto_cataglory')
    
    def export_data(self):
        schools, cataglories, programs, program_options, modules, rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos = self.read_nodes()
        f_school = open('datadict/school.txt', 'w+')
        f_cataglorie = open('datadict/cataglorie.txt', 'w+')
        f_program = open('datadict/program.txt', 'w+')
        f_program_option = open('datadict/program_option.txt', 'w+')
        f_module = open('datadict/module.txt', 'w+')
        for item in program_options:
            item = item.replace("-"," ")

        f_school.write('\n'.join(list(schools)))
        f_cataglorie.write('\n'.join(list(cataglories)))
        f_program.write('\n'.join(list(programs)))
        f_program_option.write('\n'.join(list(program_options)))
        f_module.write('\n'.join(list(modules)))

        f_school.close()
        f_cataglorie.close()
        f_program.close()
        f_program_option.close()
        f_module.close()
       
        return


if __name__ == '__main__':
    handler = GraphModel()
    handler.read_nodes()
    handler.create_graphnodes()
    handler.create_graphrels()
    # handler.export_data()
    handler.create_filter()