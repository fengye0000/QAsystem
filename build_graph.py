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
        program_option_info = []
        # 构建节点关系
        rels_program_contain_module = []
        rels_has_option = []
        rels_belongsto_cataglory = []
        rels_belongsto_school = []
        
        
        sql1= 'SELECT %s from %s '%('school',self.table)
        result = self.dbconn(sql1)
        for school in result:
            schools += school
        
        # sql2 = 'SELECT %s from %s '%('cataglory',self.table)
        # result = self.dbconn(sql2)
        # for cataglory in result:
        #     c = cataglory.split(',')
        #     for item in c:
        #         cataglories += item
        
        sql3 = 'SELECT %s from %s '%('program',self.table)
        result = self.dbconn(sql3)
        for program in result:
            programs += program
        
        # sql4 = 'SELECT %s from %s '%('project_name',self.table)
        # result = self.dbconn(sql4)
        # for program_option in result:
        #     program_options += program_option
        
        sql5 = 'SELECT %s from %s '%('project_name, degree, duration, start, ucas, insititution_code, uk_fees, international_fees, entry_requirement',self.table)
        result = self.dbconn(sql5)
        for row in result:
            program_options += row[0]
            program_option_info['name'] = row[0]
            program_option_info['degree'] = row[1]
            program_option_info['duration'] = row[2]
            program_option_info['start'] = row[3]
            program_option_info['ucas'] = row[4]
            program_option_info['insititution_code'] = row[5]
            program_option_info['uk_fees'] = row[6]
            program_option_info['international_fees'] = row[7]
            program_option_info['entry_requirement'] = row[8]
            program_option_infos.append(program_option_info)

            
        sql6 = 'SELECT %s from %s '%(' program, school',self.table)
        result = self.dbconn(sql6)
        for row in result:
            rels_belongsto_school.append([row[0],row[1]])
        
        sql7 = 'SELECT %s from %s '%('program, courses',self.table)
        result = self.dbconn(sql7)
        for row in result:
            module = row[0].split(',')
            for m in module:
                # print(m,type(m))
                if m[-2:] == 'or':
                    m = m[:-2]
                m = m.strip()
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
            # print(c)
            tmp = c
            for ci in tmp:
                # print(ci,type(ci))
                ci = ci.strip()
                cataglories += [ci]
                #print(cataglories)
                rels_belongsto_cataglory.append([row[0],ci])

        # print(set(modules))
        print(rels_has_option)
        return set(schools), set(cataglories), set(programs), set(program_options), set(modules),rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos

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
    
    
    def create_node(self,label,nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
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
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            print(query)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        schools, cataglories, programs, program_options, modules, rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos = self.read_nodes()
        # self.create_diseases_nodes(disease_infos)
        self.create_node('School', schools)
        print(len(schools))
        self.create_node('Cataglory', cataglories)
        print(len(cataglories))
        self.create_node('Program', programs)
        print(len(programs))
        self.create_node('Program_option', program_options)
        print(len(program_options))
        self.create_node('Module', modules)
        print(len(modules))
        # self.create_node('Symptom', Symptoms)
        return



    '''创建实体关系边'''
    def create_graphrels(self):
        schools, cataglories, programs, program_options, modules, rels_program_contain_module, rels_has_option, rels_belongsto_school, rels_belongsto_cataglory, program_option_infos = self.read_nodes()
        self.create_relationship('School', 'Program', rels_belongsto_school, 'belongs_to', 'belongsto_school')
        self.create_relationship('Program', 'Program_option', rels_has_option, 'has', 'has')
        self.create_relationship('Program', 'Module', rels_program_contain_module, 'taught', 'taught')
        self.create_relationship('Program', 'Cataglory', rels_belongsto_cataglory, 'belongs_to', 'belongsto_cataglory')
        

if __name__ == '__main__':
    handler = GraphModel()
    handler.read_nodes()
    # handler.create_graphnodes()
    # handler.create_graphrels()
    # handler.export_data()