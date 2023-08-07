from flask import Flask, request, jsonify
import csv
import io
import psycopg2
import os
import logging
from psycopg2.extras import LoggingConnection
import unittest

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def db_connection(dbname,user,password,host,port):
    # Replace these values with your actual PostgreSQL database configuration
    DATABASE = {
        'dbname': dbname,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }

    conn = psycopg2.connect(connection_factory=LoggingConnection, **DATABASE)
    conn.initialize(logger)
    return conn

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
    
    # Get database connection information from the request data

    dbname = request.args.get('dbname')
    if not dbname:
        logging.info(f"dbname: {dbname}")
        return jsonify({'error': 'Database name not provided'}), 400
    
    user = request.args.get('user')
    if not user:
        logging.info(f"user: {user}")
        return jsonify({'error': 'User not provided'}), 400
    
    password = request.args.get('password')
    if not password:
        logging.info(f"password: {password}")
        return jsonify({'error': 'Password not provided'}), 400
    
    host = request.args.get('host')
    if not host:
        logging.info(f"host: {host}")
        return jsonify({'error': 'Host not provided'}), 400
    
    port = request.args.get('port')
    if not port:
        logging.info(f"port: {port}")
        return jsonify({'error': 'Port not provided'}), 400

    connection = db_connection(dbname,user,password,host,port)

    if file and file.filename.endswith('.csv'):
        content = file.stream.read().decode('utf-8')
        stream = io.StringIO(content)
        reader = csv.reader(stream)
        csv_content = list(reader)

        save_to_db(table_name, csv_content, connection)

        logging.info(f"Connecting to database {dbname} on {host}:{port} as user {user}")

        return jsonify({'message': f'File contents saved to table {table_name}'}), 200
    else:
        return jsonify({'error': 'Invalid file type, please upload a CSV file'}), 400

def save_to_db(table_name, csv_content, connection):
    
    # conn = get_db_connection(dbname,user,password,host,port)
    cur = connection.cursor()

    headers = csv_content[0]
    sanitized_headers = [sanitize_column_name(header) for header in headers]

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(['{} VARCHAR'.format(header) for header in sanitized_headers])});"
    cur.execute(create_table_query)

    chunk_size = 1000
    for start in range(1, len(csv_content), chunk_size):  # start from 1 to skip headers
        end = start + chunk_size
        chunk = csv_content[start:end]
        
        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        cur.executemany(insert_query, chunk)

        # Log the insertion
        logging.info(f"Inserted {len(chunk)} rows into {table_name}.")

    connection.commit()
    connection.close()

def sanitize_column_name(column_name):
    # Replace spaces with underscores and remove non-alphanumeric characters except for underscores
    sanitized = ''.join(e if e.isalnum() or e == '_' else '_' for e in column_name)
    
    # Ensure column names don't start with a number
    if sanitized[0].isdigit():
        sanitized = "_" + sanitized
    
    return sanitized

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'  # Ensure Flask is in development mode
    app.run(debug=True, use_reloader=False, use_debugger=False)