from flask import Flask, request, jsonify
import csv
import io
import sqlite3




app = Flask(__name__)
DATABASE = 'mydatabase.db'


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.endswith('.csv'):
        # read and process the file contents
        content = file.stream.read().decode('utf-8')
        stream = io.StringIO(content)
        reader = csv.reader(stream)
        csv_content = list(reader)

        # Print each row to the log
        for row in csv_content:
            print(row)

        return jsonify({'message': 'File contents printed to the log'}), 200
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
    #app.run(debug=True)
    create_database() 
    app.run(debug=True, use_reloader=False, use_debugger=False)
