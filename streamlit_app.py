import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Başlık ve açıklama
st.title("Talep Tahmin Görselleştirme Uygulaması")
st.write("""
Bu uygulama, geçmiş satış verilerine dayalı tahmin edilen talepleri görselleştirir.
""")

# Veri yükleme veya veri oluşturma
def veri_yarat():
    tarih = pd.date_range(start="2023-01-01", periods=30, freq="D")
    satis_miktari = np.random.randint(50, 200, size=len(tarih))
    tahmin_edilen_talep = satis_miktari + np.random.normal(0, 10, size=len(tarih))
    
    veri = pd.DataFrame({
        "Tarih": tarih,
        "satis_miktari": satis_miktari,
        "Tahmin": tahmin_edilen_talep
    })
    return veri

# Veri yüklenmesi
veri = veri_yarat()

# Veri gösterimi
st.subheader("Satış ve Tahmin Verisi")
st.write(veri)

# Altair ile grafik oluşturma
st.subheader("Talep Tahmini Grafiği")
c = alt.Chart(veri.reset_index()).mark_line().encode(
    x='Tarih:T',
    y='satis_miktari:Q',
    color=alt.value("blue"),
    tooltip=['Tarih', 'satis_miktari']
).properties(title="Gerçek Satış Verisi")

t = alt.Chart(veri.reset_index()).mark_line(strokeDash=[5,5], color="red").encode(
    x='Tarih:T',
    y='Tahmin:Q',
    tooltip=['Tarih', 'Tahmin']
)

# Grafik gösterme
st.altair_chart(c + t, use_container_width=True)
