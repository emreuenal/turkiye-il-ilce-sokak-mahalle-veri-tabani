import json
import datetime
from dbconfig.config import use_mariadb, use_postgresql, use_mongodb, use_sqlite
start_time = datetime.datetime.now()

if use_mariadb:
  from dbconfig.config import mdb_connection
  mdb_cursor = mdb_connection.cursor()

  # Create Tables 
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS iller (il_id INT PRIMARY KEY, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS ilceler (ilce_id INT PRIMARY KEY, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id INT PRIMARY KEY, mahalle_adi VARCHAR(255), ilce_id INT, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS sokaklar (sokak_id INT PRIMARY KEY, sokak_adi VARCHAR(255), mahalle_id INT, mahalle_adi VARCHAR(255), ilce_id INT, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")

  # Truncate old data IF EXISTS
  mdb_cursor.execute("TRUNCATE TABLE iller;")
  mdb_cursor.execute("TRUNCATE TABLE ilceler;")
  mdb_cursor.execute("TRUNCATE TABLE mahalleler;")
  mdb_cursor.execute("TRUNCATE TABLE sokaklar;")
  mdb_connection.commit() 

if use_postgresql:
  from dbconfig.config import pg_connection
  pg_cursor = pg_connection.cursor()

  # Create Tables 
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS iller (il_id integer PRIMARY KEY, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS ilceler (ilce_id integer PRIMARY KEY, ilce_adi varchar, il_id integer, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id integer PRIMARY KEY, mahalle_adi varchar, ilce_id integer, ilce_adi varchar, il_id integer, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS sokaklar (sokak_id integer PRIMARY KEY, sokak_adi varchar,mahalle_id integer, mahalle_adi varchar, ilce_id integer, ilce_adi varchar, il_id integer, il_adi varchar);")
  
  # Truncate old data IF EXISTS
  pg_cursor.execute("TRUNCATE TABLE iller;")
  pg_cursor.execute("TRUNCATE TABLE ilceler;")
  pg_cursor.execute("TRUNCATE TABLE mahalleler;")
  pg_cursor.execute("TRUNCATE TABLE sokaklar;")
  pg_connection.commit()


if use_mongodb:
  from dbconfig.config import mongodb

  # Drop old collections
  mongodb.iller.drop()
  mongodb.ilceler.drop()
  mongodb.mahalleler.drop()
  mongodb.sokaklar.drop()


if use_sqlite:
  from dbconfig.config import sqlite_connection
  sqlite_cursor = sqlite_connection.cursor()

  # Truncate old data IF EXISTS
  sqlite_cursor.execute("DROP TABLE iller;")
  sqlite_cursor.execute("DROP TABLE ilceler;")
  sqlite_cursor.execute("DROP TABLE mahalleler;")
  sqlite_cursor.execute("DROP TABLE sokaklar;")
  sqlite_connection.commit()

  # Create Tables 
  
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS iller (il_id integer PRIMARY KEY, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS ilceler (ilce_id integer PRIMARY KEY, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id integer PRIMARY KEY, mahalle_adi text, ilce_id integer, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS sokaklar (sokak_id interger PRIMARY KEY, sokak_adi text, mahalle_id integer, mahalle_adi text, ilce_id integer, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_connection.commit()

  

# Add iller to database
executemany_list= []
with open("iller.txt") as file:
    for iller in file:
        iller_list = json.loads(iller)
        print("Eklenecek İl Sayısı: " + str(len(iller_list)))
        for il in iller_list:
          il_id = il['il_id']
          il_adi = il['il_adi']
          executemany_list.append((il_id, il_adi))
          
          # Add one by one to mongo
          if use_mongodb:
            mongodb.iller.insert_one(
              { "_id": il_id },
              {
                "$setOnInsert": {"il_adi": il_adi}
              }
            )      
stmt = "INSERT INTO iller (il_id, il_adi) VALUES (%s, %s)"


print(len(executemany_list))
if use_mariadb:
  mdb_cursor.executemany(stmt, executemany_list)
  mdb_connection.commit()
if use_postgresql:
  pg_cursor.executemany(stmt, executemany_list)
  pg_connection.commit()
if use_sqlite:
  sqlite_cursor.executemany("INSERT INTO iller VALUES (?, ?)", executemany_list)
  sqlite_connection.commit()


# Add ilceler to database
executemany_list= []
with open("ilceler.txt") as file:
    for ilceler in file:
        ilceler_list = json.loads(ilceler)
        print(len(ilceler_list))
        for ilce in ilceler_list:
          ilce_id = ilce['ilce_id']
          ilce_adi = ilce['ilce_adi']
          il_id = ilce['il_id']
          il_adi = ilce['il_adi']
          executemany_list.append((ilce_id, ilce_adi, il_id, il_adi))
          if use_mongodb:
            mongodb.ilceler.insert_one(
              { "_id": ilce_id },
              {
                "$setOnInsert": {"ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
              }
            )
          print(len(executemany_list))
            
stmt = "INSERT INTO ilceler (ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s)"
print(len(executemany_list))
if use_mariadb:
  mdb_cursor.executemany(stmt, executemany_list)
  mdb_connection.commit()
if use_postgresql:
  pg_cursor.executemany(stmt, executemany_list)
  pg_connection.commit()
if use_sqlite:
  sqlite_cursor.executemany("INSERT INTO ilceler VALUES (?, ?, ?, ?)", executemany_list)
  sqlite_connection.commit()


# Add mahalleler to database
executemany_list= []
with open("mahalleler.txt") as file:
    for mahalleler in file:
        mahalleler_list = json.loads(mahalleler)
        print(len(mahalleler_list))
        for mahalle in mahalleler_list:
            mahalle_id = mahalle['mahalle_id']
            mahalle_adi = mahalle['mahalle_adi']
            ilce_id = mahalle['ilce_id']
            ilce_adi = mahalle['ilce_adi']
            il_id = mahalle['il_id']
            il_adi = mahalle['il_adi']
            executemany_list.append((mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
            if use_mongodb:
              mongodb.mahalleler.insert_one(
                { "_id": mahalle_id },
                {
                  "$setOnInsert": {"mahalle_adi": mahalle_adi, "ilce_id": ilce_id, "ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
                }
              )
            print(len(executemany_list))
stmt = "INSERT INTO mahalleler (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s)"
print(len(executemany_list))
if use_mariadb:
  mdb_cursor.executemany(stmt, executemany_list)
  mdb_connection.commit()
  print("Adding mahalleler to MySQL / MariaDB is Done!")
if use_postgresql:
  pg_cursor.executemany(stmt, executemany_list)
  pg_connection.commit()
  print("Adding mahalleler to PostgreSQL is Done!")
if use_sqlite:
  sqlite_cursor.executemany("INSERT INTO mahalleler VALUES (?, ?, ?, ?, ?, ?)", executemany_list)
  sqlite_connection.commit()
  print("Adding mahalleler to Sqlite is Done!")

  
# Add sokaklar to database
executemany_list= []
with open("sokaklar.txt") as file:
    for sokaklar in file:
        sokaklar_list = json.loads(sokaklar)
        print(len(sokaklar_list))
        for sokak in sokaklar_list:
            sokak_id = sokak['sokak_id']
            sokak_adi = sokak['sokak_adi']
            mahalle_id = sokak['mahalle_id']
            mahalle_adi = sokak['mahalle_adi']
            ilce_id = sokak['ilce_id']
            ilce_adi = sokak['ilce_adi']
            il_id = sokak['il_id']
            il_adi = sokak['il_adi']
            executemany_list.append((sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
            print(len(executemany_list))
            if use_mongodb:
              mongodb.sokaklar.insert_one(
                { "_id": sokak_id },
                {
                  "$setOnInsert": {"sokak_adi": sokak_adi, "mahalle_id": mahalle_id, "mahalle_adi": mahalle_adi, "ilce_id": ilce_id, "ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
                }
              )
stmt = "INSERT INTO sokaklar (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
print(len(executemany_list))
if use_mariadb:
  mdb_cursor.executemany(stmt, executemany_list)
  mdb_connection.commit()
  print("Adding sokaklar to MySQL / MariaDB is Done!")
if use_postgresql:
  pg_cursor.executemany(stmt, executemany_list)
  pg_connection.commit()
  print("Adding sokaklar to PostgreSQL is Done!")
if use_sqlite:
  sqlite_cursor.executemany("INSERT INTO sokaklar VALUES (?, ?, ?, ?, ?, ?, ?, ?)", executemany_list)
  sqlite_connection.commit()
  print("Adding sokaklar to Sqlite is Done!")

  




# Close DB Connections
if use_mariadb:
  if(mdb_connection):
    mdb_cursor.close()
    mdb_connection.close()
    print("MariaDB / MySQL connection is closed")

if use_postgresql:
  if(pg_connection):
    pg_cursor.close()
    pg_connection.close()
    print("PostgreSQL connection is closed")

if use_sqlite:
  if(sqlite_connection):
    sqlite_connection.close()
    print("Sqlite connection is closed")



stop_time = datetime.datetime.now()
duration = stop_time - start_time
print(duration)
print("DONE!")