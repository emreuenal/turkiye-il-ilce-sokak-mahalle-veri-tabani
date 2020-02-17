# Database Connection Configuration File
use_mariadb = False
use_postgresql = False
use_mongodb = False

if use_mariadb:
    import MySQLdb as mariadb
    mdb_connection = mariadb.connect(user='username', passwd='password', db='tr_adres', charset='utf8')
if use_postgresql:
    import psycopg2
    pg_connection = psycopg2.connect(host="127.0.0.1", port="5432", database="tr_adres", user="username", password="password")
if use_mongodb:
    import pymongo
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    mongodb = client.tr_adres
