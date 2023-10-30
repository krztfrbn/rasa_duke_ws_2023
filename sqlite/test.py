import sqlite3

connection = sqlite3.connect("restaurant-20231024.db")

cursor = connection.cursor()

rows = cursor.execute("SELECT * FROM tables WHERE location = 'outside'").fetchall()
print(rows)
