import sqlite3


"""Initializes a database"""
conn = sqlite3.connect('./employee.db')
conn.row_factory = sqlite3.Row
curs = conn.cursor()

curs.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        age INTEGER
    )
""")
