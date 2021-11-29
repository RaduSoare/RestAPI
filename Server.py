import json
from functools import reduce

from flask import Flask
from flask import request, jsonify, Response

import psycopg2
from psycopg2 import IntegrityError

import Constants
import models
from models.Country import Country, country_to_json
from database.Database import *

DB_HOST = "localhost:5432"
DB_NAME = "sprc_database"
DB_USER = "postgres"
DB_PASS = "dbpassword"

db_connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS)

# de incercat cursor_Factory=ceva
cursor = db_connection.cursor()

#cursor.execute("select * from {0}".format("student"))

#print(cursor.fetchall()[0][0])

#db_connection.commit()

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
    app.run('0.0.0.0', debug=True)

    db_connection.close()