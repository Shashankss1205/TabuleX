from flask import Flask, request, render_template, jsonify, send_file
from dotenv import load_dotenv
from flask_cors import CORS
import os
import re
import sqlite3
import pandas as pd
# import matplotlib.pyplot as plt
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import subprocess

# load_dotenv()
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# Load google api key
app = Flask(__name__)
CORS(app)
db_name = "mydatabase.db"
history = ['Good tabular data analysis agent']
selected_table_graphy = ""
# **************************************Images of graphs*******************************************
images = [
    {"url": "./static/charts/bar_chart.png", "caption": "Bar Chart", "description": "Compare data across categories using rectangular bars."},
    {"url": "./static/charts/line_chart.png", "caption": "Line Chart", "description": "Show trends over time with connected data points."},
    {"url": "./static/charts/donut_chart.png", "caption": "Donut Chart", "description": "Represent proportions of each category as slices of a circle."},
    {"url": "./static/charts/scatterplot.png", "caption": "Scatterplot", "description": "Display relationships between two variables on a two-dimensional plane."},
    {"url": "./static/charts/area_chart.png", "caption": "Area Chart", "description": "Show data magnitude over time by filling the area between the line and X-axis."},
    {"url": "./static/charts/bubble_chart.png", "caption": "Bubble Chart", "description": "Display relationships between three variables using bubble sizes."},
    {"url": "./static/charts/histogram.png", "caption": "Histogram", "description": "Show data distribution across equal intervals."},
    {"url": "./static/charts/heatmap.png", "caption": "Heatmap", "description": "Display relationships between two variables using color intensity in a matrix."},
    # {"url": "./static/charts/treemap.png", "caption": "Treemap", "description": "Represent hierarchical data with nested rectangles proportional to their value."},
    # {"url": "./static/charts/radar_chart.png", "caption": "Radar Chart", "description": "Display performance or characteristics across multiple dimensions with a circular layout."},
    {"url": "./static/charts/box_plot.png", "caption": "Box Plot", "description": "Show data distribution and detect outliers with a rectangular box and whiskers."},
    {"url": "./static/charts/stacked_bar_chart.png", "caption": "Stacked Bar Chart", "description": "Compare data across categories and show composition with stacked rectangular bars."},
    {"url": "./static/charts/gantt_chart.png", "caption": "Gantt Chart", "description": "Visualize project schedules, tasks, and milestones with horizontal bars representing duration."},
    {"url": "./static/charts/waterfall_chart.png", "caption": "Waterfall Chart", "description": "Visualize cumulative effects of sequential data with vertical bars showing positive and negative values."},
    # {"url": "./static/charts/funnel_chart.png", "caption": "Funnel Chart", "description": "Visualize stages of a process using decreasing trapezoids."}
    {"url": "./static/charts/pie_chart.png", "caption": "Pie Chart", "description": "Show proportions of a whole as slices of a pie, useful for comparing part-to-whole relationships."},
    {"url": "./static/charts/contour_plot.png", "caption": "Contour Plot", "description": "Illustrate three-dimensional data in two dimensions using contour lines to represent levels of a variable."}
]

# **************************************Helper Functions*******************************************
def combo():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    table_names = cursor.fetchall()
    table_col_combo = []
    for table_name in table_names:
        table_name = table_name[0]
        query = f"PRAGMA table_info({table_name});"
        cursor.execute(query)
        column_names = [row[1] for row in cursor.fetchall()]
        # print("Table:", table_name, "Columns:", column_names)
        combo = f"'{table_name}' has columns {column_names}"
        # print(combo)
        table_col_combo.append(combo)
        
    # print(table_col_combo)
    cursor.close()
    conn.close()
    return table_col_combo

def table_data(selected_table_graphy):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(r"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (selected_table_graphy,))
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Retrieve column names
        query = f"PRAGMA table_info({selected_table_graphy});"
        cursor.execute(query)
        column_names = [row[1] for row in cursor.fetchall()]
        
        # Retrieve the first row of data
        cursor.execute(f"SELECT * FROM {selected_table_graphy} LIMIT 1;")
        first_row = cursor.fetchone()
        
        if first_row:
            data_example = dict(zip(column_names, first_row))
        else:
            data_example = "No data available in the table."
        
        combo = f"It has columns named {column_names}. For reference, first row example is {data_example}"
    else:
        combo = f"Table '{selected_table_graphy}' does not exist in the database."
    
    cursor.close()
    conn.close()
    
    return combo

def question_generator():
    table_col_combo= combo()
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Write 10-15 Natural language questions to ask related to the tables {table_col_combo}. Pre exisiting tables and their columns are {table_col_combo}.Dont make random columns on your own. Just write the lines no extra text"
    response = model.generate_content(prompt)
    reply = response.text
    # print(reply)
    ques_list = [line.strip() for line in reply.strip().split('\n')]          
    # print(ques_list)
    return ques_list
items= question_generator()

def collector(chat):
    history.insert(0, chat)

def extract_code_block(text):
    if text.find("```python") | text.find("```Python") | text.find("```PYTHON"):
        start =0
    else:
        start=text.find("```")
        end = text.find("```", start + 3)
        if end == -1:
            return None
        return text[start + 3:end].strip()
    end = text.find("```", start + 3)
    if end == -1:
        return None
    return text[start + 9:end].strip()

def chatbot(input):
    if input:
        table_col_combo = combo()
        
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        # prompt = "Write a story about a magic backpack."
        prompt = f"Write an SQLite command for {input}. Pre exisiting tables and their columns are {table_col_combo}. Pre-existing chats are {history[0]}. Dont make random columns on your own and try to use columns with highest co-relation when asked to alter something, Do not forget to put column names in double quotes if the column has 2 words in it."
        print(prompt)
        response = model.generate_content(prompt)
        reply = response.text
        print(reply)
        extracted_content = re.findall(r"```sqlite(.*?)```", reply, re.DOTALL) or re.findall(r"```sql(.*?)```", reply, re.DOTALL) or re.findall(r"```(.*?)```", reply, re.DOTALL) 
        responses = []
        collector(input)
        # print(extracted_content)
        for content in extracted_content:
            reply = content.strip()
            # print(reply)
            response = execute_sql(reply)
            responses.append(response)            
        return responses

def graphplot(input):
    if (input):
        # table_col_combo = combo()
        table_info = table_data(selected_table_graphy)
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Write a PYTHON command for {input} and dataframe is saved as 'output.csv'. Dataframe has name {table_info}. Dont make random columns on your own and use only columns with highest co-relation when asked to make something. YOU WILL USE ONLY THE COLUMNS I HAVE GIVEN IN THE LIST. WARNING: write code based on the example data in each field for your reference. Only use Matplotlib, pandas, numpy for creating the graphs. save the image plot as 'static/graph.png'. Draw the most suitable graph, if nothing is mentioned about the type of graph"
        # prompt2 = f"Write a Python command to {input} using Matplotlib, pandas, and numpy. The data is saved in a CSV file named 'output.csv'. {table_info} Keep the data types in mind while defining the chart. DONT USE DATE-TIME The task is to create the most suitable graph based on the correlation between columns, but only using the columns provided. Do not include any additional columns or random data. Save the resulting graph as 'static/graph.png'."
        print(prompt)
        response = model.generate_content(prompt)
        reply = response.text
        print(reply)
        if not reply.startswith('import'):
            reply = extract_code_block(reply)

        subproc(reply)
    
        return reply

def process_table_download(table_name):
    conn = sqlite3.connect('mydatabase.db')
    query = "SELECT * FROM " + table_name
    df = pd.read_sql_query(query, conn)
    df.to_csv('output.csv', index=False)
    conn.close()
    # print("Table data has been written to output.csv")
    return {'status': 'success'}

def get_db_connection():
    conn = sqlite3.connect(db_name)
    return conn

def execute_sql(sql_command):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Split the SQL script into individual SQL commands
    sql_commands = [command.strip() for command in sql_command.split(';') if command.strip()]

    # Print the list of SQL commands
    for sql_command in sql_commands:
        # print(sql_command)
        # Check if the SQL command is a SELECT statement
        is_select_query = sql_command.strip().upper().startswith('SELECT')
        cursor.execute(sql_command)
        # # If it's a SELECT statement, fetch and return the query result
        if is_select_query:
            tables = cursor.fetchall()
            # print(tables)
            conn.commit()

        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = f"Tables Available: {cursor.fetchall()}"
            conn.commit()
    # print(tables)
    return tables

def subproc(new_file_content):
    with open('dynamic_script.py', 'w') as file:
        file.write(new_file_content)

    # print("dynamic_script.py created.")
    # activate_script = os.path.join('myenv', 'Scripts', 'activate')
    # activate_cmd = f'call "{activate_script}"'
    # subprocess.run(activate_cmd, shell=True, check=True)

    # Run dynamic_script.py using the Python interpreter
    # python_path = sys.executable
    result = subprocess.run(['python', 'dynamic_script.py'], capture_output=True, text=True)
    result = subprocess.run(['python', 'dynamic_script.py'], capture_output=True, text=True)
    # Print the output
    print(result.stdout)
    print(result.stderr)
    # return 1

# **************************************Routes for Website*******************************************
@app.route("/")
def index():
    # return render_template('index.html')
    return render_template('index.html', items=items)

@app.route("/graphs")
def graphPlot():
    return render_template('graphy.html', images = images)

@app.route("/about")
def about():
    return render_template('about.html')

# *****************************************Routes for APIs******************************************
@app.route("/get", methods=["GET", "POST"])
def chat():
    input = request.form["msg"]
    # print("Input: " + input)
    responses = chatbot(input)
    # print(responses)
    # print(type(responses))
    return responses

@app.route("/graphy", methods=["POST"])
def graphy():
    input = request.form["msg"]
    # print("Input: " + input)
    responses = graphplot(input)
    # print(responses)
    # print(type(responses))
    return responses

@app.route("/listTable", methods=["GET"])
def listingTable():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    table_names = cursor.fetchall()
    print(table_names)
    cursor.close()
    conn.close()
    return table_names

@app.route('/selectTable', methods=['POST'])
def select_table():
    data = request.get_json()
    table_name = data.get('tableName')
    # print(table_name)
    global selected_table_graphy
    selected_table_graphy = table_name
    # Call your Python function with table_name as input
    # Example: Replace this with your actual function call
    result = process_table_download(table_name)

    # Return response if needed
    return jsonify({'message': 'Table download initiated.', 'result': result}), 200

@app.route('/downloadTable')
def Download_CSV():
    path = "./output.csv"
    return send_file(path, as_attachment=True)

@app.route('/downloadGraph')
def Download_Graph():
    path = "./static/graph.png"
    return send_file(path, as_attachment=True)

@app.route('/addimg', methods=['POST'])
def upload():
    table_col_combo = combo()
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    image = Image.open(BytesIO(file.read()))
    genai.configure(api_key=GOOGLE_API_KEY)
    imgmodel = genai.GenerativeModel('gemini-pro-vision')
    # print(imgmodel)
    print(f"Write an SQLite command to add the table heads along with the input data present in the image. Dont make random columns on your own. You are warned : Never compromise the SQL syntax according to the input")
    response = imgmodel.generate_content([f"Write an SQLite command in code blocks like ```sql ........ ``` to add the table heads along with the input data present in the image. Dont make random columns on your own. Dont give table names from the list : {table_col_combo}. You are warned : Never compromise the SQL syntax according to the input", image], stream=True)
    response.resolve()
    response.text
    reply = response.text
    print(reply)
    extracted_content = re.findall(r"```sqlite(.*?)```", reply, re.DOTALL) or re.findall(r"```SQLITE(.*?)```", reply, re.DOTALL) or re.findall(r"```sql(.*?)```", reply, re.DOTALL) or re.findall(r"```SQL(.*?)```", reply, re.DOTALL) 
            # or re.findall(r"```(.*?)```", reply, re.DOTALL) 
    responses = []
    # print(extracted_content)
    for content in extracted_content:
        reply = content.strip()
        # print(reply)
        response = execute_sql(reply)
        responses.append(response)            
    return responses

@app.route('/addtable', methods=['POST'])
def browse_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    base_filename = file.filename.split('.')[0]
    base_filename = base_filename.replace("-", "")
    connection = sqlite3.connect(db_name)
    df.to_sql(base_filename, connection, if_exists='replace', index=False)
    connection.close()
    items= question_generator()
    return 'File uploaded successfully'

@app.route('/show', methods=['POST'])
def show_file():

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = [table[0] for table in cursor.fetchall()]
    
    # Fetch data from each table
    data = {}
    for table in tables:
        query = f"PRAGMA table_info({table});"
        cursor.execute(query)

        # Fetch the column names for the current table
        column_names = [row[1] for row in cursor.fetchall()]
        tuple_of_col = tuple(column_names)
        cursor.execute(f"SELECT * FROM {table};")
        table_data = cursor.fetchall()
        table_data.insert(0, tuple_of_col)
        table_data = [list(t) for t in table_data]
        data[table] = table_data
    conn.close()
    # print(data)
    # print(type(data))
    return jsonify({'output_value': data})


if __name__ == '__main__':
    app.run(debug=True)