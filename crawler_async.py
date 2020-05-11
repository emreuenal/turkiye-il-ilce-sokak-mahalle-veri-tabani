# Crawler scriptinin multiprocessing kullanan ve bu sayede daha kısa sürede crawling yapan hali.
# kendi sistemimde crawler.py yaklaşık 12-13 saat arası, crawler_async.py 1-2 saat arası sürüyor.
# Veri tabanı modüllerinin birçoğunun async data girişini desteklememesinden dolayı ilk etapta
# veriler .txt olarak diske kaydedilir. 
# Sonrasında add_to_db çalıştırılarak istenilen veri tabanına bu dataların girişi sağlanır.
# executemany methodu kullanıldığı için yaklaşık 1,1M. sokak girişi bile 1dk kadar sürmektedir.

import json
import datetime

from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool





start_time = datetime.datetime.now()


main_url = "https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu"
r = requests.get(main_url)
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


def get_iller():
    """
    İlleri Alır ve {'il_id': 34, 'il_adi': 'İSTANBUL'} gibi dictler oluşturarak bu dictlerden bir liste hazırlar.
    """
    il_response = requests.post('https://adres.nvi.gov.tr/Harita/ilListesi', headers=headers, cookies=cookies, data=data)
    json_obj_iller = json.loads(il_response.text)
    iller_id_list = []
    for il in json_obj_iller:
        il_dict = {}
        il_id = il["kimlikNo"]
        il_dict['il_id'] = il_id
        il_adi = il["bilesenAdi"]
        il_dict['il_adi'] = il_adi
        
        print("İl ID: {}, İl Adı: {}".format(il_id, il_adi))
        iller_id_list.append(il_dict)
    return iller_id_list
                                                                                                                                                                                                                                                                                                                                                                                 

def get_ilceler(iller_id_list):
    """
    İlçeleri Alır.\n
    İlçeleri almak için, ilçeleri alınmak istenen ilin kimlikNo'su gerekmektedir.\n
    İller listesi verilir ve kimlikNo'lar buradan alınarak her bir ilin ilçeleri alınır.
    """
    ilceler_list = []
    for il in iller_id_list:
        data = {'ilKimlikNo': il['il_id']}
        response_ilce = requests.post('https://adres.nvi.gov.tr/Harita/ilceListesi', headers=headers, cookies=cookies, data=data)
        json_obj_ilceler = json.loads(response_ilce.text)
        for ilce in json_obj_ilceler:
            ilce_dict = {}
            il_id = il['il_id']
            ilce_dict['il_id'] = il_id
            il_adi = il['il_adi']
            ilce_dict['il_adi'] = il_adi
            ilce_id = ilce["kimlikNo"]
            ilce_dict['ilce_id'] = ilce_id
            ilce_adi = ilce["bilesenAdi"]
            ilce_dict['ilce_adi'] = ilce_adi
            ilceler_list.append(ilce_dict)
            print("İl ID: {}, İl Adı: {}, İlce ID: {}, İlçe Adı: {}".format(il_id, il_adi, ilce_id, ilce_adi))
            
    return ilceler_list
    


def get_mahalleler(ilceler_list):
    """
    Mahalleleri Alır.\n
    Mahalleleri almak için, mahalleleri alınmak istenen ilçenin kimlikNo'su gerekmektedir.\n
    İlçeler listesi verilir ve kimlikNo'lar buradan alınarak her bir ilçenin mahalleleri alınır.
    """
    mahalleler_list = []
    for ilce in ilceler_list:
        data = {'ilceKimlikNo': ilce["ilce_id"]}
        response_mahallekoy = requests.post('https://adres.nvi.gov.tr/Harita/mahalleKoyBaglisiListesi', headers=headers, cookies=cookies, data=data)
        json_obj_mahallekoy = json.loads(response_mahallekoy.text)
        for mahalle in json_obj_mahallekoy:
            mahalle_dict = {}
            il_id = ilce['il_id']
            mahalle_dict['il_id'] = il_id
            il_adi = ilce['il_adi']
            mahalle_dict['il_adi'] = il_adi
            ilce_id = ilce["ilce_id"]
            mahalle_dict['ilce_id'] = ilce_id
            ilce_adi = ilce["ilce_adi"]
            mahalle_dict['ilce_adi'] = ilce_adi
            mahalle_id = mahalle["kimlikNo"]
            mahalle_dict['mahalle_id'] = mahalle_id
            mahalle_adi = mahalle["bilesenAdi"]
            mahalle_dict['mahalle_adi'] = mahalle_adi
            mahalleler_list.append(mahalle_dict)
            print("İl ID: {}, İl Adı: {}, İlce ID: {}, İlçe Adı: {}, Mahalle ID: {}, Mahalle Adı: {}".format(il_id, il_adi, ilce_id, ilce_adi, mahalle_id, mahalle_adi))
    return mahalleler_list

def get_sokaklar(mahalleler_list):
    """
    Sokakları Alır.\n
    Sokakları almak için, sokakları alınmak istenen mahallenin kimlikNo'su gerekmektedir.\n
    Mahalleler listesi verilir ve kimlikNo'lar buradan alınarak her bir mahallenin sokakları alınır.
    """
    sokaklar_list = []
    for mahalle in mahalleler_list:
        data = {'mahalleKoyBaglisiKimlikNo': mahalle["mahalle_id"]}
        response_yolListesi = requests.post('https://adres.nvi.gov.tr/Harita/yolListesi', headers=headers, cookies=cookies, data=data)
        json_obj_yolListesi = json.loads(response_yolListesi.text)
        for sokak in json_obj_yolListesi:
            sokak_dict = {}
            il_id = mahalle['il_id']           
            il_adi = mahalle['il_adi']            
            ilce_id = mahalle["ilce_id"]            
            ilce_adi = mahalle["ilce_adi"]            
            mahalle_id = mahalle["mahalle_id"]            
            mahalle_adi = mahalle["mahalle_adi"]            
            sokak_id = sokak["kimlikNo"]            
            sokak_adi = sokak["bilesenAdi"]
            sokak_dict['il_id'] = il_id
            sokak_dict['il_adi'] = il_adi
            sokak_dict['ilce_id'] = ilce_id
            sokak_dict['ilce_adi'] = ilce_adi
            sokak_dict['mahalle_id'] = mahalle_id
            sokak_dict['mahalle_adi'] = mahalle_adi
            sokak_dict['sokak_id'] = sokak_id
            sokak_dict['sokak_adi'] = sokak_adi            
            sokaklar_list.append(sokak_dict)   
            print("İl ID: {}, İl Adı: {}, İlce ID: {}, İlçe Adı: {}, Mahalle ID: {}, Mahalle Adı: {}, Sokak ID: {}, Sokak Adı: {}".format(il_id, il_adi, ilce_id, ilce_adi, mahalle_id, mahalle_adi, sokak_id, sokak_adi))
            """with open("sokaklar_in_function.txt", 'a+', encoding="utf8") as outfile:
                outfile.write(str(sokak_dict) + "\n")"""

    return sokaklar_list


def multipro_crawl(a_list, func_name):
    """
    Bir liste alır (a_list) ve bu listeyi 4 ayrı listeye bölerek hepsinin üzerinde aynı anda func_name fonksiyonunu uygular.\n
    Bu sayede her bir request'den gelecek response'u bekleyip daha sonra diger request'i yapmak yerine işi 4 process olarak yapıyoruz.
    """
    chunks = [a_list[i::6] for i in range(6)]
    pool = Pool(processes=6)
    result = pool.map(func_name, chunks)
    return result



def merge_list_of_lists(unmerged_list):
    """
    multiprocessing kullandığımızdan dolayı fonksiyon sonunda gelen liste gerekli bilgiler yerine bu bilgileri içeren 4 ayrı listeden oluşuyor.\n
    Yani, [{data}, {data}, {data}, {data}, ......] yerine [ [{data}, {data}, ...], [{data}, {data}, ...], [{data}, {data}, ...], [{data}, {data}, ...] ]\n
    Bu dağınık listedeki her bir itemi alarak yeni düzenli bir liste oluşturur.
    """
    merged_list = []
    for a_list in unmerged_list:
        for list_item in a_list:
            merged_list.append(list_item)
    return merged_list

def write_list_to_disk(file_name, list_name):
    """
    Listeyi diske yazmak için kullanılır.
    """
    with open(file_name, 'w', encoding="utf8") as outfile:
        json.dump(list_name, outfile, ensure_ascii=False)


# Get Iller
iller_id_list = get_iller()
write_list_to_disk("iller.txt", iller_id_list)


# Get Ilceler
ilceler_list = multipro_crawl(iller_id_list, get_ilceler)
ilceler_list_merged = merge_list_of_lists(ilceler_list)
write_list_to_disk("ilceler.txt", ilceler_list_merged)


# Get Mahalleler
mahalleler_list = multipro_crawl(ilceler_list_merged, get_mahalleler)
mahalleler_list_merged = merge_list_of_lists(mahalleler_list)
write_list_to_disk("mahalleler.txt", mahalleler_list_merged)


# Get Sokaklar
sokaklar_list = multipro_crawl(mahalleler_list_merged, get_sokaklar)
sokaklar_list_merged = merge_list_of_lists(sokaklar_list)
write_list_to_disk("sokaklar.txt", sokaklar_list_merged)  


stop_time = datetime.datetime.now()
duration = stop_time - start_time


print(duration) 