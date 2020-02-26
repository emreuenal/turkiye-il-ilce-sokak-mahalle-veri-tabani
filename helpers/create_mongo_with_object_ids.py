import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

# db without ObjectIDs
mongodb = client.tr_adres

# drop db to avoid double entrys with same data but different ObjectIDs
client.drop_database("tr_adres_oid")

# create new db to store data with ObjectIDs
mongodb_oid = client.tr_adres_oid


for il in mongodb.iller.find():
    il_id = il["_id"]
    il_adi = il["il_adi"]
    row_to_insert = { 
        "il_id" : il_id, 
        "il_adi": il_adi 
    }
    mongodb_oid.iller.insert_one(row_to_insert)
print("İller Eklendi")
    

for ilce in mongodb.ilceler.find():
    ilce_id = ilce["_id"]
    ilce_adi = ilce["ilce_adi"]
    il_id = ilce["il_id"]
    il_adi = ilce["il_adi"]
    row_to_insert = {
        "ilce_id": ilce_id,
        "ilce_adi": ilce_adi,
        "il_id" : il_id,
        "il_adi": il_adi
    }
    mongodb_oid.ilceler.insert_one(row_to_insert)
print("İlçeler Eklendi")
    

    
for mahalle in mongodb.mahalleler.find():
    mahalle_id = mahalle["_id"]
    mahalle_adi = mahalle["mahalle_adi"]
    ilce_id = mahalle["ilce_id"]
    ilce_adi = mahalle["ilce_adi"]
    il_id = mahalle["il_id"]
    il_adi = mahalle["il_adi"]
    row_to_insert = {
        "mahalle_id": mahalle_id,
        "mahalle_adi": mahalle_adi,
        "ilce_id": ilce_id,
        "ilce_adi": ilce_adi,
        "il_id" : il_id,
        "il_adi": il_adi
    }
    mongodb_oid.mahalleler.insert_one(row_to_insert)
print("Mahalleler Eklendi")



for sokak in mongodb.sokaklar.find():
    sokak_id = sokak["_id"]
    sokak_adi = sokak["sokak_adi"]
    mahalle_id = sokak["mahalle_id"]
    mahalle_adi = sokak["mahalle_adi"]
    ilce_id = sokak["ilce_id"]
    ilce_adi = sokak["ilce_adi"]
    il_id = sokak["il_id"]
    il_adi = sokak["il_adi"]
    row_to_insert = {
        "sokak_id": sokak_id,
        "sokak_adi": sokak_adi,
        "mahalle_id": mahalle_id, 
        "mahalle_adi": mahalle_adi, 
        "ilce_id": ilce_id, 
        "ilce_adi": ilce_adi, 
        "il_id" : il_id, 
        "il_adi": il_adi 
    }
    mongodb_oid.sokaklar.insert_one(row_to_insert)

print("Sokaklar Eklendi")
print("Tamamlandı!!!")

    