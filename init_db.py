import sqlite3

connection = sqlite3.connect('loopkitchen.db')


with open('dbops.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()