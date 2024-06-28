from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

from flask_cors import CORS
import os
import re
import sys
import sqlite3
import csv
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import google.generativeai as genai
from PIL import Image
# import cv2
from io import BytesIO
import requests
import subprocess
# from userdata import HUGGINGFACE_API_KEY
# from userdata import GOOGLE_API_KEY

load_dotenv()
# HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')



app = Flask(__name__)
CORS(app)


db_name = "mydatabase.db"
history = ['Good tabular data analysis agent']

# val = f"Bearer {HUGGINGFACE_API_KEY}"
# API_URL = "https://api-inference.huggingface.co/models/codenamewei/speech-to-text"
# headers = {"Authorization": val}


def combo():
    # 1. Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    # 2. Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # 3. Query the SQLite database to fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # 4. Fetch the table names
    table_names = cursor.fetchall()
    table_col_combo = []
    # 5. Iterate through the table names and fetch their column names
    for table_name in table_names:
        table_name = table_name[0]  # Extract the table name from the result

        # Query to fetch column names of the current table
        query = f"PRAGMA table_info({table_name});"
        cursor.execute(query)

        # Fetch the column names for the current table
        column_names = [row[1] for row in cursor.fetchall()]

        # Print or use the table name and column names
        print("Table:", table_name)
        print("Columns:", column_names)
        combo = f"'{table_name}' has columns {column_names}"
        print(combo)
        table_col_combo.append(combo)
        
    print(table_col_combo)
    # 6. Close the cursor and the database connection
    cursor.close()
    conn.close()
    return table_col_combo

def collector(chat):
    history.insert(0, chat)

def extract_code_block(text):
    if text.find("```python") | text.find("```Python") | text.find("```PYTHON"):
        start =1
    if start == -1:
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
        
        print(f"Write an SQLite command to {input} if the table and their columns are {table_col_combo}  Pre-existing chats are {history[0]}.")
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
        prompt = f"Write a PYTHON command for {input} and dataframe is named 'output.csv'. Pre exisiting tables and their columns are {table_col_combo}. Pre-existing chats are {history[0]}. Dont make random columns on your own and try to use columns with highest co-relation when asked to alter something, Do not forget to put column names in double quotes if the column has 2 words in it. save the image plot as 'static/graph.png'"
        
        print(f"Write a PYTHON command to {input} if the table and their columns are {table_col_combo}  Pre-existing chats are {history[0]}.")
        response = model.generate_content(prompt)
        reply = response.text
        print(reply)
        if not reply.startswith('import'):
            reply = extract_code_block(reply)

        subproc(reply)
    
        return reply



def get_db_connection():      # Function to establish a database connection
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



#Routes for Website
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/graphy")
def gallery():
    return render_template('graphy.html')

@app.route("/about")
def about():
    return render_template('about.html')

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

# @app.route("/audio", methods=["POST"])
# def query():
#     # with open(filename, "rb") as f:
#         # data = f.read()
#     audio_data = request.files['audio']
#     response = requests.post(API_URL, headers=headers, files={'audio': audio_data})
#     print(response.json())
#     if response.status_code == 200:
#         return response.json()["text"]
#     else:
#         return "Error processing audio", 500



@app.route("/listTable", methods=["GET"])
def listingTable():
    # 1. Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    # 2. Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # 3. Query the SQLite database to fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # 4. Fetch the table names
    table_names = cursor.fetchall()
    print(table_names)
    cursor.close()
    conn.close()
    return table_names

@app.route('/downloadTable', methods=['POST'])
def download_table():
    data = request.get_json()
    table_name = data.get('tableName')

    # Call your Python function with table_name as input
    # Example: Replace this with your actual function call
    result = process_table_download(table_name)

    # Return response if needed
    return jsonify({'message': 'Table download initiated.', 'result': result}), 200

def process_table_download(table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')

    # SQL query to fetch the table data
    query = "SELECT * FROM " + table_name

    # Use pandas to read the SQL query results into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Write the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)

    # Close the database connection
    conn.close()

    print("Table data has been written to output.csv")

    print(f'Downloading table: {table_name}')
    # Implement your logic here (e.g., download the table)

    return {'status': 'success'}



@app.route('/addimg', methods=['POST'])
def upload():
    table_col_combo = combo()
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    image = Image.open(BytesIO(file.read()))
    # image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    # Display the image
    # cv2.imshow("My Image", image)

    # Wait for a key press to close the window (optional)
    # cv2.waitKey(0)
    # from userdata import GOOGLE_API_KEY
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
    return 'File uploaded successfully'
    # base_filename = file.filename.split('.')[0]
    # connection = sqlite3.connect(db_name)
    # cursor = connection.cursor()

    # # Create table with column names inferred from the first row of the CSV file
    # create_table_query = f"CREATE TABLE IF NOT EXISTS {base_filename} ("
    # with open(file, 'r') as f:
    #     columns = f.readline().strip().split(',')
    #     for column in columns:
    #         create_table_query += f"{column.strip()} TEXT,"
    #     create_table_query = create_table_query[:-1] + ")"
    #     cursor.execute(create_table_query)

    # # Insert data from CSV into the created table
    # with open(file, 'r') as f:
    #     next(f)  # Skip header row
    #     for line in f:
    #         values = line.strip().split(',')
    #         placeholders = ','.join(['?' for _ in range(len(values))])
    #         insert_query = f"INSERT INTO {base_filename} VALUES ({placeholders})"
    #         cursor.execute(insert_query, values)

    # connection.commit()
    # connection.close()
    
    # return 'File uploaded successfully'


@app.route('/show', methods=['POST'])
def show_file():

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
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

def subproc(new_file_content):

    with open('dynamic_script.py', 'w') as file:
        file.write(new_file_content)

    print("dynamic_script.py created.")
    # activate_script = os.path.join('myenv', 'Scripts', 'activate')
    # activate_cmd = f'call "{activate_script}"'
    # subprocess.run(activate_cmd, shell=True, check=True)

    # Run dynamic_script.py using the Python interpreter that has pandas installed
    # python_path = sys.executable
    result = subprocess.run(['python', 'dynamic_script.py'], capture_output=True, text=True)
    # Print the output
    print(result.stdout)
    print(result.stderr)
    # return 1
# subproc()

if __name__ == '__main__':
    app.run(debug=True)