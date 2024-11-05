import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import altair as alt

# Başlık ve açıklama
st.title("Satış Verisi, Talep Tahmini ve Görselleştirme Uygulaması")
st.write("""
Bu uygulamada, elle girdiğiniz satış verilerine dayalı olarak basit bir doğrusal regresyon modeli kullanarak talep tahmini yapılır.
Ayrıca verilerin analizi için kullanılan formülleri ve açıklamaları görebilirsiniz.
""")

# Satış verilerini elle girebilmek için input alanları
st.subheader("Satış Verilerini Girin")

# Tarih ve satış miktarını alacak alanlar
tarih_girdisi = st.date_input("Tarih Girin", value=pd.to_datetime("2023-01-01"))
satis_miktari_girdisi = st.number_input("Satış Miktarı Girin", min_value=0, value=100)

# Boş bir veri çerçevesi oluşturma veya mevcut veriyi yükleme
if "veri" not in st.session_state:
    st.session_state["veri"] = pd.DataFrame(columns=["Tarih", "satis_miktari"])

# Kullanıcının girdiği veriyi tabloya ekleme
if st.button("Veriyi Ekle"):
    yeni_veri = pd.DataFrame({
        "Tarih": [tarih_girdisi],
        "satis_miktari": [satis_miktari_girdisi],
    })
    st.session_state["veri"] = pd.concat([st.session_state["veri"], yeni_veri], ignore_index=True)

# Güncel tabloyu gösterme
st.subheader("Girilen Satış Verisi")
st.write(st.session_state["veri"])

# Tahmin ve Görselleştirme
if len(st.session_state["veri"]) > 1:
    # Tarihi sayısal bir değere çevirme
    st.session_state["veri"]["Tarih_sayisal"] = st.session_state["veri"]["Tarih"].map(pd.Timestamp.toordinal)
    
    # Modeli oluşturma ve eğitme
    X = st.session_state["veri"][["Tarih_sayisal"]]
    y = st.session_state["veri"]["satis_miktari"]
    model = LinearRegression()
    model.fit(X, y)
    
    # Gelecek 7 gün için tahmin yapma
    tarih_tahmin = pd.date_range(st.session_state["veri"]["Tarih"].max(), periods=7, freq="D")
    tarih_tahmin_sayisal = tarih_tahmin.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    tahmin_edilen_talep = model.predict(tarih_tahmin_sayisal)
    
    # Tahmin verisini bir DataFrame'e dönüştürme
    tahmin_verisi = pd.DataFrame({
        "Tarih": tarih_tahmin,
        "Tahmin": tahmin_edilen_talep
    })

    # Veriyi birleştirerek görselleştirme için hazırlama
    veri_grafik = st.session_state["veri"][["Tarih", "satis_miktari"]]
    veri_grafik["Tahmin"] = np.nan
    tahmin_verisi["satis_miktari"] = np.nan  # Gerçek satış verisi olmadığı için NaN bırakıyoruz
    veri_grafik = pd.concat([veri_grafik, tahmin_verisi], ignore_index=True)
    
    # Altair ile görselleştirme
    st.subheader("Satış ve Tahmin Grafiği")
    base = alt.Chart(veri_grafik).encode(x="Tarih:T")

    c1 = base.mark_line(color="blue").encode(
        y="satis_miktari:Q",
        tooltip=['Tarih', 'satis_miktari']
    ).properties(title="Gerçek Satış Verisi")
    
    c2 = base.mark_line(strokeDash=[5,5], color="red").encode(
        y="Tahmin:Q",
        tooltip=['Tarih', 'Tahmin']
    ).properties(title="Tahmin Edilen Talep")

    st.altair_chart(c1 + c2, use_container_width=True)

# Açıklamalar ve analiz
st.subheader("Analiz ve Kullanılan Formüller")
st.write("""
Tahmin için basit doğrusal regresyon modeli kullanılmıştır. Modelin genel formülü:

- **Y = m * X + b**

Burada:
- **Y**: Tahmin edilen değer (talep miktarı)
- **X**: Tarihin sayısal karşılığı
- **m**: Doğrusal regresyonun eğimi (yani, tarih ile talep arasındaki ilişkiyi ifade eder)
- **b**: Y eksenini kestiği nokta, modelin sabit katsayısıdır.

Bu formül, girilen geçmiş veriye dayalı olarak gelecekteki satış miktarlarını tahmin etmek için kullanılır.
Girilen her yeni veri ile model daha isabetli tahminler sunacaktır.
""")
