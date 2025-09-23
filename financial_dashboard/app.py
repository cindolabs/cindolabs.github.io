import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Dashboard Keuangan Hocindo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- CSS THEME ----------------------
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #006847, #004c3f); color: #D4AF37; }
    .sidebar .sidebar-content { background: #1a3c34; color: #D4AF37; }
    h1, h2, h3, h4 { color: #D4AF37; }
    .stButton>button { background: linear-gradient(to right, #D4AF37, #b8860b); color: #004c3f; }
    .stMetric { background: #2e5d4f; border-radius: 10px; padding: 10px; color: #FFFFFF !important; }
    .stMetric label { color: #FFFFFF !important; }
    .stMetric .metric-value { color: #FFFFFF !important; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# ---------------------- AUTENTIKASI ----------------------
st.sidebar.header("Autentikasi")
password = st.sidebar.text_input("Masukkan kata sandi:", type="password")
if password != "hocindo123":  # Ganti dengan kata sandi pilihan Anda
    st.error("Kata sandi salah! Hubungi admin.")
    st.stop()

# ---------------------- INISIALISASI DATA ----------------------
if 'transaksi' not in st.session_state:
    if os.path.exists("transaksi.csv"):
        st.session_state.transaksi = pd.read_csv("transaksi.csv")
        st.session_state.transaksi["Tanggal"] = pd.to_datetime(st.session_state.transaksi["Tanggal"])
    else:
        data = [
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Mochamad Tabrani", "Jumlah": 50000, "Investor": "Mochamad Tabrani"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Pipit", "Jumlah": 50000, "Investor": "Pipit"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Sangaji", "Jumlah": 100000, "Investor": "Sangaji"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Asmin", "Jumlah": 135000, "Investor": "Asmin"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Rasyid", "Jumlah": 50000, "Investor": "Rasyid"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pengeluaran", "Deskripsi": "Biaya Operasional", "Jumlah": -10000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Dana Manajer", "Deskripsi": "Dana Dikelola Manajer", "Jumlah": -100000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Dana Cadangan", "Deskripsi": "Dana Cadangan", "Jumlah": -275000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pertumbuhan", "Deskripsi": "Pertumbuhan Dana Manajer", "Jumlah": 900, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Bagi Hasil", "Deskripsi": "Bagi Hasil Investor", "Jumlah": -100, "Investor": "N/A"},
        ]
        st.session_state.transaksi = pd.DataFrame(data)
        st.session_state.transaksi["Tanggal"] = pd.to_datetime(st.session_state.transaksi["Tanggal"])
        st.session_state.transaksi.to_csv("transaksi.csv", index=False)

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #D4AF37;'>💼 Dashboard Keuangan Hocindo</h1>
    <p style='text-align: center; color: #ccc;'>Manajemen keuangan interaktif untuk Hotel Kreatif Indonesia</p>
    <hr style='border: 1px solid #D4AF37;'>
    """, unsafe_allow_html=True
)

# ---------------------- INPUT TRANSAKSI ----------------------
st.sidebar.header("Tambah Transaksi")
with st.sidebar.form("form_transaksi"):
    tanggal = st.date_input("Tanggal")
    kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil", "Investasi Blockchain"])
    deskripsi = st.text_input("Deskripsi")
    jumlah = st.number_input("Jumlah (IDR)", format="%.2f")
    investor = st.text_input("Investor (kosongkan jika tidak relevan)", value="N/A")
    submit = st.form_submit_button("Tambah Transaksi")

if submit:
    new_transaksi = pd.DataFrame({
        "Tanggal": [tanggal],
        "Kategori": [kategori],
        "Deskripsi": [deskripsi],
        "Jumlah": [jumlah if kategori in ["Pemasukan", "Pertumbuhan"] else -jumlah],
        "Investor": [investor]
    })
    st.session_state.transaksi = pd.concat([st.session_state.transaksi, new_transaksi], ignore_index=True)
    st.session_state.transaksi.to_csv("transaksi.csv", index=False)
    st.success("Transaksi ditambahkan!")

# ---------------------- UPLOAD CSV ----------------------
st.sidebar.header("Impor Data CSV")
uploaded_file = st.sidebar.file_uploader("Unggah file CSV", type=["csv"])
if uploaded_file:
    uploaded_data = pd.read_csv(uploaded_file)
    uploaded_data["Tanggal"] = pd.to_datetime(uploaded_data["Tanggal"])
    st.session_state.transaksi = pd.concat([st.session_state.transaksi, uploaded_data], ignore_index=True)
    st.session_state.transaksi.to_csv("transaksi.csv", index=False)
    st.success("Data CSV diimpor!")

# ---------------------- FILTER DATA ----------------------
st.header("Filter Transaksi")
col1, col2, col3 = st.columns(3)
with col1:
    filter_kategori = st.multiselect("Kategori", options=["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil", "Investasi Blockchain"], default=["Pemasukan", "Pengeluaran"])
with col2:
    filter_investor = st.multiselect("Investor", options=st.session_state.transaksi["Investor"].unique(), default=["Mochamad Tabrani", "Pipit", "Sangaji", "Asmin", "Rasyid"])
with col3:
    date_range = st.date_input("Rentang Tanggal", [datetime(2025, 9, 1), datetime(2025, 9, 30)])
filtered_data = st.session_state.transaksi[
    (st.session_state.transaksi["Kategori"].isin(filter_kategori)) &
    (st.session_state.transaksi["Investor"].isin(filter_investor)) &
    (st.session_state.transaksi["Tanggal"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# ---------------------- METRICS ----------------------
total_pemasukan = filtered_data[filtered_data["Kategori"] == "Pemasukan"]["Jumlah"].sum()
total_pengeluaran = abs(filtered_data[filtered_data["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
dana_manajer = abs(filtered_data[filtered_data["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
dana_cadangan = abs(filtered_data[filtered_data["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
pertumbuhan = filtered_data[filtered_data["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
bagi_hasil = abs(filtered_data[filtered_data["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
saldo = filtered_data["Jumlah"].sum()

st.header("Ringkasan Keuangan")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Pemasukan", f"Rp {total_pemasukan:,.0f}")
col2.metric("📉 Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("🧑‍💼 Dana Manajer", f"Rp {dana_manajer:,.0f}")
col4.metric("📊 Saldo", f"Rp {saldo:,.0f}")
col5, col6, col7 = st.columns(3)
col5.metric("🏦 Dana Cadangan", f"Rp {dana_cadangan:,.0f}")
col6.metric("📈 Pertumbuhan", f"Rp {pertumbuhan:,.0f}")
col7.metric("🤝 Bagi Hasil", f"Rp {bagi_hasil:,.0f}")

# ---------------------- TABS ----------------------
tab1, tab2, tab3 = st.tabs(["📊 Grafik", "📑 Transaksi", "🏆 Investor"])

with tab1:
    st.subheader("Grafik Keuangan")
    
    # Pie Chart: Distribusi Pemasukan per Investor
    try:
        pie_data = filtered_data[filtered_data["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
        if not pie_data.empty and pie_data["Jumlah"].sum() > 0:
            fig_pie = px.pie(pie_data, values="Jumlah", names="Investor", title="Distribusi Pemasukan per Investor", 
                             color_discrete_sequence=px.colors.sequential.Golds)
            fig_pie.update_traces(textinfo="percent+label", pull=[0.1 if i == pie_data["Jumlah"].idxmax() else 0 for i in range(len(pie_data))])
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("Tidak ada data pemasukan untuk ditampilkan.")
    except Exception as e:
        st.error(f"Gagal membuat pie chart: {str(e)}")

    # Bar Chart: Dana Manajer, Cadangan, Bagi Hasil
    bar_data = pd.DataFrame({
        "Kategori": ["Dana Manajer", "Dana Cadangan", "Bagi Hasil"],
        "Jumlah": [dana_manajer, dana_cadangan, bagi_hasil]
    })
    fig_bar = px.bar(bar_data, x="Kategori", y="Jumlah", title="Perbandingan Dana", 
                     color_discrete_sequence=["#D4AF37"], text="Jumlah")
    fig_bar.update_traces(texttemplate="Rp %{text:,.0f}", textposition="auto")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart: Tren Saldo
    if not filtered_data.empty:
        tren_data = filtered_data.sort_values("Tanggal")
        tren_data["Saldo Kumulatif"] = tren_data["Jumlah"].cumsum()
        fig_tren = px.line(tren_data, x="Tanggal", y="Saldo Kumulatif", title="Tren Saldo Harian", 
                           color_discrete_sequence=["#D4AF37"])
        fig_tren.update_traces(line=dict(width=3))
        st.plotly_chart(fig_tren, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk tren saldo.")

with tab2:
    st.subheader("📑 Daftar Transaksi")
    st.dataframe(filtered_data, use_container_width=True, height=400)
    
    # Ekspor CSV
    if st.button("Unduh Data sebagai CSV"):
        filtered_data.to_csv("export_transaksi.csv", index=False)
        with open("export_transaksi.csv", "rb") as file:
            st.download_button("Unduh CSV", file, file_name="transaksi_hocindo.csv")

with tab3:
    st.subheader("🏆 Ranking Investor")
    ranking = filtered_data[filtered_data["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
    ranking = ranking.sort_values("Jumlah", ascending=False)
    ranking["Jumlah"] = ranking["Jumlah"].apply(lambda x: f"Rp {x:,.0f}")
    st.table(ranking)

# ---------------------- CATATAN ----------------------
st.markdown("**Catatan**: Gunakan filter untuk analisis spesifik. Data disimpan di `transaksi.csv`. Hubungi admin untuk kata sandi atau pertanyaan.")
