import sqlite3 # import the sqlite3 module, which provides a lightweight disk-based database

connection = sqlite3.connect("database.db") # establish a connection to the SQLite database file named "database.db"

# open the "database.sql" file and read its content
with open("database.sql") as f:
    connection.executescript(f.read())   # executes the SQL script from the file using executescript()
connection.commit() # commit the changes made to the database
connection.close()  # close the connection to the database