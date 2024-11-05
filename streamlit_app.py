import streamlit as st
import pandas as pd
import numpy as np

# Başlık ve açıklama
st.title("Satış Verisi ve Talep Tahmin Uygulaması")
st.write("""
Bu uygulamada, elle girdiğiniz satış verilerine dayalı olarak talep tahmini yapılır.
Ayrıca verilerin analizi için kullanılan formülleri ve açıklamaları görebilirsiniz.
""")

# Satış verilerini elle girebilmek için input alanları
st.subheader("Satış Verilerini Girin")

# Tarih ve satış miktarını alacak alanlar
tarih_girdisi = st.date_input("Tarih Girin", value=pd.to_datetime("2023-01-01"))
satis_miktari_girdisi = st.number_input("Satış Miktarı Girin", min_value=0, value=100)

# Boş bir veri çerçevesi oluşturma veya mevcut veriyi yükleme
if "veri" not in st.session_state:
    st.session_state["veri"] = pd.DataFrame(columns=["Tarih", "satis_miktari", "Tahmin"])

# Kullanıcının girdiği veriyi tabloya ekleme
if st.button("Veriyi Ekle"):
    yeni_veri = pd.DataFrame({
        "Tarih": [tarih_girdisi],
        "satis_miktari": [satis_miktari_girdisi],
        "Tahmin": [satis_miktari_girdisi + np.random.normal(0, 10)]
    })
    st.session_state["veri"] = pd.concat([st.session_state["veri"], yeni_veri], ignore_index=True)

# Güncel tabloyu gösterme
st.subheader("Girilen Satış ve Tahmin Verisi")
st.write(st.session_state["veri"])

# Açıklamalar ve analiz
st.subheader("Analiz ve Kullanılan Formüller")
st.write("""
Talep tahmini için kullanılan formül:

- **Talep Tahmini = Satış Miktarı + Rastgele Gürültü (μ=0, σ=10)**

Bu formül, mevcut satış verisine dayalı olarak rastgele bir gürültü eklenerek tahmin edilen talebi oluşturur.
Böylece talep tahmininde küçük bir varyasyon göz önünde bulundurulur.

Girilen her veri için yukarıdaki formül uygulanarak tahmin hesaplanmaktadır. 
Bu tahmin, satış verisinin girdiğiniz miktarına göre ±10 birimlik bir sapma ile belirlenmiştir.
""")
