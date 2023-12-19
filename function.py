from flask import render_template, request  # import the 'render_template' and 'request' modules from the Flask framework.
import sqlite3  # import the sqlite3 module, which provides a lightweight disk-based database

# function for connecting to the database
def connect(db):
    connetion = sqlite3.connect(db)         # creates a connection to the SQLITE database name passed as an argument
    connetion.row_factory = sqlite3.Row     # the row type is set as an object of type sqlite3.Row
    return connetion                        # the connection thus created is returned
# ----------------------------------------------------------------

# function to check if a registered user already exists with the email passed as argument
def username_already_exists(email):
    connection = connect("database.db")                                     # a connection is established to the database called "database.db"
    cursor = connection.cursor()                                            # a cursor object is created to execute queries
    cursor.execute("SELECT * FROM Utenti WHERE emailUtente = ?", (email,))  # the query is executed to see if a user already exists with the email passed as argument
    connection.commit()                                                     # the changes generated by the previous query are committed
    return cursor.fetchone() is not None                                    # if the query returned at least one entry then the user with that email already exists, so it returns True
# ----------------------------------------------------------------

# function to check if there is already a registered user with the phone number passed as argument
def phone_already_exists(phone):
    connection = connect("database.db")                                         # a connection is established to the database called "database.db"
    cursor = connection.cursor()                                                # a cursor object is created to execute queries
    cursor.execute("SELECT * FROM Utenti WHERE telefonoUtente = ?", (phone,))   # the query is executed to see if a user already exists with the number phone passed as argument
    connection.commit()                                                         # the changes generated by the previous query are committed
    return cursor.fetchone() is not None                                        # if the query returned at least one entry then the user with that phone already exists, so it returns True
# ----------------------------------------------------------------

# function to check if user "X" has already entered a trip with the same criteria 
def trip_already_exists(_idUtente,start_pos,start_lat,start_lng,posti, timestamp):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to check if a trip already exists with those parameters (therefore if that user has already planned that trip with those parameters)
    cursor.execute("SELECT * FROM Viaggi WHERE _idUtente = ? AND indirizzoPartenza = ? AND lat_Partenza = ? AND lon_Partenza = ? AND postiDisponibili = ? AND time_stamp = ?", 
                   (_idUtente,start_pos,start_lat,start_lng,posti,timestamp))
    connection.commit()                     # the changes generated by the previous query are committed
    return cursor.fetchone() is not None    # if the query returned at least one entry then a trip with this info already exists, so it returns True
# ----------------------------------------------------------------

# function to check if there is a trip nearby (1000m)
def trip_exists(_idUtente,user_lat,user_lng):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries
    
    # query to check if there is a driver within 1km of the user's location
    query = """
                SELECT *
                FROM Viaggi v JOIN Tracking t ON v._idUtente = t._idUtente
                WHERE
                ((SQRT(POW((t.lat - ?), 2) + POW((t.lon - ?), 2)) * 111000) <= 1000) AND
                v._idUtente != ? AND 
                postiDisponibili > 0 AND 
                Stato = 'In Corso...' AND 
                NOT EXISTS (
                    SELECT 1
                    FROM RichiestePassaggio
                    WHERE v.idViaggio = RichiestePassaggio._idViaggio AND RichiestePassaggio._idUtente = ?
                )
        """
    cursor.execute(query, (user_lat,user_lng,_idUtente, _idUtente)) # the query is executed
    connection.commit()                     # the changes generated by the previous query are committed
    return cursor.fetchone() is not None    # if the query returned at least one entry then exist a user who is within 1000 meters is eligible to give a lift, so it returns True
# ----------------------------------------------------------------

#function to check that a user is not booking a ride for which he has already made a request
def ride_already_exits(_id_Viaggio, _idUtente):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to check if there is already an accepted ride request for that trip to that user
    query = """
                SELECT * FROM RichiestePassaggio
                WHERE
                _idViaggio = ? AND _idUtente = ? AND (Stato = 'Accettato' OR Stato = 'In Attesa')
            """
    cursor.execute(query, (_id_Viaggio, _idUtente)) # the query is executed
    connection.commit()                     # the changes generated by the previous query are committed
    return cursor.fetchone() is not None    # if the query returned at least one entry then already exist a for that trip, so it returns True
# ----------------------------------------------------------------

# function to verify that a user with these credentials exists
def get_user(username, password):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # the query is executed to check if a user exists with the email and password passed as arguments
    cursor.execute("SELECT * FROM Utenti WHERE emailUtente = ? AND passwordUtente = ?", (username, password))
    connection.commit()                     # the changes generated by the previous query are committed
    return cursor.fetchone()                # if the query returned at least one entry then already exist a for that trip, so it returns True
# ----------------------------------------------------------------

# function that returns all trips made by the user
def get_user_trips(user_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # the query is executed to get all the trips taken by the user
    cursor.execute("SELECT * FROM Viaggi WHERE _idUtente = ? ORDER BY indirizzoPartenza", (user_id,))
    connection.commit()                     # the changes generated by the previous query are committed
    trips = cursor.fetchall()               # all trips made by the user are obtained
    connection.close()                      # the connection is closed
    return trips                            # the list of trips made by the user is returned
# ----------------------------------------------------------------

# function that returns all the passage requests made by the user
def get_user_rides(user_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to get all the ride requests made by the user
    query = """
                SELECT *
                FROM RichiestePassaggio
                JOIN Viaggi ON RichiestePassaggio._idViaggio = Viaggi.idViaggio
                WHERE RichiestePassaggio._idUtente = ?;
            """
    cursor.execute(query, (user_id,))   # the query is executed
    connection.commit()                 # the changes generated by the previous query are committed
    rides = cursor.fetchall()           # all ride requests by the user are obtained
    connection.close()                  # the connection is closed
    return rides                        # the list of rides requests by the user is returned
# ----------------------------------------------------------------

# function to delete a trip given its id
def delete_trip(trip_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to get all switch requests made by the user
    cursor.execute("DELETE FROM RichiestePassaggio WHERE _idViaggio = ?;", (trip_id,))  # the query is executed to remove in cascade, the ride requests for the trip with that id
    cursor.execute("DELETE FROM Viaggi WHERE idViaggio = ?;", (trip_id,))               # only then is the query executed to remove a trip with that id
    connection.commit() # the changes generated by the previous queries are committed
    connection.close()  # the connection with database is closed
# ----------------------------------------------------------------

# function to delete a pass request given its id
def delete_ride(ride_id):
    connection = connect("database.db")         # a connection is established to the database called "database.db"
    cursor = connection.cursor()                # a cursor object is created to execute queries

    _idUtente = request.cookies.get('idUtente') # the user id who made the request is retrieved
    cursor.execute("UPDATE Viaggi SET postiDisponibili = postiDisponibili + 1 WHERE idViaggio = ?", ( ride_id, ))   # the query is executed to update the number of available seats before canceling the request
    cursor.execute("DELETE FROM RichiestePassaggio WHERE _idViaggio = ? AND _idUtente = ?", (ride_id,_idUtente))    # the query to remove step request with that id and user id is executed
    connection.commit() # the changes generated by the previous queries are committed
    connection.close()  # the connection with database is closed
# ----------------------------------------------------------------

# function to end a trip given its id
def end_trip(trip_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries
    
    print(trip_id) # DEBUG

    # if the trip with that id has already been accepted
    if trip_already_ended(trip_id):
        connection.close()  # the connection with database is closed
        return 
    else:
        cursor.execute("UPDATE Viaggi SET Stato = 'Concluso' WHERE idViaggio = ?", ( trip_id, ))    # removal of an available seat for that trip
        connection.commit() # the changes generated by the previous queries are committed
        connection.close()  # the connection with database is closed
        return
# ----------------------------------------------------------------

# function to check if that particular trip already exists
def trip_already_ended(trip_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to check if that trip has already been marked as 'Conluso'
    query = """
                SELECT * FROM Viaggi
                WHERE
                idViaggio = ? AND Stato = 'Concluso'
            """
    cursor.execute(query, (trip_id, ))      # the query is executed
    connection.commit()                     # the changes generated by the previous queries are committed
    return cursor.fetchone() is not None    # if the query returned at least one entry then that trip has already been marked as 'Conluso', therefore it returns True
# ----------------------------------------------------------------

# function to get all trips waiting to be accepted
def get_notifications():
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    _idUtente = request.cookies.get('idUtente') # the user id is retrieved by the cookie

    # query to find all trips for that user who is yet to accept
    query = """ SELECT * 
                FROM Viaggi v JOIN RichiestePassaggio r ON v.idViaggio = r._idViaggio
                WHERE r.Stato = 'In Attesa' AND v._idUtente = ?
            """
    cursor.execute(query, (_idUtente,)) # the query is executed
    connection.commit()                 # the changes generated by the previous queries are committed
    result = cursor.fetchall()          # all notifications are retrieved (requests waiting to be accepted)
    connection.close()                  # the connection with database is closed
    return result                       # notifications are returned
# ----------------------------------------------------------------

# function to get the number of trips waiting to be accepted
def get_notifications_number():
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    _idUtente = request.cookies.get('idUtente') # the user id is retrieved by the cookie

    # query to count the number of all trips for that user who is yet to accept
    query = """ SELECT COUNT(*) as n
                FROM Viaggi v JOIN RichiestePassaggio r ON v.idViaggio = r._idViaggio
                WHERE r.Stato = 'In Attesa' AND v._idUtente = ?
            """
    cursor.execute(query, (_idUtente,)) # the query is executed
    connection.commit()                 # the changes generated by the previous queries are committed
    result = cursor.fetchone()[0]       # the number of all notifications is retrieved (requests waiting to be accepted)
    connection.close()                  # the connection with database is closed
    return result                       # notifications are returned
# ----------------------------------------------------------------

# function to accept the handover request
def accept_request_byID(req_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to update the status of a given request to 'Accettato'
    cursor.execute("UPDATE RichiestePassaggio SET Stato = 'Accettato' WHERE idRichiestaPassaggio = ? ", (req_id,))  # the query is executed to update the status of the request
    connection.commit()                 # the changes generated by the previous queries are committed
    connection.close()                  # the connection with database is closed
    return
# ----------------------------------------------------------------

# function to refuse the passage request
def reject_request_byID(req_id):
    connection = connect("database.db")     # a connection is established to the database called "database.db"
    cursor = connection.cursor()            # a cursor object is created to execute queries

    # query to update the status of a given request to 'Rifiutato'
    cursor.execute("UPDATE RichiestePassaggio SET Stato = 'Rifiutato' WHERE idRichiestaPassaggio = ? ", (req_id,))      # the query is executed to update the status of the request
    cursor.execute("SELECT _idViaggio FROM RichiestePassaggio WHERE idRichiestaPassaggio = ?", (req_id,))               # the query is executed to obtain the trip related to the request
    _idViaggio = cursor.fetchone()[0]  # the first entry of the result table is obtained
    print(_idViaggio)   # DEBUG
    cursor.execute("UPDATE Viaggi SET postiDisponibili = postiDisponibili + 1 WHERE idViaggio = ?", ( _idViaggio, ))   # the query is executed to update the number of available seats since the request was rejected
    connection.commit()                 # the changes generated by the previous queries are committed
    connection.close()                  # the connection with database is closed
    return
# ----------------------------------------------------------------