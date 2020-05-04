from py2neo import Graph
import json

class AnswerSearcher:
    def __init__(self):
        self.preix = "www.qmul.ac.uk/undergraduate/coursefinder/courses/2020/"
        self.g = Graph(
        host = "127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
        http_port = 7474,  # neo4j 服务器监听的端口号
        user = "neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
        password = "FengYe1998__")

    def search_main(self,intent,slot):
        '''进行图数据库查询并返回模版答案'''
        answer = ""
        if intent == "Intro":
            answer = "Hi!<cr>I'm the Queen Mary Bot. I've been trained to help you get your prospectus!"
        if intent == "None":
            answer = "Sorry I can't understand your question, you can check the program list on <a href='https://search.qmul.ac.uk/s/search.html?collection=queenmary-coursefinder-undergraduate-meta&query=&sort=title'>https://search.qmul.ac.uk/s/search.html?collection=queenmary-coursefinder-undergraduate-meta&query=&sort=title</a>"
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
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,%s"%(slot[0], det)
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                detail = answers[i][det]
                answer += name + ":" + detail + "\n"
            answer += "more details on %s%s/"%(self.preix, slot[0])
        if intent == "GetCommonModule":
            answ = []
            cql = "MATCH (n:Program)-[r:taught]->(m)<-[r2:taught]-(p:Program) where n.name ='%s' and p.name='%s' RETURN m.name"%(slot[0],slot[1])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                ans = answers[i]["m.name"]
                ans = ans.replace("-", " ")
                ans = ans.capitalize()
                answ.append(ans)
            answer = "<br>".join(answ)
            if len(answ) == 0:
                answer = "No common class between %s and %s."%(slot[0], slot[1])
        if intent == "GetProgramfee":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.uk_fees,m.international_fees"%(slot[0])
            answers = self.cql_match(cql).data()
            print(answers)
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-", " ")
                uk = answers[i]["m.uk_fees"]
                international = answers[i]["m.international_fees"]
                answer += name + ":" + "uk fee:" + uk + ",international fee:" + international + "<cr>"
            answer = answer[:-4]
            answer = answer.replace("\u00a3","GPB")
            answer += "more details on <a href='%s%s'>%s%s/</a>"%(self.preix, slot[0], self.preix, slot[0])
        if intent == "GetProgramduration":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.duration"%(slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-"," ")
                detail = answers[i]["m.duration"]
                answer += name+":"+detail+"<cr>"
            answer = answer[:-4]
            answer += "more details on <a href='%s%s'>%s%s/</a>"%(self.preix, slot[0], self.preix, slot[0])
        if intent == "GetEntryRequirement":
            cql = "match (n:Program)-[r:has]->(m:Program_option) where n.name='%s' return m.name,m.entry_requirement"%(slot[0])
            answers = self.cql_match(cql).data()
            for i in range(len(answers)):
                name = answers[i]["m.name"]
                name = name.replace("-"," ")
                entry_requirement = answers[i]["m.entry_requirement"]
                entry_requirement = entry_requirement.replace("|", ";")
                answer += name + ":" + entry_requirement + "<cr>"
            answer = answer[:-4]
            answer += "more details on <a href='%s%s'>%s%s/</a>"%(self.preix,slot[0], self.preix, slot[0])
        if intent == "GetProgrambyModule":
            cql = "match (n:Program)-[r:taught]->(m:Module) where m.name='%s' return n.name"%(slot[0])
            answers = self.cql_match(cql).data()
            answer = "The following programs contain %s<cr>"%slot[0]
            for i in range(len(answers)):
                answer += answers[i]["n.name"]+";"
        if intent == "GetRelatedProgram":
            cql = "match (n:Program)-[r:taught]->(m:Module)<-[r2:taught]-(p:Program) where n.name = '%s' return p.name,count(*) order by count(*) desc limit 3"%(slot[0])
            answers = self.cql_match(cql).data()
            answer = "The following programs are strongly related to %s."%slot[0]
            for i in range(len(answers)):
                ans = answers[i]["p.name"]
                ans = ans.replace("-", " ")
                answer += ans+";"
        if intent == "GetprogramIntro":
            cql = "match (n:Program) where n.name = '%s' return n.desc"%(slot[0])
            answers = self.cql_match(cql).data()
            print(answers)
            answ = answers[0]
            answer = "Here is the introduction of %s<cr>"%slot[0] + answ["n.desc"]
            answer = answer.replace("\u2019", "'")
        if intent == "Getschool":
            cql = "MATCH (n:School) RETURN n.name"
            answ = []
            answers = self.cql_match(cql).data()
            print(answers)
            
            for i in range(len(answers)):
                ans = answers[i]["n.name"]
                # answ.append(ans)
                title = 'What program do %s have?'%ans
                botton += self.botton_wrap(ans,title)
            wraped = self.div_wrap(botton)
            answer = "we have following schools, please choose the school you interested in " + wraped
        return answer
                
    def cql_match(self, cql):
        ress = self.g.run(cql)
        return ress

    def botton_wrap(self, text, title):
        botton = ''
        botton = '<button aria-label="%s" title="%s" class="km-quick-replies km-custom-widget-text-color km-quick-rpy-btn km-custom-widget-border-color km-cta-button-many " data-metadata="" data-languagecode="">%s</button>'%(text, title, text)
        return botton

    def div_wrap(self, bottons):
        warped = '<div class="km-msg-box-attachment n-vis "><div class="km-msg-box-progressMeter n-vis "></div></div><div class="km-cta-multi-button-container">%s</div></div>'%bottons
        return warped

if __name__ == '__main__':
    ans = AnswerSearcher()
    final_ans = ans.search_main("GetProgramDetail",["creative-computing","fee"])
    print(final_ans)
        