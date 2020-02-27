# Database Connection Configurations File
use_mariadb = False
use_postgresql = False
use_mongodb = False
use_sqlite = False
use_redis = False

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
if use_sqlite:
    import sqlite3
    sqlite_connection = sqlite3.connect('tr_adres.db')
if use_redis:
    import redis
    red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    