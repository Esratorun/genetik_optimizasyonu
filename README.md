
# GENETİK ALGORİTMA KULLANARAK ENDÜSTRİYEL BOYA KARIŞIM OPTİMİZASYONU (SENARYO 2)

Bir fabrika , iki tür pigment karışımı ile ideal renk yoğunluğunu yakalamak istiyor.
Bu projede ideal renk yoğunluğuna ulaşabilmek için Genetik Algoritma kullanacağız.

---

-> Amaç Fonksiyonu

Amaç  fonksiyonu elde etmek istediğimiz renk kalitesi puanını temsil eder .Genetik Algoritma bu değeri maksimize etmeye çalışır.

Bu Projede Kullanacağımız Amaç Fonksiyonu :

    y = 5*x1 + 2*x2 -x1*x2

  * x1 : A pigmentinin oranı (%)
  * x2 : B pigmentinin oranı (%)
  * y  : Renk Kalitesi Puanı

---

-> Değişkenler ve Kısıtlar

    1. Değişken Aralıkları

     * A Pigmenti : [0,100]
     * B Pigmenti : [0,100]

    2. Kısıtlar

     * x1 + x2 = 100   -> Toplam karışım %100 olmalı
     * x1 >=30         -> A karışımının oranı en az %30 olmalı
     * Uygunluk Cezası ->Kısıtların ihlali durumunda uygunluk fonksiyonuna yüksek bir ceza puanı uygulanarak o bireyin seçilme ihtimalini düşürmeliyiz.

---

# Genetik Algoritma Yapısı ve Operatörler


Algoritma,optimal çözümü bulana veya kullanıcı tarafından girilecek nesil sayısına ulaşana kadar devam edecek ve evrimsel süreci uygulayacak.


# Temel Genetik Algoritma Adımları


1.Başlangıç Popülasyonu : Rastgele x1 ve x2 değerleriyle başlangıç popülasyonu oluşturulur.
2.Uygunluk Hesaplama : Amaç fonksiyonu sonucu ve kısıt cezaları ile her birey için fitness skoru hesaplanır.
3.Elitizm : Popülasyondan en iyi bireyler rulet (rulet_secimi) veya rank (rank_temelli_secim) yöntemlerinden bir tanesi ile seçilir.
4.Çaaprazlama : Seçilen ebeveynlerden yeni bireyler tek veya iki noktalı çaprazlama ile üretilir.
5.Mutasyon : Popülasyona yeni genetik özellikler eklemek için düşük ihtimaller ile muasyon uygulanır.


#Dosya Yapısı

1. genetik_operators.py : Seçim (rulet, rank), çaprazlama, mutasyon, uygunluk hesaplama ve kısıt kontrolü gibi tüm genetik algoritma operatörlerini içeren yardımcı Python modülüdür.
2. evrim_motoru.py : Genetik algoritmanın ana çalışma motorudur. Popülasyon oluşturma, elitizm, nesil döngüsü, kısıt düzeltme işlemleri ve uygunluk evriminin grafikleştirilmesi bu dosyada gerçekleştirilir.
3. main.py : Kullanıcıdan genetik algoritma parametrelerini alan ve optimizasyon sürecini başlatan ana çalıştırma dosyasıdır. Optimizasyon sonunda elde edilen en iyi birey ve sonuçlar ekrana yazdırılır.
4. Endustriyel_Boya_Optimizasyonu.ipynb : Projenin Google Colab ortamında çalıştırıldığı Jupyter Notebook dosyasıdır. Kodların çalıştırılması, kullanıcı etkileşimi ve sonuçların görsel olarak sunulması bu dosya üzerinden yapılır.
5. README.md : Projenin amacı, kullanılan yöntemler, dosya yapısı ve çalıştırma adımlarını açıklayan bilgilendirme dosyasıdır.


---

# Beklenen Çıktılar

* En İyi Çözüm : Maksimum y değerini sağlayan optimal x1 ve x2 oranları
* Maksimum Renk Kalitesi : Algoritma tarafından bulunan en yüksek y değeri
* Görselleştirme : Nesiller boyunca en iyi uygunluk değerini gösteren grafikler


