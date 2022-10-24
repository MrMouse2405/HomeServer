import sqlite3
import base64

db1 = sqlite3.connect("db1")
db1c = db1.cursor()

response = db1c.execute("SELECT sql from sqlite_master").fetchall()
print('sqls: ',response)

response = db1c.execute("""
    SELECT user,password FROM passwords
""").fetchall()

print('\n\nUsername | Password\n')

for x in response:
    print(x[0],'|',x[1])

db2 = sqlite3.connect("db2")
db2c = db2.cursor()

response = db2c.execute("SELECT sql FROM sqlite_master").fetchall()
print("\n\n\nsqls:",response)

response = db2c.execute("""
    SELECT user,hashed_passwords FROM passwords
""").fetchall()

print('\n\nUsername | Password\n')

for x in response:
    print(x[0],'|',base64.b64decode(x[1]))
