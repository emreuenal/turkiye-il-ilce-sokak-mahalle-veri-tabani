# Türkiye Adres Veri Tabanı
Bu Repo https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu adresinde yer alan tüm İl - İlçe - Mahalle / Köy / Mezra / Mevki - CSBM 
bilgilerini almak için oluşturulmuş **Python 3** scriptini içerir.

Üzerinde çalışmakta olduğum bir proje için bu bilgiler gerekti ve tam olarak işime yarayacak ayrıntıda bir veri tabanı bulamadığım
için bir python crawler yazarak bu bilgileri PostgreSQL, MariaDB ve MongoDB veri tabanlarına aktardım.

Eğer siz de bu bilgilere ihtiyaç duyuyorsanız bu crawler'ı kullanabilir **(!!! Lütfen Aşağıdaki Uyarıları Okuyunuz)** ya da dumps klasöründen
kullanmak istediğiniz veri tabanı sunucusu için uygun olan dump'ı indirebilirsiniz.

# Uyarılar
Mecbur kalmadıkça scripti kendiniz çalıştırmak yerine dumps klasöründeki dumplardan yararlanmanızı tavsiye ederim.   

Her bir kombinasyon için ayrı bir request yollandığından dolayı script sonunda yaklaşık olarak toplam 75461 adet istek **İçişleri Bakanlığı**'na bağlı olan
https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu adresine yollanmış olur.   

Sistem, Bağlantı ve Veri Tabanı Sunucunuzun hızına bağlı olarak bu işlem 12 - 15 saat (her üç veri tabanına veri girişi) arasında sürer.


```
Total Requests: 75461
Runtime : 12:22:48.273607
```



# Crawler'ın Kullanımı
- İlk olarak repoyu clonlayın: `git clone https://github.com/emreuenal/turkiye-il-ilce-sokak-mahalle-veri-tabani.git`
- Veri tabanı konfigrasyon dosyasını kopyalayın: `mv dbconfig/config-sample.py dbconfig/config.py`
- Kullanmak istediğiniz veri tabanı sunucusunu `False`dan `True`ya çevirerek veri tabanı bağlantısı için gerekli olan bilgileri girin.
- Kullanmak istediğiniz veri tabanı sunucusuna bağlı olarak gerekli modülleri pip ile yükleyin.(MySQL/MariaDB için **mysqlclient**, PostgreSQL için **psycopg2**, MongoDB için **pymongo**)
- `python -V` ya da `python -V` komutu ile python sürümünüzün en az Python 3.6 olduğundan emin olun.
- `python crawler.py` veya `python3 crawler.py` komutu ile crawlerı çalıştırın.

Crawling işlemi biraz(!) süreceği için, eğer uzak sunucunuza ssh ile bağlanarak bu işlemleri gerçekleştiriyorsanız bağlantınızın kopması ve doğal olarak işlemin durması ihtimaline karşın
screen ya da tmux gibi bir terminal multiplexer kullanmanızı tavsiye ederim.

# Veri Tabanı Yapısı    
## PostgreSQL ve MariaDB / MySQL
Dört Adet Tablodan oluşmaktadır: `iller`, `ilceler`, `mahalleler` ve `sokaklar`.
- `iller` tablosu il isimlerini ve il kimlik numaralarını içerir (`il_id`, `il_adi`).
- `ilceler` tablosu ilçe isimlerini, ilçe kimlik numaralarını ve iller tablosundaki bilgileri içerir (`ilce_id`, `ilce_adi`, `il_id`, `il_adi`).
- `mahalleler` tablosu Mahalle / Köy / Mezra / Mevki isimlerini, bunların kimlik numaralarını ve ilceler tablosundaki bilgileri içerir (`mahalle_id`, `mahalle_adi`, `ilce_id`, `ilce_adi`, `il_id`, `il_adi`).
- `sokaklar` tablosu Cadde / Sokak / Bulvar / Meydan isimlerini, bunların kimlik numaralarını ve mahalleler tablosundaki bilgileri içerir (`sokak_id`, `sokak_adi`, `mahalle_id`, `mahalle_adi`, `ilce_id`, `ilce_adi`, `il_id`, `il_adi`).

## MongoDB
Tablo isimleri PostgreSQL ve MariaDB / MySQL ile aynıdır. Tek fark her bir tablonun id sütunları (`il_id`, `ilce_id`, `mahalle_id`, `sokak_id`) mongodb yapısından dolayı (ObjectID kullanmamak için)
`_id` şeklinde oluşturulmuştur.

```
> db.iller.findOne()
{ "_id" : 1, "il_adi" : "ADANA" }
```
```
> db.ilceler.findOne()
{ "_id" : 1757, "il_adi" : "ADANA", "il_id" : 1, "ilce_adi" : "ALADAĞ" }
```
```
> db.mahalleler.findOne()
{
        "_id" : 176887,
        "il_adi" : "ADANA",
        "il_id" : 1,
        "ilce_adi" : "ALADAĞ",
        "ilce_id" : 1757,
        "mahalle_adi" : "AKÖREN MAHALLESİ"
}
```
```
> db.sokaklar.findOne()
{
        "_id" : 566149,
        "il_adi" : "ADANA",
        "il_id" : 1,
        "ilce_adi" : "ALADAĞ",
        "ilce_id" : 1757,
        "mahalle_adi" : "AKÖREN MAHALLESİ",
        "mahalle_id" : 176887,
        "sokak_adi" : "AKDERE (Sokak)"
}
```
**Not:**  ObjectID'li versiyona ihtiyaç duyarsanız helpers klasöründeki scriptden faydalanabilirsiniz.
```
> db.iller.findOne()
{
        "_id" : ObjectId("5e56345febe7d0061a6c0dd2"),
        "il_id" : 1,
        "il_adi" : "ADANA"
}
```
```
> db.ilceler.findOne()
{
        "_id" : ObjectId("5e563460ebe7d0061a6c0e23"),
        "ilce_id" : 1757,
        "ilce_adi" : "ALADAĞ",
        "il_id" : 1,
        "il_adi" : "ADANA"
}
```
```
> db.mahalleler.findOne()
{
        "_id" : ObjectId("5e563460ebe7d0061a6c11f0"),
        "mahalle_id" : 176887,
        "mahalle_adi" : "AKÖREN MAHALLESİ",
        "ilce_id" : 1757,
        "ilce_adi" : "ALADAĞ",
        "il_id" : 1,
        "il_adi" : "ADANA"
}
```
```
> db.sokaklar.findOne()
{
        "_id" : ObjectId("5e563473ebe7d0061a6d3495"),
        "sokak_id" : 566149,
        "sokak_adi" : "AKDERE (Sokak)",
        "mahalle_id" : 176887,
        "mahalle_adi" : "AKÖREN MAHALLESİ",
        "ilce_id" : 1757,
        "ilce_adi" : "ALADAĞ",
        "il_id" : 1,
        "il_adi" : "ADANA"
}
```
