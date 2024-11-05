import streamlit as st
import pandas as pd
import altair as alt

# Başlık ve genel açıklama
st.title("Satış Verisi Analizi ve Tahmin Uygulaması")
st.write("""
Bu uygulama, manuel olarak girdiğiniz satış verileri üzerinde analiz yapar ve gelecek için basit bir tahmin modeli sunar.
Satış verilerini girerek, grafik ve tahmin sonuçlarını gözlemleyebilirsiniz.
""")

# Satış verilerini girmek için input alanları
st.subheader("Satış Verilerini Girin")
tarih_girdisi = st.date_input("Tarih Girin", value=pd.to_datetime("2023-01-01"))
satis_miktari_girdisi = st.number_input("Satış Miktarı Girin", min_value=0, value=100)

# Boş bir veri çerçevesi veya mevcut veriyi yükleme
if "veri" not in st.session_state:
    st.session_state["veri"] = pd.DataFrame(columns=["Tarih", "Satış Miktarı"])

# Kullanıcının girdiği veriyi tabloya ekleme
if st.button("Veriyi Ekle"):
    yeni_veri = pd.DataFrame({
        "Tarih": [tarih_girdisi],
        "Satış Miktarı": [satis_miktari_girdisi],
    })
    st.session_state["veri"] = pd.concat([st.session_state["veri"], yeni_veri], ignore_index=True)

# Güncel tabloyu gösterme
st.subheader("Girilen Satış Verisi")
st.write(st.session_state["veri"])

# Grafik Görselleştirme (Altair kullanarak)
st.subheader("Satış Verisi Grafiği")
if len(st.session_state["veri"]) > 1:
    st.session_state["veri"] = st.session_state["veri"].sort_values(by="Tarih")
    c = alt.Chart(st.session_state["veri"]).mark_line().encode(
        x='Tarih:T',
        y='Satış Miktarı:Q'
    ).properties(title="Satış Verisi Zaman Serisi")
    st.altair_chart(c, use_container_width=True)

# Tahmin fonksiyonu - Basit Ortalama Tahmini
st.subheader("Satış Tahmini")
if len(st.session_state["veri"]) >= 2:
    # Ortalama hesaplayarak bir tahmin oluşturma
    ortalama_satis = st.session_state["veri"]["Satış Miktarı"].mean()
    st.write(f"Son verilere göre gelecek satış tahmini: {ortalama_satis:.2f} birim.")

# Rapor ve Analiz Bölümü
st.subheader("Rapor ve Analiz")
st.write("""
Bu rapor, girilen verilere dayalı olarak yapılan analizleri ve tahminleri içerir.

**Grafik Açıklaması**: 
- Grafik, tarihsel satış verilerinizin bir zaman serisini gösterir. Bu seriyi inceleyerek verilerdeki trend ve dalgalanmaları gözlemleyebilirsiniz.

**Tahmin Yöntemi**:
- Bu tahmin, girilen verilerin ortalamasını baz alır. Gelişmiş tahmin yöntemleri uygulanmasa da bu ortalama, kısa vadeli bir referans olarak değerlendirilebilir.

**Formüller**:
- **Ortalama Satış Miktarı**: Verilerin toplam satış miktarını veri sayısına bölerek hesaplanır.
- **Tahmin**: Gelecekteki değerleri ortalama değeri sabit alarak öngörür.

Daha fazla veri girdikçe tahmin sonuçları daha anlamlı hale gelecektir.
""")
