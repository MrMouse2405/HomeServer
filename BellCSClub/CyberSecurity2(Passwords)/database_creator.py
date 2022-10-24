import sqlite3
import base64

db1 = sqlite3.connect("db1")
db1c = db1.cursor()

db1c.execute("CREATE TABLE IF NOT EXISTS passwords(user text,password text)")
db1c.execute("""
    INSERT INTO passwords VALUES
        ('edwardli','i learn scratch at UBC'),
        ('blitz','soobway'),
        ('mrmouse2405','cats are cool')
""")
db1.commit()

del db1, db1c

db2 = sqlite3.connect('db2')
db2c = db2.cursor()
db2c.execute("""
    CREATE TABLE IF NOT EXISTS passwords (user text,hashed_passwords text)
""")
db2c.executemany("""
    INSERT INTO passwords VALUES (?,?)
""", [
    ('edwardli',base64.b64encode('i learn scratch at UBC'.encode('ascii'))),
    ('blitz',base64.b64encode('soobway'.encode('ascii'))),
    ('mrmouse2405',base64.b64encode('cats are cool'.encode('ascii')))
])
db2.commit()

del db2, db2c