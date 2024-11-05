import streamlit as st
import pandas as pd

# Başlık ve açıklama
st.title("Satış Verisi ve Temel Talep Analizi")
st.write("""
Bu uygulama, manuel girdiğiniz satış verileri üzerinde temel analiz yapmanıza yardımcı olur.
Girilen verileri tabloda görebilir ve grafik olarak görüntüleyebilirsiniz.
""")

# Satış verilerini elle girebilmek için input alanları
st.subheader("Satış Verilerini Girin")

# Tarih ve satış miktarını alacak alanlar
tarih_girdisi = st.date_input("Tarih Girin", value=pd.to_datetime("2023-01-01"))
satis_miktari_girdisi = st.number_input("Satış Miktarı Girin", min_value=0, value=100)

# Boş bir veri çerçevesi oluşturma veya mevcut veriyi yükleme
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

# Grafik Görselleştirme
st.subheader("Satış Verisi Grafiği")
if len(st.session_state["veri"]) > 1:
    # Tarih sırasına göre veriyi sıralama
    st.session_state["veri"] = st.session_state["veri"].sort_values(by="Tarih")
    st.line_chart(st.session_state["veri"].set_index("Tarih")["Satış Miktarı"])

# Açıklamalar ve analiz
st.subheader("Analiz ve Kullanılan Formüller")
st.write("""
Bu grafik, zaman içindeki satış miktarlarını gösterir.
Analiz, tarih ve satış miktarı arasındaki ilişkiyi anlamanıza yardımcı olur.

Formüller ve Açıklamalar:
- **Ortalama Satış Miktarı**: Verilen satış verisinin ortalamasını gösterir.
- **Standart Sapma**: Satış verisinin ne kadar yaygın veya birbirine yakın olduğunu gösterir.

Verileriniz arttıkça grafik daha anlamlı bir hale gelir ve daha sağlıklı bir analiz yapmanıza olanak sağlar.
""")
