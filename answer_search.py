from py2neo import Graph
import json

class AnswerSearcher:
    def __init__(self):
        self.preix = "www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/"
        self.g = Graph(
        host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
        http_port=7474,  # neo4j 服务器监听的端口号
        user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
        password="FengYe1998__")
    def search_main(self,intent,slot):
        answer=""
        if intent == "Intro":
            answer = "Hi!<br>I'm the Queen Mary Bot. I've been trained to help you get your prospectus!"
        if intent == "GetModule":
            answ = []
            cql = "MATCH (n1:Program)-[r:taught]->(n2:Module) where n1.name = '%s' RETURN n2.name"%(slot[0])
            print (slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                ans = answers[i]["n2.name"]
                answ.append(ans)
            answer = "<br>".join(answ)
        if intent == "GetProgramDetail":
            answer = ""
            det = "m."+slot[1]
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,%s"%(slot[0],det
            )
            answers = self.cql_match(cql).data()
            # print(answers)
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                detail = answers[i][det]
                answer += name+":"+detail+"\n"
            answer += "more details on %s%s/"%(self.preix,slot[0])
        if intent == "GetCommonModule":
            answ = []
            cql = "MATCH (n:Program)-[r:taught]->(m)<-[r2:taught]-(p:Program) where n.name ='%s' and p.name='%s' RETURN m.name"%(slot[0],slot[1])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                ans = answers[i]["m.name"]
                answ.append(ans)
            answer = "<br>".join(answ)
            if len(answ)==0:
                answer = "No common class between %s and %s."%(slot[0],slot[1])
        if intent =="GetProgramfee":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.uk_fees,m.international_fees"%(slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-"," ")
                uk = answers[i]["uk_fees"]
                international = answers[i]["international_fees"]
                answer += name+":"+"uk fee:"+uk+",international fee:"+international+"\n"
        if intent =="GetProgramduration":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.duration"%(slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-"," ")
                detail = answers[i]["m.duration"]
                answer += name+":"+detail+"\n"
           
        if intent == "GetEntryRequirement":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.entry_requirement"%(slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-"," ")
                entry_requirement = answers[i]["m.entry_requirement"]
                entry_requirement = entry_requirement.replace("|","\n")
                answer += name+":"+entry_requirement+"<br>"
        if intent == "GetProgrambyModule":
            cql = "match (n:Program)-[r:taught]->(m:Module) where m.name='%s' return n.name"%(slot[0])
            answers = self.cql_match(cql).data()
            answer = "The following programs contain %s\n"%slot[0]
            for i in range(len(answers)):
                answer += answers[i]["n.name"]+"\n"
        # if intent == "GetprogramIntro":
        #     cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.desc"%(slot[0])
        #     answers = self.cql_match(cql).data()
        #     for i in range(len(answers)):
        #          name = answers[i]["m.name"]
        #         name = name.replace("-"," ")
        #         detail = answers[i]["m.duration"]
        #         answer += name+":"+detail+"\n"
        if intent == "GetRelatedProgram":
            cql = "match (n:Program)-[r:taught]->(m:Module)<-[r2:taught]-(p:Program) where n.name = '%s' return p.name,count(*) order by count(*) desc limit 3"%(slot[0])
            answers = self.cql_match(cql).data()
            answer = "The following programs are strongly related to %s\n"%slot[0]
            for i in range(len(answers)):
                ans = answers[i]["p.name"]
                ans = ans.replace("-"," ")
                answer += ans+";"
        return answer
                

    def cql_match(self,cql):
        ress = self.g.run(cql)
        # print (ress)
        return ress

if __name__ == '__main__':
    ans = AnswerSearcher()
    final_ans = ans.search_main("GetProgramDetail",["creative-computing","fee"])
    print(final_ans)
        