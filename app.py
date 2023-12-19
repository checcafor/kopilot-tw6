# we add the modules necessary for the web app to function
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3                      # import sqlite3 module
from datetime import date, datetime # import datetime module
import hashlib                      # import hashlib module to encrypt the password
from function import *              # import all functions from function
from forms import SingupForm, LoginForm, InfoForm, TakeForm, GiveForm   # import custom classes from form

#
import threading                # import the 'threading' module for multi-threading support and custom modules.
from position_server import *   # import all function from position_server module
#

# the application is initialized (creates an instance of the Flask application)
app = Flask(__name__)

# a secret key is set for the application (mostly for cookies)
app.secret_key = 'secret_key'

# ----------------------- INDEX DECORATOR -----------------------
@app.route("/") # if this path is specified in the URL
def index():
    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is logged in
    if is_user_authenticated:   
        return redirect(url_for("home"))        # is redirected to your reserved area  
    else:
        return render_template("index.html")    # otherwise the index is shown
# ----------------------------------------------------------------

# ----------------------- LOGIN DECORATOR -----------------------
@app.route("/login", methods=("GET","POST")) # if this path is specified in the URL, whether via GET or POST method
def login():
    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is logged in
    if is_user_authenticated:   
        return redirect(url_for("home"))        # is redirected to your reserved area 
    
    login_form = LoginForm()    # an object of type LoginForm is created to initialize the login form

    # if the request method is of type "POST"
    if request.method == 'POST' and login_form.validate_on_submit():

        email = str(login_form.email.data)          # the email is retrieved from the form making sure it is a string (converting to a string)
        password = str(login_form.password.data)    # the password is recovered from the form making sure it is a string (converting to a string)
        rememberme = login_form.rememberme.data     # the user's desire to remain logged in or not is retrieved
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # the password is encrypted via sha256, which is irreversible
        user_info = get_user(email, hashed_password)    # the function is called to search for a user in the database with these credentials

        # if the user with these combinations exists, then if user_info is not null     
        if user_info:
            response = make_response(redirect(url_for("home")))                         # viene creata una risposta HTTP che reindirizza il client alla route "home"
            if rememberme:                                                              # if the user wants to stay logged in
                response.set_cookie('auth', 'true', max_age=31536000)                   # a cookie is set to indicate that the user is logged in, it will last one year from the last login unless logged out
                response.set_cookie('idUtente', f"{user_info[0]}", max_age=31536000)    # a cookie is set to indicate the user ID who logged in, it will last one year from the last login unless logged out
                response.set_cookie('nomeUtente', f"{user_info[1]}", max_age=31536000)  # a cookie is set to indicate the user name that logged in, it will last one year from the last login unless you log out
            else: 
                response.set_cookie('auth', 'true', max_age = None)                     # a cookie is set to indicate that the user is logged in, it will last until the end of the session (i.e. until the user logs out)
                response.set_cookie('idUtente', f"{user_info[0]}", max_age= None)       # a cookie is set to indicate the logged in user ID, it will last until the end of the session (i.e. until the user logs out)
                response.set_cookie('nomeUtente', f"{user_info[1]}", max_age = None)    # a cookie is set to indicate the username who logged in, it will last until the end of the session (i.e. until the user logs out)
            return response                                                             # HTTP response is returned
        else:
            # if the user_info variable is null, it means that the user you are trying to log in for does not exist,
            # so the credentials are wrong, so we return the user to the login page showing the error
            return render_template("login.html", error = "credenziali errate, per favore riprova", message = None, form = login_form)

    else:
        # if the request method is of type "GET" it means that the user is simply accessing the login page, so we render the login page
        return render_template("login.html", message = None, error = None, form = login_form)
# ----------------------------------------------------------------

# ----------------------- SINGUP DECORATOR -----------------------
@app.route("/signup", methods=("GET","POST"))   # if this path is specified in the URL, whether via GET or POST method
def signup():

    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is logged in
    if is_user_authenticated:   
        return redirect(url_for("home"))        # is redirected to your reserved area 
    
    singup_form = SingupForm()   # an object of type SingupForm is created to initialize the singup form
    login_form = LoginForm()     # an object of type LoginForm is created to initialize the login form

    # if the request method is of type "POST"
    if request.method == 'POST' and singup_form.validate_on_submit():  
        name = str(singup_form.name.data)            # the name is retrieved from the form making sure it is a string (converting to a string)
        lastname = str(singup_form.lastname.data)    # the surname is retrieved from the form making sure it is a string (converting to a string)
        phone = str(singup_form.phone.data)          # the telephone number is retrieved from the form
        email = str(singup_form.email.data)          # the email is retrieved from the form making sure it is a string (converting to a string)
        password = str(singup_form.password.data)    # the password is recovered from the form making sure it is a string (converting to a string)

        print("debug")

        # if a user with that email already exists
        if username_already_exists(email):
            # the singup page is rendered with an error message
            return render_template("signup.html", message='la mail che sta cercando di inserire è già stata usata per un altro profilo utente', form = singup_form)
        # if a user with that phone number already exists
        elif phone_already_exists(phone):
            # the singup page is rendered with an error message
            return render_template("signup.html", message='il telefono che sta cercando di inserire è già stato usato per un altro profilo utente', form = singup_form)
        else:
            # otherwise it means that no user exists with that email or telephone number, so we proceed to register it
            connection = connect("database.db")                                     # a connection is established to the database called "database.db"
            cursor = connection.cursor()                                            # a cursor object is created to execute queries
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # the password is encrypted via sha256, which is irreversible
            # the user is then registered in the database with the credentials entered in the form
            cursor.execute("INSERT INTO Utenti (nomeUtente,cognomeUtente,emailUtente,passwordUtente,telefonoUtente) VALUES (?, ?, ?, ?, ?)", (name,lastname,email,hashed_password,phone))

            cursor.execute("SELECT idUtente FROM Utenti WHERE emailUtente = ? AND telefonoUtente = ?", (email,phone))   # the ID of the user just inserted into the database is obtained
            _idUtente = cursor.fetchone()[0]    # the user id who registered is retrieved from the result of the previous query
            default = 0                         # default value for latitude and longitude
            timestamp = datetime.now()          # timestamp for the actual date 
            # a default tracking entry is inserted for that user
            cursor.execute("INSERT INTO Tracking (lat,lon,time_stamp,_idUtente) VALUES (?, ?, ?, ?)", (default,default,timestamp,_idUtente))    # inserimao una tupla nella tabella relativa al tracking

            connection.commit() # the changes generated by the previous query are committed
            connection.close()  # the connection is closed
            # you will be redirected to the login page with a message confirming your registration
            return render_template('login.html', message = "Registrazione eseguita con successo, procedi al login", error = None, form = login_form)
    else:
        # if the request is instead of type "GET", it means that the user is simply accessing the signup page for the first time, so we render the signup page
        return render_template("signup.html", message = None, form = singup_form)
# ----------------------------------------------------------------

# ----------------------- HOME DECORATOR ------------------------
@app.route("/home") # if this path is specified in the URL
def home():
    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index

    # is rendered to the home page
    return render_template("home.html") 
# ----------------------------------------------------------------

# ----------------------- HISTORY DECORATOR ------------------------
@app.route("/history") # if this path is specified in the URL
def history():
    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index

    _idUtente = request.cookies.get('idUtente') # the logged in user ID is retrieved
    user_trips = get_user_trips(_idUtente)      # call to get trips scheduled by the user
    user_rides = get_user_rides(_idUtente)      # call to get the steps requested by the user

    notificationsNumber = get_notifications_number()    # the number of notifications from the logged in user is retrieved
    notifications = get_notifications()                 # notifications of the logged in user are retrieved

    # is rendered to the history page with the information of the planned trips and steps requested by the logged in user and also the notifications
    return render_template("history.html", trips=user_trips, rides = user_rides, notificationsNumber = notificationsNumber, notifications = notifications) 
# ----------------------------------------------------------------

# ------------------- DELETE TRIP DECORATOR ----------------------
@app.route("/delete_trip/<int:trip_id>", methods=["POST"]) # if this path is specified in the URL by POST method
def delete_trip_route(trip_id):
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    delete_trip(trip_id)    # call to delete the selected trip

    return redirect(url_for('home')) # the home is rendered
# ----------------------------------------------------------------

# ------------------ DELETE RIDE DECORATOR -----------------------
@app.route("/delete_ride/<int:ride_id>", methods=["POST"]) # if this path is specified in the URL by POST method
def delete_ride_route(ride_id):
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    delete_ride(ride_id)    # call to delete the selected ride request

    return redirect(url_for('home'))  # the home is rendered
# ----------------------------------------------------------------

# ---------------- REQUEST RIDE DECORATOR ------------------------
@app.route("/request_ride/", methods=["POST"]) # if this path is specified in the URL by POST method
def request_ride_route():
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    take_form = TakeForm()  # an object of type TakeForm is created to initialize the take a ride form
    
    ride_id = request.form.get('ride')              # it is retrieved from the i-th form for which trip you want to make the request
    startAddress = request.form.get('startPos')     # the starting address is recovered
    destAddress = request.form.get('destPos')       # the destination address is retrieved
    latAddress = request.form.get('destLat')        # the destination latitude is retrieved
    lonAddress = request.form.get('destLon')        # the destination longitude is retrieved
    
    connection = connect("database.db")         # a connection is established to the database called "database.db"
    cursor = connection.cursor()                # a cursor object is created to execute queries
    _idUtente = request.cookies.get('idUtente') # the user id who made the request is retrieved

    # if a ride request already exists with that id and user id
    if ride_already_exits(ride_id, _idUtente):
        connection.close()  # the connection is closed and we return the same page but with an error
        return render_template("take.html", error='Hai già prenotato questo Passaggio', message = None, selected_trip = None, form = take_form)
    else:
        cursor.execute("INSERT INTO RichiestePassaggio (_idViaggio, _idUtente, indirizzoPartenzaRider, indirizzoArrivo, lat_Arrivo, lon_Arrivo, Stato) VALUES (?,?,?,?,?,?,?);", ( ride_id, _idUtente, startAddress, destAddress, latAddress, lonAddress, "In Attesa")) # query to add a ride request waiting to be accepted to the db
        cursor.execute("UPDATE Viaggi SET postiDisponibili = postiDisponibili - 1 WHERE idViaggio = ?", ( ride_id, ))                       # removing an available seat for that trip
        connection.commit() # the changes generated by the previous query are committed
        connection.close()  # the database connection is closed
        # the same page is returned with a message confirming the request
        return render_template('take.html', message = "Passaggio richiesto con successo", error = None, form = take_form)
# ----------------------------------------------------------------

# --------------------- END TRIP DECORATOR -----------------------
@app.route("/end_trip/<int:trip_id>", methods=["POST"]) # if this path is specified in the URL by POST method
def end_trip_route(trip_id):
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    end_trip(trip_id) # call to end the selected trip

    # redirected to the page for the passage request with message confirming the request
    return render_template('home.html', message = "Viaggio terminato con successo", error = None)
# ----------------------------------------------------------------

# ----------------------- GIVE DECORATOR -------------------------
@app.route("/give", methods=("GET","POST")) # if this path is specified in the URL by POST method
def give():
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    give_form = GiveForm() # an object of type GiveForm is created to initialize the give a ride form
    
    # if the request method is "POST" and all input in the form are valid
    if request.method == 'POST' and give_form.validate_on_submit():
        
        start_pos = str(give_form.startPos.data)    # the starting address is retrieved from the form
        start_lat = str(give_form.startLat.data)    # the starting latitude is retrieved from the form
        start_lng = str(give_form.startLng.data)    # the starting longitude is retrieved from the form
        posti = str(give_form.seats.data)           # the number of seats available for this trip is retrieved from the form
        _idUtente = request.cookies.get('idUtente') # the user ID who is registering the trip is retrieved

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # the trip registration date is obtained

        # if there is already a trip booked with the same information
        if trip_already_exists(_idUtente,start_pos,start_lat,start_lng, posti,timestamp):
            # the same page is returned with an error message
            return render_template("give.html", message = None, form = give_form, error='Il viaggio che stai cercando di inserire, è già stato registrato')
        else:
            connection = connect("database.db")     # a connection is established to the database called "database.db"
            cursor = connection.cursor()            # a cursor object is created to execute queries
            # registration in the trip database
            cursor.execute("INSERT INTO Viaggi (_idUtente,indirizzoPartenza,lat_Partenza,lon_Partenza,time_stamp,postiDisponibili, Stato) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           (_idUtente,start_pos,start_lat,start_lng,timestamp,posti, "In Corso..."))
            connection.commit() # the changes generated by the previous query are committed
            connection.close()  # the database connection is closed
            # the same page is returned with a message confirming registration
            return render_template('give.html', message = "Viaggio registrato con successo", form = give_form, error = None)
    else:
        # if the request method is "GET" it means that the user is simply accessing the page
        return render_template("give.html", message = None, form = give_form, error = None)
# ----------------------------------------------------------------

# ----------------------- TAKE DECORATOR -------------------------    
@app.route("/take", methods=("GET","POST")) # if this path is specified in the URL, whether via GET or POST method
def take():
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    take_form = TakeForm() # an object of type TakeForm is created to initialize the take a ride form

    # if the request method is "POST" and all input in the form are valid
    if request.method == 'POST' and take_form.validate_on_submit():

        user_pos = str(take_form.startPos.data)             # the position where the user is located is retrieved from the form  
        user_lat = str(take_form.startLat.data)             # the starting latitude is retrieved from the form
        user_lng = str(take_form.startLng.data)             # the starting longitude is retrieved from the form
        destination_pos = str(take_form.endPos.data)        # the destination address is retrieved from the form
        destination_lat = str(take_form.endLat.data)        # the destination latitude is retrieved from the form
        destination_lng =  str(take_form.endLng.data)       # the destination longitude is retrieved from the form
        
        _idUtente = request.cookies.get('idUtente')         # the user id making the request is retrieved

        # if there are no drivers eligible to grant a ride because they are not within a 1000m radius of where the user requesting it is located
        if not trip_exists(_idUtente,user_lat, user_lng):
            # the same page is returned with an error
            return render_template("take.html", error='Nessun viaggio con i criteri richiesti nelle vicinanze', message = None, selected_trip = None, form = take_form)
        else:
            # if instead there is a driver eligible for the passage
            connection = connect("database.db")     # a connection is established to the database called "database.db"
            cursor = connection.cursor()            # a cursor object is created to execute queries
            
            # query to get trips filtered by distance (1km radius between driver and rider)
            query = """
                    SELECT *, (SQRT(POW((t.lat - ?), 2) + POW((t.lon - ?), 2)) * 111000) as distanza_assoluta
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
                    ORDER BY distanza_assoluta ASC;
            """
            # the query is executed
            cursor.execute(query, (user_lat,user_lng,user_lat,user_lng,_idUtente, _idUtente))

            # ----------------------------------------------------------------
            available_trips = cursor.fetchall() # all the entries returned from the query are obtained and inserted into the "available_trips" variable

            # data structure containing the information of the user who wants to request a ride
            request_info = {
                "starting_address": user_pos,           # rider's starting position
                "destination_address": destination_pos, # rider's destination position
                "lat": destination_lat,                 # rider's destination latitude
                "lon": destination_lng                  # rider's destination longitude
            }

            connection.commit() # the changes generated by the previous query are committed
            connection.close()  # the database connection is closed
            # the same page is returned with compatible trips for which you can request a ride
            return render_template('take.html', available_trips = available_trips, error = None, message = None, form = take_form, request_info = request_info)
    else:
        # if the request method is "GET", then the user is simply accessing the page
        return render_template("take.html", error = None, form = take_form, message = None)
# ----------------------------------------------------------------

# ------------------------ PROFILE DECORATOR ------------------------
@app.route("/profile", methods=("GET","POST")) # if this path is specified in the URL, whether via GET or POST method
def profile():
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    form = InfoForm() # an object of type InfoForm is created to initialize the user's info form

    _idUtente = request.cookies.get("idUtente") # the user ID is retrieved from cookies to load his information into the forms

    connection = connect("database.db")                                     # a connection is established to the database called "database.db"
    cursor = connection.cursor()                                            # a cursor object is created to execute queries
    cursor.execute("SELECT * FROM Utenti WHERE idUtente = ?", (_idUtente,)) # we select the user information
    user_info = cursor.fetchone()                                           # the user information is inserted into a "user_info" variable
    
    # if the request method is "POST" and all input in the form are valid
    if request.method == "POST" and form.validate_on_submit():

        name = str(form.name.data)            # the name is retrieved from the form making sure it is a string (converting to a string)
        lastname = str(form.lastname.data)    # the surname is retrieved from the form making sure it is a string (converting to a string)
        phone = str(form.phone.data)          # the telephone number is retrieved from the form
        email = str(form.email.data)          # the email is retrieved from the form making sure it is a string (converting to a string)
        password = str(form.password.data)    # the password is recovered from the form making sure it is a string (converting to a string)
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # the password is encrypted via sha256

        # a query is performed to see if the email he entered belongs to some other user than him
        cursor.execute("SELECT * FROM Utenti WHERE idUtente != ? AND emailUtente = ?", (_idUtente, email))
        user = cursor.fetchone()    # the first row of the returned table is obtained

        # if there is no user with this email just entered
        if not user:
            # we proceed to check whether the phone he entered belongs to some other user than him
            cursor.execute("SELECT * FROM Utenti WHERE idUtente != ? AND telefonoUtente = ?", (_idUtente, phone))
            user = cursor.fetchone()    # the first row of the returned table is obtained

            # if there is no user with this phone number just entered
            if not user:
                # a query is made to see if the information entered is the same as that already present in the database for that user
                cursor.execute("SELECT * FROM Utenti WHERE idUtente = ? AND nomeUtente = ? AND cognomeUtente = ? AND emailUtente = ? AND passwordUtente = ? AND telefonoUtente = ?", (_idUtente, name, lastname, email, hashed_password, phone))
                user = cursor.fetchone() # the first row of the returned table is obtained
                if user:    # if the user has not changed any parameters
                    connection.close()  # the database connection is closed
                    # the same page is returned, encouraging you, if necessary, to change the parameters to make a change
                    return render_template("profile.html", user_info = user_info, message = None, error = "Modifica qualche campo per rendere effettiva la modifica", form = form)
                else:   # if the user has changed at least one parameter
                    try:
                        # we then proceed to update the user information
                        cursor.execute("UPDATE Utenti SET nomeUtente = ?, cognomeUtente = ?, emailUtente = ?, passwordUtente = ?, telefonoUtente = ? WHERE idUtente = ?", (name, lastname, email, hashed_password, phone, _idUtente))
                        cursor.execute("SELECT * FROM Utenti WHERE idUtente = ?", (_idUtente,)) # this user information is obtained
                        user_info = cursor.fetchone()   # the first row of the returned table is obtained and inserted into a variable
                        connection.commit()             # the changes made by previous queries are confirmed
                        print("Aggiornamento riuscito") # DEBUG
                    except sqlite3.Error as e:
                        print("Errore durante l'aggiornamento:", e)  # DEBUG
                    finally:
                        connection.close()              # the database connection is closed
                    # the same page is returned showing a message that the user information has been modified
                    return render_template("profile.html", user_info = user_info, message = "Aggiornamento delle credenziali avventuo con successo", error = None, form = form)   
            else:
                # if there is at least one user with this phone number
                connection.close()  # the database connection is closed
                # the same page is returned showing an error message
                return render_template("profile.html", user_info = user_info, message = None, error = "Attenzione, questo numero di telefono è già stato utilizziato", form = form)
            
        else:
            # if there is at least one user with this email
            connection.close()  # the database connection is closed
            # the same page is returned showing an error message
            return render_template("profile.html", user_info = user_info, message = None, error = "Attenzione, questa mail è già stata utilizziata", form = form)
    
    else:
        # if the request method is "GET", then the user is simply accessing the page
        connection.close() # the database connection is closed, since we have already obtained the user information previously
        # the page is simply returned
        return render_template("profile.html", user_info = user_info, message = None, error = None, form = form)
# ----------------------------------------------------------------

# -------------------- NOTIFICATION DECORATOR --------------------
@app.route("/requests") # if this path is specified in the URL
def requests():
    # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    notifications = get_notifications()         # notifications of the logged in user are retrieved

    # the requests page is rendered with the notification data structure with them in it
    return render_template("requests.html", notifications = notifications) 
# ----------------------------------------------------------------

# ------------------  ACCEPT REQUEST DECORATOR -------------------
@app.route("/accept_ride/<int:req_id>", methods=["POST"]) # if this path is specified in the URL by POST method
def accept_request(req_id):
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    accept_request_byID(req_id)     # call the function to accept the ride request

    return render_template("notifications.html")    # the notifications page is rendered
# ----------------------------------------------------------------

# ------------------ REJECT REQUEST DECORATOR --------------------
@app.route("/reject_ride/<int:req_id>", methods=["POST"]) # if this path is specified in the URL by POST method
def reject_request(req_id):
     # if a cookie called "auth" exists and is set to "true" then it means that the user is logged in
    is_user_authenticated = request.cookies.get('auth') == 'true'
    # if the user is NOT logged in
    if not is_user_authenticated:
        return redirect(url_for('index'))       # is redirected to the index
    
    reject_request_byID(req_id)     # calls the function to reject the ride request

    return render_template("notifications.html")    # the notifications page is rendered
# ----------------------------------------------------------------

# ---------------------- LOGOUT DECORATOR ------------------------
@app.route('/logout') # if this path is specified in the URL
def logout():
    response = make_response(redirect(url_for('index')))    # an HTTP response is created
    response.delete_cookie('auth')                          # the cookie called "auth" is deleted
    response.delete_cookie('idUtente')                      # the cookie called "idUtente" is deleted
    response.delete_cookie('nomeUtente')                    # the cookie called "nomeUtente" is deleted
    return response
# ----------------------------------------------------------------

# ---------------------- ERROR HANDLER 404 -----------------------
@app.errorhandler(404) # if a request is made for a daecorator that does not exist
def page_not_found(error):
    # if you get a response from the server, with code "404"
    # it will render the page to show the 404 error, and warn the user that the page he is trying to access does not exist
    return render_template('404.html'), 404 
# ----------------------------------------------------------------

if __name__ == "__main__":  # if the application is run directly (and not as an imported module)

    t1 = threading.Thread(target=my_websocket_server)   # create a new thread and assign 'my_websocket_server' function as its target
    t1.start()  # strating the thread

    # the Flask application is executed (in particular we start the Flask server)
    app.run(debug = True,       # it is specified that debug mode is active
            host = HOST,        # it indicates that the application will be accessible from any address on the network   
            port = HTTP_PORT    # the port on which the application will be active is specified, i.e. 5000
        )      