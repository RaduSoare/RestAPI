from flask import Flask
from flask import request, jsonify, Response

import psycopg2
from psycopg2 import IntegrityError

import Constants
import os
from models.Country import Country
from database.Database import *

DB_HOST = "localhost:5432"
DB_NAME = "sprc_database"
DB_USER = "postgres"
DB_PASS = "dbpassword"


db_connection = psycopg2.connect(database=DB_NAME,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 host=os.environ['DB_HOST'],
                                 port=5432)


cursor = db_connection.cursor()

cursor.execute(
        'create table if not exists Tari (id serial PRIMARY KEY, nume_tara VARCHAR ( 50 ) UNIQUE NOT NULL, latitudine DOUBLE PRECISION, longitudine DOUBLE PRECISION);')

app = Flask(__name__)

def jsonToCountry(json):
    name = json.get(Constants.NAME)
    if not name:
        return None
    lat = json.get(Constants.LAT)
    if not lat:
        return None
    long = json.get(Constants.LONG)
    if not long:
        return None
    return Country(name, lat, long)

@app.route("/api/countries", methods=["POST"])
def add_country():

    params = request.get_json(silent=True)

    if not params:
        return Response(status=400)

    new_country = jsonToCountry(params)
    if new_country is None:
        return Response(status=400)

    try:
        id = insert_to_countries(cursor, db_connection, new_country)
        return jsonify({'id': id})
    except IntegrityError as e:
        cursor.execute("ROLLBACK")
        db_connection.commit()
        return Response(status=409)

@app.route("/api/countries", methods=["GET"])
def get_countries():

    cursor.execute("SELECT * FROM Tari")

    countries_list = cursor.fetchall()

    countries_json_list = list(map(lambda x: {"id" : x[0], "lat" : x[1], "lon" : x[2]}, countries_list))

    return jsonify(countries_json_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

    db_connection.close()