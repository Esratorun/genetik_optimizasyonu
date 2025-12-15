

import numpy as np
import random
import matplotlib.pyplot as plt
from genetik_operators import (
    amac_fonksiyonu,
    kisit_kontrol,
    uygunluk_hesapla,
    rulet_secimi,
    rank_temelli_secim,
    tek_noktali_caprazlama,
    mutasyon_uygula,
    populasyon_olustur,
    gen_sayisi
)




def kisit_duzelt(birey: np.ndarray) -> np.ndarray:
    """x1 + x2 = 100 kısıtını sağlamak için bireyi normalleştirir."""
    toplam = np.sum(birey)

    # abs(toplam - 100) > 1e-4 kontrolü, kısıtın ihlal edilip edilmediğini kontrol eder
    if toplam > 0 and abs(toplam - 100) > 1e-4:
        oran = 100 / toplam
        birey *= oran

    # Değerlerin 0-100 aralığında kalmasını sağla
    return np.clip(birey, 0, 100)






def genetik_optimizasyon_motoru(
    populasyon_boyutu: int,
    nesil_sayisi: int,
    caprazlama_turu: str,
    secim_turu: str,
    mutasyon_ihtimali: float,
    mutasyon_buyuklugu: float
):

    # ADIM 1 :BAŞLANGIÇ POPÜLASYONU OLUŞTURMA

    populasyon = populasyon_olustur(populasyon_boyutu,gen_sayisi)
    en_iyi_uygunluk_gecmisi = []
    en_iyi_birey = None
    en_yuksek_uygunluk = -np.inf

    print(f"GENETİK ALGORİTMA BAŞLATILDI ({secim_turu.upper()} Seçim)")

    for nesil in range(nesil_sayisi):

        # ADIM 2 UYGUNLUK (FİTNESS) HESAPLAMA
        uygunluklar = np.array([uygunluk_hesapla(birey) for birey in populasyon])

        # ADIM 3 EİLTİZM İLE EN İYİ BİREYİ BULMA
        en_iyi_indeks = np.argmax(uygunluklar)
        mevcut_elit_birey = populasyon[en_iyi_indeks].copy()
        mevcut_elit_uygunluk = uygunluklar[en_iyi_indeks]

        # En iyi bireyi güncelleme
        if mevcut_elit_uygunluk > en_yuksek_uygunluk:
            en_yuksek_uygunluk = mevcut_elit_uygunluk
            en_iyi_birey = mevcut_elit_birey.copy()

        # Geçmişe kaydetme 
        en_iyi_uygunluk_gecmisi.append(en_yuksek_uygunluk)

        # EKRANDA GÖSTERELİM 
        print(f"\n 1. Nesil: {nesil+1}/{nesil_sayisi}")
        print(f"2. En İyi Birey (x1, x2): [{en_iyi_birey[0]:.3f}, {en_iyi_birey[1]:.3f}]")
        print(f"3. Renk Kalitesi (y): {amac_fonksiyonu(en_iyi_birey):.4f}")
        print(f"4. Uygunluk (Fitness): {en_yuksek_uygunluk:.4f}")
        print(f"5. Kısıt İhlali: {kisit_kontrol(en_iyi_birey)}")

        # ADIM 4 EŞLEŞME HAVUZU OLUŞTURMA
        havuz=[]

        for _ in range(populasyon_boyutu // 2):
            if secim_turu == "rulet":
                ebeveynler = rulet_secimi(populasyon, uygunluklar)
            elif secim_turu == "rank":
                ebeveynler = rank_temelli_secim(populasyon, uygunluklar)
            else:
                raise ValueError("Seçim türü 'rulet' veya 'rank' olmalı.")
            havuz.append(ebeveynler)

        # ADIM 5 ÇAPRAZLAMA VE MUTASYON
        yeni_populasyon=[en_iyi_birey]

        while len(yeni_populasyon)<populasyon_boyutu:
            p1,p2=random.choice(havuz)

            if caprazlama_turu=="tek" or caprazlama_turu == "iki":
                c1,c2=tek_noktali_caprazlama(p1,p2)
            else:
                raise ValueError("Çaprazlama türü 'tek' veya 'iki' olmalı.")

            c1=mutasyon_uygula(c1,mutasyon_ihtimali,mutasyon_buyuklugu)
            c2=mutasyon_uygula(c2,mutasyon_ihtimali,mutasyon_buyuklugu)

            # X1+X2=100 KISITINI DÜZELTME
            c1 = kisit_duzelt(c1)
            c2 = kisit_duzelt(c2)

            yeni_populasyon.extend([c1,c2])

        populasyon=np.array(yeni_populasyon[:populasyon_boyutu])

    print("\n---  OPTİMİZASYON TAMAMLANDI ---\n")

    # Grafik çizimi
    fig = plt.figure(figsize=(10, 6))
    plt.plot(en_iyi_uygunluk_gecmisi, marker='.', linestyle='-', color='indigo')

    plt.title(f"Genetik Algoritma Evrimi: En İyi Uygunluk ({secim_turu.upper()} Seçim)")
    plt.xlabel("Nesil Sayısı")
    plt.ylabel("En İyi Uygunluk Değeri")
    plt.grid(True)
    plt.tight_layout()

    # PNG olarak kaydet
    plt.savefig("evrim_grafiği.png", dpi=300, bbox_inches="tight")

    # Notebook çıktısında GÖSTER
    plt.show()

    # Belleği temizle
    plt.close(fig)

    return en_iyi_birey, en_yuksek_uygunluk, en_iyi_uygunluk_gecmisi


