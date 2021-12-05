from flask import Flask
from flask import request, jsonify, Response

import psycopg2
from psycopg2 import IntegrityError

import Constants
import os
from models.Country import *
from models.City import *
from models.Temperature import *
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


cursor.execute('drop table tari;')
db_connection.commit()
cursor.execute('drop table orase;')
db_connection.commit()
cursor.execute('drop table temperaturi;')
db_connection.commit()

cursor.execute(
        'create table if not exists Tari (id serial PRIMARY KEY, nume_tara VARCHAR ( 50 ) UNIQUE NOT NULL, latitudine DOUBLE PRECISION, longitudine DOUBLE PRECISION);')
db_connection.commit()

cursor.execute(
        'create table if not exists Orase (id serial PRIMARY KEY, id_tara INTEGER NOT NULL, nume_oras VARCHAR ( 50 ) UNIQUE NOT NULL, latitudine DOUBLE PRECISION, longitudine DOUBLE PRECISION, UNIQUE (id_tara, nume_oras));')
db_connection.commit()

cursor.execute(
    'create table if not exists Temperaturi (id serial PRIMARY KEY, id_oras INTEGER NOT NULL, valoare DOUBLE PRECISION,  timestamp DATE NOT NULL DEFAULT CURRENT_DATE, UNIQUE (id_oras, timestamp));'
)
db_connection.commit()


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


### POST ROUTES ###

@app.route("/api/countries", methods=["POST"])
def add_country():

    return post_helper(request.get_json(silent=True), cursor, db_connection, jsonToCountry, insert_to_countries)


@app.route("/api/cities", methods=["POST"])
def add_city():

    return post_helper(request.get_json(silent=True), cursor, db_connection, jsonToCity, insert_to_cities)

@app.route("/api/temperatures", methods=["POST"])
def add_temperature():

    return post_helper(request.get_json(silent=True), cursor, db_connection, jsonToTemperature, insert_to_temperatures)


### GET ROUTES ###

@app.route("/api/countries", methods=["GET"])
def get_countries():

    sql_command = "SELECT * FROM %s" % Constants.TARI_TABLE

    return get_helper(sql_command, cursor, fetched_data_to_json_countries)

@app.route("/api/cities", methods=["GET"])
def get_cities():

    sql_command = "SELECT * FROM %s" % Constants.ORASE_TABLE

    return get_helper(sql_command, cursor, fetched_data_to_json_cities)

@app.route("/api/cities/country/<int:id_Tara>", methods=["GET"])
def get_cities_from_country(id_Tara):
    
    sql_command = "select * from orase where id_tara=%s" %  id_Tara

    return get_helper(sql_command, cursor, fetched_data_to_json_cities)

# @app.route("/api/temperatures", methods=["GET"])
# def get_temperatures():
#     lat_param = float(request.args.get(Constants.LAT))
#     lon_param = float(request.args.get(Constants.LONG))
#     from_param = request.args.get(Constants.FROM)
#     until_param = request.args.get(Constants.UNTIL)

#     # cursor.execute(sql_command)

#     # locations_list = cursor.fetchall()

#     # for location 


#     return jsonify(lat_param)

# @app.route("/api/temperatures/cities/<int:id_oras>", methods=["GET"])
# def get_temperatures_cities(id_oras):
#     return Response(status=200)

# @app.route("/api/temperatures/countries/<int:id_Tara>", methods=["GET"])
# def get_temperatures_countries(id_Tara):
#     return Response(status=200)


### PUT ROUTES ###

@app.route("/api/countries/<int:id>", methods=["PUT"])
def update_country(id):

    return put_helper(request.get_json(silent=True), id, cursor, jsonToCountry, execute_update_country, db_connection)


@app.route("/api/cities/<int:id>", methods=["PUT"])
def update_city(id):
    
    return put_helper(request.get_json(silent=True), id, cursor, jsonToCity, execute_update_city, db_connection)

@app.route("/api/temperatures/<int:id>", methods=["PUT"])
def update_temperature(id):
    
    return put_helper(request.get_json(silent=True), id, cursor, jsonToTemperature, execute_update_temperature, db_connection)

### DELETE ROUTES ###

@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_country(id):

    return delete_helper(id, cursor, Constants.TARI_TABLE, db_connection)

@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_city(id):

    return delete_helper(id, cursor, Constants.ORASE_TABLE, db_connection)

@app.route("/api/temperatures/<int:id>", methods=["DELETE"])
def delete_temperature(id):

    return delete_helper(id, cursor, Constants.TEMPERATURI_TABLE, db_connection)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

    db_connection.close()

