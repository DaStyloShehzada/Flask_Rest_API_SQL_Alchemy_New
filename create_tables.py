import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY, USERNAME TEXT, PASSWORD TEXT)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS ITEMS (ID INTEGER PRIMARY KEY, NAME TEXT, PRICE REAL)"
cursor.execute(create_table)


connection.commit()
connection.close()