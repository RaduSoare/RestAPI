def insert_to_countries(cursor, db_connection, country):

    cursor.execute("insert into Tari (nume_tara, latitudine, longitudine) values (%s, %s, %s) returning id",
                   (country.name, country.lat, country.long))

    db_connection.commit()

    return cursor.fetchone()[0]