from flask import Flask
from flask import request, jsonify, Response

import psycopg2
from psycopg2 import IntegrityError

import Constants
import os
from models.Country import *
from models.City import *
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
cursor.execute(
        'create table if not exists Orase (id serial PRIMARY KEY, id_tara INTEGER UNIQUE NOT NULL, nume_oras VARCHAR ( 50 ) UNIQUE NOT NULL, latitudine DOUBLE PRECISION, longitudine DOUBLE PRECISION);')

app = Flask(__name__)


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

# @app.route("/api/cities", methods=["POST"])
# def add_city():

#     params = request.get_json(silent=True)

#     if not params:
#         return Response(status=400)

#     new_city = jsonToCity(params)
#     if new_city is None:
#         return Response(status=400)

#     try:
#         id = insert_to_cities(cursor, db_connection, new_city)
#         return jsonify({'id': id})
#     except IntegrityError as e:
#         cursor.execute("ROLLBACK")
#         db_connection.commit()
#         return Response(status=409)


@app.route("/api/countries", methods=["GET"])
def get_countries():

    cursor.execute("SELECT * FROM Tari")

    countries_list = cursor.fetchall()

    countries_json_list = list(map(lambda x: {"id" : x[0], "nume" : x[1], "lat" : x[2], "lon" : x[3]}, countries_list))

    return jsonify(countries_json_list)

@app.route("/api/countries/<int:id>", methods=["PUT"])
def update_country(id):
    
    params = request.get_json(silent=True)

    if not params:
        return Response(status=400)

    updated_country = jsonToCountry(params)
    if updated_country is None:
        return Response(status=400)


    cursor.execute("UPDATE TARI SET nume_tara=%s, latitudine=%s, longitudine=%s where id=%s returning id", (updated_country.name, updated_country.lat, updated_country.long, id))

    if cursor.fetchone() is None:
        return Response(status=404)

    return Response(status=200)

@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_country(id):

    cursor.execute("DELETE FROM TARI WHERE id=%s returning id", (id,))

    if cursor.fetchone() is None:
        return Response(status=404)

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

    db_connection.close()