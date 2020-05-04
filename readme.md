# Smart QA system in campus domain

### 1.directory tree

|— datadict  # dictonary of stored data
|    -- *.txt
|-- static
|   |-- Images
|   |-- credentials.js  
|   |-- index.js 
|   |-- style.css
|-- templates
|   |-- ana.JPG
|   — index.html  # index page of the web application
|— answer_search.py # perform graph database query and return template answer
|— app.py  # entry script of flask framework
|-- areas_courses.json
|— build_graph.py  # the script used to import data from rational database to graph database
|— dataset.json  # trainning dataset
|— dataset.yaml  
|— data_spider_qmul.py # script used to crawl data from QMUL website
|-- index.html
|-- __init__.py
|-- module2.txt
|-- module.txt
|— project_bean.py
|-- project.sql
|-- readme.md
|-- sample_dataset.json
`— sample.py # dialog management

### 2. Procedure of implementation

1. Collecting data

2. Building knowledge map and visualize it 

3. Realizing Intelligent Question and Answer function

4. Setup the web application to provide Q&A service

   **Set up procedures**

   ```shell
   source ./venv/bin/activate
   python3 -m flask run -h 0.0.0.0
   ```

### 3. Other

All source code will be updated at https://github.com/fengye0000/QAsystem, and the service can be access at http://106.53.84.119:5000/index


   

   