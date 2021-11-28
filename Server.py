import json
from flask import Flask
from flask import request, jsonify, Response

import psycopg2

DB_HOST = "localhost:5432"
DB_NAME = "sprc_database"
DB_USER = "postgres"
DB_PASS = "dbpassword"

db_connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS)

cursor = db_connection.cursor()



cursor.execute("select * from {0}".format("student"))

print(cursor.fetchall()[0][0])

#db_connection.commit()


db_connection.close()

app = Flask(__name__)

print(12)