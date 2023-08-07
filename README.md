#  Flask App with PostgreSQL Database Connection, File Upload, and Unit Tests (Dockerized)

This is a simple Flask application that provides a basic API to connect to a PostgreSQL database using psycopg2, handle requests, and allow file uploads in CSV format. The app includes a function to establish a database connection with logging enabled, as well as a function to save CSV data to the database. Additionally, the application is Dockerized for easy deployment and includes unit tests for testing the functionality.

## Database Connection

The db_connection function in this application establishes a connection to the PostgreSQL database using the provided parameters: dbname, user, password, host, and port. The psycopg2.extras.LoggingConnection is used to enable logging for database interactions.

Please note that you need to modify the function arguments to match your PostgreSQL database configuration.




## Prerequisites
Before running this application, ensure that you have the following installed:

Docker (https://www.docker.com/get-started)

## Process

Build the Docker image:

```
docker build -t flask-postgres-app .
```

Run Docker:

```
docker run -it -p 5000:5000 migrador:1.0.0
```

## Testing

For testing purposes, run the following command 
```
python -m unittest tests/test_app.py
```

## Saving to DataBase

The save_to_db function is used to create a table in the database based on the provided CSV data and save the data to the table. The function also sanitizes the column names to ensure they are valid for database usage.

The API will request Parameters:

table (required): The name of the table in the database where the CSV data will be stored.
dbname (required): The name of the PostgreSQL database.
user (required): The username for database authentication.
password (required): The password for database authentication.
host (required): The host address where the database is running.
port (required): The port number for the database connection.


To update the tables send CURL command (eg using Git Bash):

CURLS example:
```
 curl -X POST -F "file=@imports/hired_employees.csv" "http://127.0.0.1:5000/upload?table=hired_employees&dbname=mydatabase&user=user&password=keypw&host=servicehost&port=XXXX"
 curl -X POST -F "file=@imports/jobs.csv" "http://127.0.0.1:5000/upload?table=jobs&dbname=mydatabase&user=user&password=keypw&host=servicehost&port=XXXX"
 curl -X POST -F "file=@imports/departments.csv" "http://127.0.0.1:5000/upload?table=departments&dbname=mydatabase&user=user&password=keypw&host=servicehost&port=XXXX"
```

Keep in mind that depending on the database and credentials given you will need to change the following parameters in the CURL command:

dbname=mydatabase (modify mydatabase)
user=user (modify user)
password=keypw (modify keypw)
host=servicehost (modify servicehost)
port=XXXX (modify XXXX)


##   Conclusion

This Flask application provides a simple API to interact with a PostgreSQL database, handle file uploads, and is Dockerized for easy deployment. Additionally, it includes unit tests to ensure the correctness of the application's functionality. Feel free to extend and modify it to suit your specific requirements. Happy coding!