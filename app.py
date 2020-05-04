# -*- coding: utf-8 -*-
from flask import Flask,jsonify,render_template,request
import json
import sys
from sample import NLU

app = Flask(__name__)#实例化app对象
 
testInfo = {}
nlu = NLU()
@app.route('/_test_post',methods=['GET','POST'])#路由
def test_post():
    data = request.form.get("query")
    print(data) 
    ans = nlu.nluparser(data)
    return json.dumps(ans)
 
@app.route('/')
def hello_world():
    ans = nlu.nluparser("hi")
    return ans

@app.route('/index')
def index():
    return render_template('index.html')
 
 
if __name__ == '__main__':
    app.run(host = '0.0.0.0',#任何ip都可以访问
            port = 5000,#端口
            debug = True
            )


