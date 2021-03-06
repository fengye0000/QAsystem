from __future__ import unicode_literals, print_function

import json
from pathlib import Path
from fuzzywuzzy import process 
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
from answer_search import AnswerSearcher
previousslot=dict()
previousslot["program"]=""

class NLU:
    #training data when implement a class
    def __init__(self):
        SAMPLE_DATASET_PATH = Path(__file__).parent / "dataset.json"
        with SAMPLE_DATASET_PATH.open(encoding="utf8") as f:
            sample_dataset = json.load(f) 
        self.nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
        self.nlu_engine.fit(sample_dataset)
        self.threshold = 93

    # parsing core
    def nluparser(self,text):          
        newslots = [] 
        parsing = self.nlu_engine.parse(text)
        print(json.dumps(parsing, indent=2))
        intent = parsing["intent"]
        slots = parsing["slots"]
        global previousslot
        if len(slots) == 0 and intent != "Intro":
            newslots.append(previousslot["program"])
        for i in range(len(slots)): 
            slot = slots[i]["rawValue"]
            slottype = slots[i]["entity"]
            if slot in ["this", "that", "it", "this program", "it?", ""]:
                slot = previousslot[slottype]
            print(slot)
            result = self.fuzzyw(slot)
            print(result)
            if result[1]<self.threshold: # threshold for automatic correction
                return "No program called %s, are you trying to find %s"%(slot, result[0])
            if result[1]>=self.threshold:
                slot = result[0]
            slot2 = slot.replace(" ", "-")
            slot2 = slot2.lower()
            previousslot[slottype] = slot2 
            newslots.append(slot2)
        print(intent["intentName"])
        print(newslots)
        searcher = AnswerSearcher()
        final_ans = searcher.search_main(intent["intentName"], newslots)
        print(final_ans)
        return final_ans

    # fuzzy match
    def fuzzyw(self,sentence):
        matchlist = ['electrical and electronic engineering', 'politics with business management', 'software engineering for business', 'mathematics', 'aerospace engineering with management', 'politics and sociology', 'politics and international relations', 'linguistics', 'international foundation programme in business and management', 'astrophysics', 'pharmaceutical chemistry', 'economics and politics', 'mechanical engineering', 'global health', 'biomaterials for biomedical sciences', 'english language and linguistics', 'mathematics with finance and accounting', 'accounting and management', 'economics', 'pharmacology and innovative therapeutics', 'theoretical physics', 'zoology', 'financial mathematics', 'aerospace engineering', 'geography ba', 'english literature and linguistics', 'graduate diploma in finance and economics', 'environmental science', 'graduate diploma in humanities and social sciences', 'mathematics and statistics', 'dental materials', 'comparative literature and film studies', 'physics with astrophysics', 'materials science and engineering', 'environmental science with business management', 'biology', 'psychology', 'computer science', 'neuroscience', 'biomedical engineering', 'materials and design', 'comparative literature and linguistics', 'creative computing', 'biochemistry', 'materials science and engineering with management', 'geography with business management', 'sustainable energy engineering', 'physics with particle physics', 'film studies and drama', 'medical genetics', 'computer science and mathematics', 'biomedical sciences', 'economics and finance', 'genetics', 'pure mathematics', 'international relations', 'mechanical engineering with management', 'electronic engineering and telecommunications', 'chemistry', 'mathematics with actuarial science', 'politics', 'english language', 'accounting and finance', 'comparative literature', 'electronic engineering', 'economics and international finance', 'mathematics with statistics', 'medieval history', 'human geography', 'chemical engineering', 'mathematics with management', 'international foundation programme in humanities and social sciences', 'film studies', 'finance', 'drama', 'marketing and management', 'geography bsc', 'physics', 'robotics engineering', 'computer systems engineering', 'world history', 'biomedical engineering with management', 'business management']
        result = process.extractOne(sentence, matchlist)
        return result

    # compare slot content with dataset
    def toDataset(self):
        fp = open("datadict/program.txt", "r")
        fp2 = open("module2.txt", "w+")
        answ = []
        while 1:
            line = fp.readline()
            if not line:
                break
            line = line.lower()
            line = line.replace("-", " ")
            line = line.replace("\n", "")
            answ.append(line)
        fp2.write(str(answ))
        fp2.close()
        fp.close()
   


