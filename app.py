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

def question_generator():
    table_col_combo= combo()
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Write 10-15 Natural language questions to ask related to the tables {table_col_combo}. Pre exisiting tables and their columns are {table_col_combo}.Dont make random columns on your own. Just write the lines no extra text"
    response = model.generate_content(prompt)
    reply = response.text
    print(reply)
    ques_list = [line.strip() for line in reply.strip().split('\n')]          
    print(ques_list)
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
        print(extracted_content)
        for content in extracted_content:
            reply = content.strip()
            print(reply)
            response = execute_sql(reply)
            responses.append(response)            
        return responses

def graphplot(input):
    if (input):
        table_col_combo = combo()
        
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')

        # prompt = "Write a story about a magic backpack."
        prompt = f"Write a PYTHON command for {input} and dataframe is named 'output.csv'. Pre exisiting tables and their columns are {table_col_combo}. Pre-existing chats are {history[0]}. Dont make random columns on your own and try to use columns with highest co-relation when asked to alter something, Do not forget to put column names in double quotes if the column has 2 words in it.Only use Matplotlib, pandas, numpy for creating the graphs. save the image plot as 'static/graph.png'"
        
        print(f"Write a PYTHON command to {input} if the table and their columns are {table_col_combo}  Pre-existing chats are {history[0]}.")
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
    print("Table data has been written to output.csv")
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
        print(sql_command)
        # Check if the SQL command is a SELECT statement
        is_select_query = sql_command.strip().upper().startswith('SELECT')
        cursor.execute(sql_command)
        # # If it's a SELECT statement, fetch and return the query result
        if is_select_query:
            tables = cursor.fetchall()
            print(tables)
            conn.commit()

        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = f"Tables Available: {cursor.fetchall()}"
            conn.commit()
    print(tables)
    return tables

def subproc(new_file_content):
    with open('dynamic_script.py', 'w') as file:
        file.write(new_file_content)

    print("dynamic_script.py created.")
    # activate_script = os.path.join('myenv', 'Scripts', 'activate')
    # activate_cmd = f'call "{activate_script}"'
    # subprocess.run(activate_cmd, shell=True, check=True)

    # Run dynamic_script.py using the Python interpreter
    # python_path = sys.executable
    result = subprocess.run(['python3', 'dynamic_script.py'], capture_output=True, text=True)
    # result = subprocess.run(['python3', 'dynamic_script.py'], capture_output=True, text=True)
    # Print the output
    print(result.stdout)
    print(result.stderr)
    # return 1


# **************************************Routes for Website*******************************************
@app.route("/")
def index():
    # return render_template('index.html')
    return render_template('index.html', items=items)

@app.route("/graphy")
def graphPlot():
    return render_template('graphy.html')

@app.route("/about")
def about():
    return render_template('about.html')

# *****************************************Routes for APIs******************************************
@app.route("/get", methods=["GET", "POST"])
def chat():
    input = request.form["msg"]
    print("Input: " + input)
    responses = chatbot(input)
    print(responses)
    print(type(responses))
    return responses

@app.route("/graphy", methods=["POST"])
def graphy():
    input = request.form["msg"]
    print("Input: " + input)
    responses = graphplot(input)
    print(responses)
    print(type(responses))
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
    print(imgmodel)
    print(f"Write an SQLite command to add the table heads along with the input data present in the image. Dont make random columns on your own. You are warned : Never compromise the SQL syntax according to the input")
    response = imgmodel.generate_content([f"Write an SQLite command in code blocks like ```sql ........ ``` to add the table heads along with the input data present in the image. Dont make random columns on your own. Dont give table names from the list : {table_col_combo}. You are warned : Never compromise the SQL syntax according to the input", image], stream=True)
    response.resolve()
    response.text
    reply = response.text
    print(reply)
    extracted_content = re.findall(r"```sqlite(.*?)```", reply, re.DOTALL) or re.findall(r"```SQLITE(.*?)```", reply, re.DOTALL) or re.findall(r"```sql(.*?)```", reply, re.DOTALL) or re.findall(r"```SQL(.*?)```", reply, re.DOTALL) 
            # or re.findall(r"```(.*?)```", reply, re.DOTALL) 
    responses = []
    print(extracted_content)
    for content in extracted_content:
        reply = content.strip()
        print(reply)
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
    print(type(data))
    return jsonify({'output_value': data})


if __name__ == '__main__':
    app.run(debug=True)