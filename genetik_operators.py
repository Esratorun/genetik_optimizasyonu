
import numpy as np
import random

karsilik_cezasi =-5000 # Kısıt ihlallerinde verilecek ceza (Uygunluk değerinden düşecek)
gen_sayisi=2

# KULLANILACAK TEMEL FONKSİYONLAR (Amaç ve Uygunluk Fonksiyonları)

"""
AMAÇ FONKSİYONU (Renk Kalitesi Puanı ) :   y = 5*x1 + 2*x2 - x1*x2

        birey (np.ndarray): [x1, x2] değerlerini içeren kromozom parametre olarak alınır.

        float: Hesaplanan y (Renk Kalitesi) puanı döndürülür.

"""

def amac_fonksiyonu(birey: np.ndarray) -> float:

    x1, x2 = birey
    # Amaç fonksiyonu: y = 5 * x1 + 2 * x2 - x1 * x2 (Maksimize edilecek)
    y = 5 * x1 + 2 * x2 - x1 * x2
    return y




"""
    Bireyin kısıtları ihlal edip etmediğini kontrol eder.

    Kısıtlar:
    1. x1 + x2 = 100
    2. x1 >= 30
    3. x1 : [0,100] ve  x2 : [0,100]

        birey (np.ndarray): [x1, x2] değerlerini içeren birey kromozomu parametre alır.
        int: İhlal edilen kısıt sayısı (0, 1 veya 2) döndürür.

 """




def kisit_kontrol(birey: np.ndarray) -> int:
    x1, x2 = birey
    ihlal_sayisi=0

    # x1 + x2 = 100 olmalı ama float kullandığımız için küçük bir tolerans(epilon) kullanıyoruz.

    epsilon=1e-4

    if abs( x1+x2-100)>epsilon:
        ihlal_sayisi+=1

    # x1 >= 30 olmalı

    if x1<30:
        ihlal_sayisi+=1

    # x1 : [0,100] ve  x2 : [0,100]

    if not (0 <= x1 <= 100 and 0 <= x2 <= 100):
        ihlal_sayisi += 1


    return ihlal_sayisi




"""
    Bireyin uygunluk (fitness) skorunu hesaplar.
    Bu, amaç fonksiyonu sonucundan kısıt cezalarının düşülmüş halidir.

        birey (np.ndarray): [x1, x2] değerlerini içeren birey kromozomu parametre alır.
        float: uygunluk skoru döndürür.

"""




def uygunluk_hesapla(birey: np.ndarray) -> float:

    y_puan =amac_fonksiyonu(birey)
    ihlal_sayisi=kisit_kontrol(birey)

    #kisit_kontrol fonksiyonundan gelen ihlal sayısı ile başta tanımladığım karsilik_cezasi kullanarak ceza hesaplanır.

    ceza = ihlal_sayisi*karsilik_cezasi

    uygunluk = y_puan + ceza

    return uygunluk


# SEÇİM OPERATÖRLERİ (Rulet ve Rank)

    """
    RULET SEÇİM METODU  :

    Uygunluk değerlerine göre rulet tekeri yöntemiyle ebeveyn seçer.
    Uygunluğu yüksek olan bireylerin seçilme olasılığı daha fazladır.

    """

def rulet_secimi(populasyon: list, uygunluklar: np.ndarray, adet: int = 2) -> np.ndarray:
    # Olasılık hesaplaması için tüm uygunluklar pozitif olmalı.
    # Bunun için en küçük uygunluk değerine kaydırma uyguluyoruz.
    min_uygunluk = np.min(uygunluklar)

    # Tüm uygunluklar pozitif olacak şekilde offset eklenir.
    offset = np.abs(min_uygunluk) + 1e-6
    pozitif_uygunluklar = uygunluklar + offset

    toplam_uygunluk = np.sum(pozitif_uygunluklar)
    olasiliklar = pozitif_uygunluklar / toplam_uygunluk

    # Birey listesini numpy array'e çeviriyoruz.
    populasyon_np = np.array(populasyon, dtype=object)

    secilen_indeksler = np.random.choice(
        len(populasyon_np),
        size=adet,
        p=olasiliklar,
        replace=False
    )

    return populasyon_np[secilen_indeksler]


    """

    RANK SEÇİM METODU  :

    Bireyler uygunluk değerlerine göre sıralanır, sıralamadaki yerlerine göre seçim olasılığı atanır.

    """

def rank_temelli_secim(populasyon: list, uygunluklar: np.ndarray, adet: int = 2) -> np.ndarray :

     N = len(populasyon)

     sirali_indeksler = np.argsort(-uygunluklar) # Büyükten küçüğe sıralıyoruz

     # Popülasyonu numpy dizisine çeviriyoruz
     populasyon_np = np.array(populasyon, dtype=object)

     payda = N * (N + 1) / 2
     secim_ihtimalleri = np.array([(N - i) / payda for i in range(N)]) #en iyi bireye en yüksek lasılık değeri verilmeli

     secilen_indeksler = np.random.choice(
        N,
        size=adet,
        p=secim_ihtimalleri,
        replace=False
       )

      # Seçilen sıralı indeksler kullanılarak gerçek bireyler alınır.Yani sirali_indeksler hangi bireye karşılık geliyorsa o alınıyor.
     ebeveynler = [populasyon_np[sirali_indeksler[i]] for i in secilen_indeksler]

     return np.array(ebeveynler)



#ÇAPRAZLAMA OPERATÖRLERİ

"""
TEK VE İKİ NOKTALI ÇAPRAZLAMA :

    Rastgele bir noktadan ebeveynlerin kromozomlarını kesip çaprazlar.
    Gen sayısı 2 (x1, x2) olduğu için kesim noktası sabittir (x1 ile x2 arası).
    İki noktalı çaprazlamada ise kesme noktası rastgele belirlenir.Fakat bizim gen sayımız iki olduğu için buna gerek yok.
    Projede sadece tek noktalı çaprazlama kullanacağım.

"""

def tek_noktali_caprazlama(p1: np.ndarray, p2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:

    # Kesim noktası 1 yani x1'den sonra
    nokta = 1

    c1 = np.concatenate((p1[:nokta], p2[nokta:]))
    c2 = np.concatenate((p2[:nokta], p1[nokta:]))

    return c1, c2


# MUTASYON OPERATÖRÜ

"""
    Her gen için rastgele mutasyon uygulayarak çözüm çeşitliliğini artırır.
    Mutasyon sonrası değerler [0, 100] aralığına kısıtlanır.
"""

def mutasyon_uygula(birey: np.ndarray, ihtimal: float, buyukluk: float) -> np.ndarray:

  yeni = birey.copy()

      # Her gen için mutasyon olasılığı kontrol edilir
  for i in range(len(yeni)):
        if np.random.rand() < ihtimal:
            # Rastgele bir değişim miktarı hesaplama
            degisim = buyukluk * (np.random.rand() - 0.5) * 2  #Rastgele sapma 1 ve -1 arasında olsun
            yeni[i] += degisim

            # Gen değerleri belirlenen sınırlar içinde tutmak için clip
            yeni[i] = np.clip(yeni[i], 0, 100)


  return yeni



# POPÜLASYON OLUŞTURMA

"""
  Başlangıç popülasyonunu rastgele oluşturur.
  x1 ve x2 değerleri 0-100 aralığında olmalıdır.

  x1 + x2 = 100 kısıtını sağlamak için normalizasyon yapılır.
"""



def populasyon_olustur(boyut: int, gen_sayisi: int) -> list:
    populasyon = []

    for i in range(boyut):
        # Rastgele bireyler oluşturuluyor
        birey = np.random.uniform(0, 100, gen_sayisi)

        # Normalizasyon
        toplam = np.sum(birey)

        # x1, x2 ... değerlerinin toplamı 100 olacak şekilde ölçekleme
        if toplam > 0:
            oran = 100 / toplam
            birey *= oran

        # Değerler [0, 100] aralığında kalsın
        birey = np.clip(birey, 0, 100)

        populasyon.append(birey)

    return populasyon

