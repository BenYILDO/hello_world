import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Başlık ve Açıklama
st.title("Talep Tahmini ve Stok Planlama Uygulaması")
st.write("Bu uygulama, geçmiş satış verilerine dayalı olarak talep tahmini ve stok önerisi sunar.")

# Veri Yükleme
veri = pd.read_csv("satis_verisi.csv")
veri["ay"] = pd.to_datetime(veri["ay"])
veri = veri.set_index("ay")

# Satış Verilerini Görselleştirme
st.subheader("Geçmiş Satış Verileri")
st.line_chart(veri["satis_miktari"])

# Talep Tahmini (Basit Ortalama ile)
ortalama_talep = veri["satis_miktari"].mean()
st.write(f"Önümüzdeki ay için tahmini talep: {ortalama_talep:.2f} adet")

# Stok Önerisi (Tahmini Talebin %20 Fazlası)
stok_onerisi = ortalama_talep * 1.2
st.write(f"Önerilen minimum stok seviyesi: {stok_onerisi:.2f} adet")

# Gelecek Ay Tahmini Görselleştirme
veri["Tahmin"] = np.nan
veri.at[veri.index[-1] + pd.DateOffset(months=1), "Tahmin"] = ortalama_talep
st.subheader("Tahmini Talep Görselleştirmesi")
plt.figure(figsize=(10, 5))
plt.plot(veri.index, veri["satis_miktari"], label="Gerçek Satış Verisi", color="blue")
plt.plot(veri.index, veri["Tahmin"], label="Tahmin Edilen Talep", color="red", linestyle="--")
plt.legend()
st.pyplot(plt)
