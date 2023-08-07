from flask import Flask, request, jsonify
import csv
import os
import io
import sqlite3
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
DATABASE = 'mydatabase.db'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    table_name = request.args.get('table')
    if not table_name:
        return jsonify({'error': 'Table name not provided'}), 400
    
    if file and file.filename.endswith('.csv'):
        content = file.stream.read().decode('utf-8')
        stream = io.StringIO(content)
        reader = csv.reader(stream)
        csv_content = list(reader)

        save_to_db(table_name, csv_content)



        return jsonify({'message': f'File contents saved to table {table_name}'}), 200
    else:
        return jsonify({'error': 'Invalid file type, please upload a CSV file'}), 400
    

def create_database():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Create the 'departments' table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            department STRING
        )
    ''')

    # Create the 'jobs' table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job STRING
        )
    ''')

    # Create the 'hired_employees' table with foreign key constraints
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hired_employees (
            id INTEGER PRIMARY KEY,
            name STRING,
            datetime STRING,
            department_id INTEGER,
            job_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')

    conn.commit()
    conn.close()

    
def save_to_db(table_name, csv_content):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    headers = csv_content[0]
    sanitized_headers = [sanitize_column_name(header) for header in headers]

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(['{} TEXT'.format(header) for header in sanitized_headers])});"
    cur.execute(create_table_query)

    chunk_size = 1000
    for start in range(1, len(csv_content), chunk_size):  # start from 1 to skip headers
        end = start + chunk_size
        chunk = csv_content[start:end]

        placeholders = ', '.join(['?'] * len(headers))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        cur.executemany(insert_query, chunk)

        # Log the insertion
        logging.info(f"Inserted {len(chunk)} rows into {table_name}.")

        

    conn.commit()
    conn.close()

def sanitize_column_name(column_name):
    # Replace spaces with underscores and remove non-alphanumeric characters except for underscores
    sanitized = ''.join(e if e.isalnum() or e == '_' else '_' for e in column_name)

    # Ensure column names don't start with a number
    if sanitized[0].isdigit():
        sanitized = "_" + sanitized

    return sanitized

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'  # Ensure Flask is in development mode
    create_database() 
    app.run(debug=True, use_reloader=False, use_debugger=False)
