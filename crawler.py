from bs4 import BeautifulSoup
import requests
import json
import datetime
from dbconfig.config import use_mariadb, use_postgresql, use_mongodb, use_sqlite, use_redis

if use_mariadb:
  from dbconfig.config import mdb_connection
if use_postgresql:
  from dbconfig.config import pg_connection
if use_mongodb:
  from dbconfig.config import mongodb
if use_sqlite:
  from dbconfig.config import sqlite_connection
if use_redis:
  from dbconfig.config import red


# We need:
# BeautifulSoup to get request_verification_token_header from a hidden input (view-source:https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu, line 685)
# requests to create requests and get response from urls
# json to load responses as json data
# datetime to determine crawlers run time
# psycopg2(in dbconfig) to create a connection to our postgresql database
# MySQLdb(in dbconfig) to create a connection to our MySQL/MariaDB database
# pymongo(in dbconfig) to create a connection to our mongodb database

if use_postgresql:
  pg_cursor = pg_connection.cursor()
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS iller (il_id integer PRIMARY KEY, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS ilceler (ilce_id integer PRIMARY KEY, ilce_adi varchar, il_id integer, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id integer PRIMARY KEY, mahalle_adi varchar, ilce_id integer, ilce_adi varchar, il_id integer, il_adi varchar);")
  pg_cursor.execute("CREATE TABLE IF NOT EXISTS sokaklar (sokak_id integer PRIMARY KEY, sokak_adi varchar,mahalle_id integer, mahalle_adi varchar, ilce_id integer, ilce_adi varchar, il_id integer, il_adi varchar);")
  pg_connection.commit()

if use_mariadb:
  mdb_cursor = mdb_connection.cursor()
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS iller (il_id INT PRIMARY KEY, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS ilceler (ilce_id INT PRIMARY KEY, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id INT PRIMARY KEY, mahalle_adi VARCHAR(255), ilce_id INT, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")
  mdb_cursor.execute("CREATE TABLE IF NOT EXISTS sokaklar (sokak_id INT PRIMARY KEY, sokak_adi VARCHAR(255), mahalle_id INT, mahalle_adi VARCHAR(255), ilce_id INT, ilce_adi VARCHAR(255), il_id INT, il_adi VARCHAR(255));")
  mdb_connection.commit()

if use_sqlite:
  sqlite_cursor = sqlite_connection.cursor()
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS iller (il_id integer PRIMARY KEY, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS ilceler (ilce_id integer PRIMARY KEY, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS mahalleler (mahalle_id integer PRIMARY KEY, mahalle_adi text, ilce_id integer, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS sokaklar (sokak_id interger PRIMARY KEY, sokak_adi text, mahalle_id integer, mahalle_adi text, ilce_id integer, ilce_adi text, il_id integer, il_adi text)''')
  sqlite_connection.commit()


response_count = 0
start_time = datetime.datetime.now()

    
    

main_url = "https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu"
r = requests.get(main_url)
response_count = response_count + 1
response = BeautifulSoup(r.text, "lxml")

#headers
request_verification_token_header = response.find(attrs={"name": "__RequestVerificationToken"}).attrs["value"]

#cookies
TS_cookie_key = r.cookies.keys()[0]
TS_cookie_value = r.cookies[TS_cookie_key]
request_verification_token_cookie = r.cookies['__RequestVerificationToken']




cookies = {
    '__RequestVerificationToken': request_verification_token_cookie,
    TS_cookie_key: TS_cookie_value,
}

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    '__RequestVerificationToken': request_verification_token_header,
    'Referer': 'https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu',
}

data = {
  
}

il_response = requests.post('https://adres.nvi.gov.tr/Harita/ilListesi', headers=headers, cookies=cookies, data=data)
response_count = response_count + 1
json_obj_iller = json.loads(il_response.text)

for il in json_obj_iller:
    il_id = il["kimlikNo"]
    il_adi = il["bilesenAdi"]
    print("İl ID: " + str(il_id) + ", " + "İl ADI: " + il_adi)
    
    if use_postgresql:
      pg_cursor.execute("INSERT INTO iller (il_id, il_adi) VALUES (%s, %s) ON CONFLICT (il_id) DO NOTHING", (il_id, il_adi))
      pg_connection.commit()
    
    if use_mariadb:
      mdb_cursor.execute("INSERT IGNORE INTO iller (il_id, il_adi) VALUES (%s, %s)", (il_id, il_adi))
      mdb_connection.commit()

    if use_mongodb:
      mongodb.iller.update_one(
        { "_id": il_id },
        {
          "$setOnInsert": {"il_adi": il_adi}
        },
        upsert=True
      )

    if use_sqlite:
      sqlite_cursor.execute('INSERT OR IGNORE INTO iller VALUES (?,?)', (il_id, il_adi) )

    if use_redis:
      red.hset('tr_adres:iller:' + str(il_id), 'il_adi', il_adi)
      
    
    data = {'ilKimlikNo': il["kimlikNo"]}
    response_ilce = requests.post('https://adres.nvi.gov.tr/Harita/ilceListesi', headers=headers, cookies=cookies, data=data)
    response_count = response_count + 1
    json_obj_ilceler = json.loads(response_ilce.text)
    for ilce in json_obj_ilceler:
        ilce_id = ilce["kimlikNo"]
        ilce_adi = ilce["bilesenAdi"]
        print("=" + "İl ADI: " + il_adi + ", " + "İlçe ID: " + str(ilce_id) + ", " + "İlçe ADI: " + ilce_adi)
        
        if use_postgresql:
          pg_cursor.execute("INSERT INTO ilceler (ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s) ON CONFLICT (ilce_id) DO NOTHING", (ilce_id, ilce_adi, il_id, il_adi))
          pg_connection.commit()
         
        if use_mariadb:
          mdb_cursor.execute("INSERT IGNORE INTO ilceler (ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s)", (ilce_id, ilce_adi, il_id, il_adi))
          mdb_connection.commit()
          
        if use_mongodb:
          mongodb.ilceler.update_one(
            { "_id": ilce_id },
            {
              "$setOnInsert": {"ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
            },
            upsert=True
          )

        if use_sqlite:
          sqlite_cursor.execute('INSERT OR IGNORE INTO ilceler VALUES (?,?,?,?)', (ilce_id, ilce_adi, il_id, il_adi) )

        if use_redis:
          dict_to_insert = {}
          dict_to_insert = {
            'ilce_adi': ilce_adi, 
            'il_id': il_id, 
            'il_adi': il_adi
          }
          red.hmset('tr_adres:ilceler:' + str(ilce_id), dict_to_insert)
        
        

        data = {'ilceKimlikNo': ilce["kimlikNo"]}
        response_mahallekoy = requests.post('https://adres.nvi.gov.tr/Harita/mahalleKoyBaglisiListesi', headers=headers, cookies=cookies, data=data)
        response_count = response_count + 1
        json_obj_mahallekoy = json.loads(response_mahallekoy.text)
        for mahallekoy in json_obj_mahallekoy:
            mahalle_id = mahallekoy["kimlikNo"]
            mahalle_adi = mahallekoy["bilesenAdi"]
            print("==" + "İl ADI: " + il_adi + ", " + "İlçe ADI: " + ilce_adi + ", " + "Mahalle ID: " + str(mahalle_id) + ", " + "Mahalle ADI: " + mahalle_adi)
            
            if use_postgresql:
              pg_cursor.execute("INSERT INTO mahalleler (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (mahalle_id) DO NOTHING", (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
              pg_connection.commit()
            
            if use_mariadb:
              mdb_cursor.execute("INSERT IGNORE INTO mahalleler (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s)", (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
              mdb_connection.commit()

            if use_mongodb:
              mongodb.mahalleler.update_one(
                { "_id": mahalle_id },
                {
                  "$setOnInsert": {"mahalle_adi": mahalle_adi, "ilce_id": ilce_id, "ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
                },
                upsert=True
              )

            if use_sqlite:
              sqlite_cursor.execute('INSERT OR IGNORE INTO mahalleler VALUES (?,?,?,?,?,?)', (mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) )

            if use_redis:
              dict_to_insert = {}
              dict_to_insert = {
                'mahalle_adi': mahalle_adi, 
                'ilce_id': ilce_id, 
                'ilce_adi': ilce_adi, 
                'il_id': il_id, 
                'il_adi': il_adi
              }
              red.hmset('tr_adres:mahalleler:' + str(mahalle_id), dict_to_insert)
            

            data = {'mahalleKoyBaglisiKimlikNo': mahallekoy["kimlikNo"]}
            response_yolListesi = requests.post('https://adres.nvi.gov.tr/Harita/yolListesi', headers=headers, cookies=cookies, data=data)
            response_count = response_count + 1
            json_obj_yolListesi = json.loads(response_yolListesi.text)
            for yol in json_obj_yolListesi:
                sokak_id = yol["kimlikNo"]
                sokak_adi = yol["bilesenAdi"]
                print("===" + "İl ADI: " + il_adi + ", "+ "İlçe ADI: " + ilce_adi + ", " + "Mahalle ADI: " + mahalle_adi + ", "  + "Yol ID: " + str(yol["kimlikNo"]) + ", " + "Yol ADI: " + yol["bilesenAdi"])
                
                if use_postgresql:
                  pg_cursor.execute("INSERT INTO sokaklar (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (sokak_id) DO NOTHING", (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
                  pg_connection.commit()
                
                if use_mariadb:
                  mdb_cursor.execute("INSERT IGNORE INTO sokaklar (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi))
                  mdb_connection.commit()

                if use_mongodb:
                  mongodb.sokaklar.update_one(
                    { "_id": sokak_id },
                    {
                      "$setOnInsert": {"sokak_adi": sokak_adi, "mahalle_id": mahalle_id, "mahalle_adi": mahalle_adi, "ilce_id": ilce_id, "ilce_adi": ilce_adi, "il_id": il_id, "il_adi": il_adi}
                    },
                    upsert=True
                  )

                if use_sqlite:
                  sqlite_cursor.execute('INSERT OR IGNORE INTO sokaklar VALUES (?,?,?,?,?,?,?,?)', (sokak_id, sokak_adi, mahalle_id, mahalle_adi, ilce_id, ilce_adi, il_id, il_adi) )

                if use_redis:
                  dict_to_insert = {}
                  dict_to_insert = {
                    'sokak_adi': sokak_adi, 
                    'mahalle_id': mahalle_id, 
                    'mahalle_adi': mahalle_adi, 
                    'ilce_id': ilce_id, 
                    'ilce_adi': ilce_adi, 
                    'il_id': il_id, 
                    'il_adi': il_adi
                  }
                  red.hmset('tr_adres:sokaklar:' + str(sokak_id), dict_to_insert)
                
    
stop_time = datetime.datetime.now()
duration = stop_time - start_time


if use_postgresql:
  if(pg_connection):
    pg_cursor.close()
    pg_connection.close()
    print("PostgreSQL connection is closed")

if use_mariadb:
  if(mdb_connection):
    mdb_cursor.close()
    mdb_connection.close()
    print("MariaDB / MySQL connection is closed")

if use_sqlite:
  sqlite_connection.commit()
  sqlite_connection.close()
  print("SQLite connection is closed")

print("Total Requests: " + str(response_count))
print("Duration: " + str(duration))

