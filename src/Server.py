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
db_connection.commit()
cursor.execute(
        'create table if not exists Orase (id serial PRIMARY KEY, id_tara INTEGER NOT NULL, nume_oras VARCHAR ( 50 ) UNIQUE NOT NULL, latitudine DOUBLE PRECISION, longitudine DOUBLE PRECISION, UNIQUE (id_tara, nume_oras));')
db_connection.commit()


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

@app.route("/api/cities", methods=["POST"])
def add_city():

    params = request.get_json(silent=True)

    if not params:
        return Response(status=400)

    new_city = jsonToCity(params)
    if new_city is None:
        return Response(status=400)

    try:
        id = insert_to_cities(cursor, db_connection, new_city)
        return jsonify({'id': id})
    except IntegrityError as e:
        cursor.execute("ROLLBACK")
        db_connection.commit()
        return Response(status=409)


@app.route("/api/countries", methods=["GET"])
def get_countries():

    cursor.execute("SELECT * FROM Tari")

    countries_list = cursor.fetchall()

    countries_json_list = list(map(lambda x: {"id" : x[0], "nume" : x[1], "lat" : x[2], "lon" : x[3]}, countries_list))

    return jsonify(countries_json_list)

@app.route("/api/cities", methods=["GET"])
def get_cities():

    cursor.execute("SELECT * FROM Orase")

    cities_list = cursor.fetchall()

    cities_json_list = list(map(lambda x: {"id" : x[0], "idTara" : x[1] ,"nume" : x[2], "lat" : x[3], "lon" : x[4]}, cities_list))

    return jsonify(cities_json_list)

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

@app.route("/api/cities/<int:id>", methods=["PUT"])
def update_city(id):
    
    params = request.get_json(silent=True)

    if not params:
        return Response(status=400)

    updated_city = jsonToCity(params)
    if updated_city is None:
        return Response(status=400)

    cursor.execute("UPDATE ORASE SET id_tara=%s, nume_oras=%s, latitudine=%s, longitudine=%s where id=%s returning id", (updated_city.countryID, updated_city.name, updated_city.lat, updated_city.long, id))


    if cursor.fetchone() is None:
        return Response(status=404)

    return Response(status=200)

@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_country(id):

    cursor.execute("DELETE FROM TARI WHERE id=%s returning id", (id,))

    if cursor.fetchone()[0] is None:
        return Response(status=404)

    return Response(status=200)

@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_city(id):

    cursor.execute("DELETE FROM ORASE WHERE id=%s returning id", (id,))

    if cursor.fetchone()[0] is None:
        return Response(status=404)

    return Response(status=200)

@app.route("/api/cities/country/<int:id_Tara>", methods=["GET"])
def get_cities_from_country(id_Tara):
    
    cursor.execute("select * from orase where id_tara=%s", (id_Tara,))

    cities_from_country_list = cursor.fetchall()

    cities_from_country_json_list = list(map(lambda x: {"id" : x[0], "idTara" : x[1] ,"nume" : x[2], "lat" : x[3], "lon" : x[4]}, cities_from_country_list))

    return jsonify(cities_from_country_json_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

    db_connection.close()