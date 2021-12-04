from flask import Flask
from flask import request, jsonify, Response
from psycopg2 import IntegrityError

def fetched_data_to_json_countries(countries_list):
    return list(map(lambda x: {"id" : x[0], "nume" : x[1], "lat" : x[2], "lon" : x[3]}, countries_list))

def fetched_data_to_json_cities(cities_list):
    return list(map(lambda x: {"id" : x[0], "idTara" : x[1] ,"nume" : x[2], "lat" : x[3], "lon" : x[4]}, cities_list))

def insert_to_countries(cursor, db_connection, country):

    cursor.execute("insert into Tari (nume_tara, latitudine, longitudine) values (%s, %s, %s) returning id",
                (country.name, country.lat, country.long))


    db_connection.commit()

    return cursor.fetchone()[0]

def insert_to_cities(cursor, db_connection, city):

    cursor.execute("insert into Orase (id_tara, nume_oras, latitudine, longitudine) values (%s, %s, %s, %s) returning id",
                   (city.countryID, city.name, city.lat, city.long))

    db_connection.commit()

    return cursor.fetchone()[0]

def insert_to_temperatures(cursor, db_connection, temperature):
    
    cursor.execute("insert into Temperaturi (id_oras, valoare, timestamp) values (%s, %s, %s) returning id",
                    (temperature.cityID, temperature.value, temperature.timestamp))

    db_connection.commit()

    return cursor.fetchone()[0]

def post_helper(params, cursor, db_connection, jsonToFunc, insertToFunc):
    if not params:
        return Response(status=400)

    new_entry = jsonToFunc(params)
    if new_entry is None:
        return Response(status=400)

    try:
        id = insertToFunc(cursor, db_connection, new_entry)
        return jsonify({'id': id})
    except IntegrityError as e:
        cursor.execute("ROLLBACK")
        db_connection.commit()
        return Response(status=409)

def get_helper(sql_command, cursor, fetchedDataToFunc):
    
    cursor.execute(sql_command)

    locations_list = cursor.fetchall()

    locations_json_list = fetchedDataToFunc(locations_list)

    return jsonify(locations_json_list)


def execute_update_country(cursor, country, id):
    cursor.execute("UPDATE TARI SET nume_tara=%s, latitudine=%s, longitudine=%s where id=%s returning id", (country.name, country.lat, country.long, id))

def execute_update_city(cursor, city, id):
    cursor.execute("UPDATE ORASE SET id_tara=%s, nume_oras=%s, latitudine=%s, longitudine=%s where id=%s returning id", (city.countryID, city.name, city.lat, city.long, id))

def execute_update_temperature(cursor, temperature, id):
    cursor.execute("UPDATE TEMPERATURI SET id_oras=%s, valoare=%s where id=%s returning id", (temperature.cityID, temperature.value, id))

def put_helper(params, id, cursor, jsonToFunc, executeUpdateFunc, db_connection):
    
    if not params:
        return Response(status=400)

    updated_data = jsonToFunc(params)
    if updated_data is None:
        return Response(status=400)
    
    executeUpdateFunc(cursor, updated_data, id)

    if cursor.fetchone() is None:
        return Response(status=404)

    db_connection.commit()
    return Response(status=200)

def delete_helper(id, cursor, table_name, db_connection):
    cursor.execute("DELETE FROM %s WHERE id=%s returning id" % (table_name, id,))

    if cursor.fetchone()[0] is None:
        return Response(status=404)
    
    db_connection.commit()
    return Response(status=200)
