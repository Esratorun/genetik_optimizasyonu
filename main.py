
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

if not os.path.exists('evrim_motoru.py') or not os.path.exists('genetik_operators.py'):
    print("HATA: Gerekli modüller (evrim_motoru.py, genetik_operators.py) bulunamadı.")
    sys.exit(1)

from evrim_motoru import genetik_optimizasyon_motoru as evrimsel_algoritma
from genetik_operators import amac_fonksiyonu, kisit_kontrol

#Kullanıcıdan parametreler alıyoruz.

try:
    print("--- GENETİK ALGORİTMA PARAMETRELERİ ")
    populasyon_boyutu = int(input("Popülasyon boyutu kaç olsun? (Örn: 50): "))
    nesil_sayisi = int(input("Kaç nesil çalıştırılsın? (Örn: 100): "))
    caprazlama_turu = input("Çaprazlama türü ne olsun? ('tek' / 'iki'): ").strip().lower()
    secim_turu = input("Seçim türü ne olsun? ('rulet' / 'rank'): ").strip().lower()
    mutasyon_ihtimali = float(input("Mutasyon ihtimali (örn: 0.15): "))
    mutasyon_buyuklugu = float(input("Mutasyon büyüklüğü (örn: 5): "))
except ValueError:
    print("\nHATA: Lütfen sayısal alanlara geçerli bir sayı giriniz.")
    sys.exit(1)

print("\n EVRİMSEL SÜREÇ BAŞLATILIYOR ")

en_iyi_birey, en_yuksek_uygunluk, _ = evrimsel_algoritma(
    populasyon_boyutu=populasyon_boyutu,
    nesil_sayisi=nesil_sayisi,
    caprazlama_turu=caprazlama_turu,
    secim_turu=secim_turu,
    mutasyon_ihtimali=mutasyon_ihtimali,
    mutasyon_buyuklugu=mutasyon_buyuklugu
)

x1_opt = en_iyi_birey[0]
x2_opt = en_iyi_birey[1]
y_max = amac_fonksiyonu(en_iyi_birey)
kisit_ihlali_sayisi = kisit_kontrol(en_iyi_birey)

print("\n---  OPTİMİZASYON SONUÇLARI  ---")
print(f"Optimal A Pigmenti Oranı (x1): {x1_opt:.4f} %")
print(f"Optimal B Pigmenti Oranı (x2): {x2_opt:.4f} %")
print(f"Maksimum Renk Kalitesi Puanı (y): {y_max:.4f}")
print(f"Toplam Oran Kontrolü (x1+x2): {x1_opt + x2_opt:.4f}")
print(f"Kısıt Durumu: {' Sağlanıyor' if kisit_ihlali_sayisi == 0 else f' {kisit_ihlali_sayisi} İhlal Var'}")
