import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Tema Hocindo dengan kontras lebih baik
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #006847, #004c3f); color: #D4AF37; }
    .sidebar .sidebar-content { background: #1a3c34; color: #D4AF37; }
    h1, h2, h3, h4 { color: #D4AF37; }
    .stButton>button { background: linear-gradient(to right, #D4AF37, #b8860b); color: #004c3f; }
    .stMetric { background: #2e5d4f; border-radius: 10px; padding: 10px; color: #FFFFFF !important; }
    .stMetric label { color: #FFFFFF !important; }
    .stMetric .metric-value { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("Dashboard Keuangan Hocindo - Lanjutan")

# Inisialisasi data
if 'transaksi' not in st.session_state:
    # Muat data dari CSV jika ada
    if os.path.exists("transaksi.csv"):
        st.session_state.transaksi = pd.read_csv("transaksi.csv")
        st.session_state.transaksi["Tanggal"] = pd.to_datetime(st.session_state.transaksi["Tanggal"])
    else:
        # Data awal berdasarkan input Anda
        initial_data = [
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Mochamad Tabrani", "Jumlah": 50000, "Investor": "Mochamad Tabrani"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Pipit", "Jumlah": 50000, "Investor": "Pipit"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Sangaji", "Jumlah": 100000, "Investor": "Sangaji"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Asmin", "Jumlah": 135000, "Investor": "Asmin"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pemasukan", "Deskripsi": "Investasi Rasyid", "Jumlah": 50000, "Investor": "Rasyid"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pengeluaran", "Deskripsi": "Biaya Operasional", "Jumlah": -10000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Dana Manajer", "Deskripsi": "Dana Dikelola Manajer", "Jumlah": -100000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Dana Cadangan", "Deskripsi": "Dana Cadangan", "Jumlah": -275000, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Pertumbuhan", "Deskripsi": "Pertumbuhan Dana Manajer", "Jumlah": 900, "Investor": "N/A"},
            {"Tanggal": datetime(2025, 9, 23), "Kategori": "Bagi Hasil", "Deskripsi": "Bagi Hasil Investor", "Jumlah": -100, "Investor": "N/A"}
        ]
        st.session_state.transaksi = pd.DataFrame(initial_data)
        st.session_state.transaksi["Tanggal"] = pd.to_datetime(st.session_state.transaksi["Tanggal"])
        st.session_state.transaksi.to_csv("transaksi.csv", index=False)

# Sidebar untuk input transaksi
st.sidebar.header("Input Transaksi Baru")
with st.sidebar.form("form_transaksi"):
    tanggal = st.date_input("Tanggal")
    kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil"])
    deskripsi = st.text_input("Deskripsi")
    jumlah = st.number_input("Jumlah (IDR)", format="%.2f")
    investor = st.text_input("Investor (kosongkan jika tidak relevan)", value="N/A")
    submit = st.form_submit_button("Tambah Transaksi")

# Tambah transaksi baru
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

# Filter data
st.header("Filter Transaksi")
col1, col2 = st.columns(2)
with col1:
    filter_kategori = st.multiselect("Pilih Kategori", options=["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil"], default=["Pemasukan", "Pengeluaran"])
with col2:
    filter_investor = st.multiselect("Pilih Investor", options=st.session_state.transaksi["Investor"].unique(), default=["Mochamad Tabrani", "Pipit", "Sangaji", "Asmin", "Rasyid"])
filtered_data = st.session_state.transaksi[
    (st.session_state.transaksi["Kategori"].isin(filter_kategori)) &
    (st.session_state.transaksi["Investor"].isin(filter_investor))
]

# Tabel transaksi
st.header("Daftar Transaksi")
st.dataframe(filtered_data)

# Ringkasan keuangan
total_pemasukan = st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Pemasukan"]["Jumlah"].sum()
total_pengeluaran = abs(st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
dana_manajer = abs(st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
dana_cadangan = abs(st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
pertumbuhan = st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
bagi_hasil = abs(st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
saldo = total_pemasukan - total_pengeluaran - dana_manajer - dana_cadangan - bagi_hasil + pertumbuhan

# Metrik dengan warna lebih jelas
st.header("Ringkasan Keuangan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.2f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.2f}")
col3.metric("Saldo Bersih", f"Rp {saldo:,.2f}")
col4, col5, col6 = st.columns(3)
col4.metric("Dana Manajer", f"Rp {dana_manajer:,.2f}")
col5.metric("Dana Cadangan", f"Rp {dana_cadangan:,.2f}")
col6.metric("Pertumbuhan", f"Rp {pertumbuhan:,.2f}")
st.metric("Bagi Hasil", f"Rp {bagi_hasil:,.2f}")

# Visualisasi 1: Pie chart distribusi pemasukan per investor
st.header("Distribusi Pemasukan per Investor")
try:
    pie_data = filtered_data[filtered_data["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
    if not pie_data.empty and pie_data["Jumlah"].sum() > 0:
        fig_pie = px.pie(pie_data, values="Jumlah", names="Investor", title="Pemasukan per Investor", color_discrete_sequence=px.colors.sequential.Golds)
        st.plotly_chart(fig_pie)
    else:
        st.warning("Tidak ada data pemasukan untuk ditampilkan dalam pie chart.")
except Exception as e:
    st.error("Gagal membuat pie chart. Periksa data pemasukan.")
    st.write(f"Detail error: {str(e)}")

# Visualisasi 2: Bar chart untuk dana manajer, cadangan, dan bagi hasil
st.header("Dana Manajer, Cadangan, dan Bagi Hasil")
bar_data = pd.DataFrame({
    "Kategori": ["Dana Manajer", "Dana Cadangan", "Bagi Hasil"],
    "Jumlah": [dana_manajer, dana_cadangan, bagi_hasil]
})
fig_bar = px.bar(bar_data, x="Kategori", y="Jumlah", title="Perbandingan Dana", color_discrete_sequence=["#D4AF37"])
st.plotly_chart(fig_bar)

# Visualisasi 3: Tren saldo harian
st.header("Tren Saldo Harian")
if not filtered_data.empty:
    tren_data = filtered_data.sort_values("Tanggal")
    tren_data["Saldo Kumulatif"] = tren_data["Jumlah"].cumsum()
    fig_tren = px.line(tren_data, x="Tanggal", y="Saldo Kumulatif", title="Tren Saldo Harian", color_discrete_sequence=["#D4AF37"])
    st.plotly_chart(fig_tren)
else:
    st.warning("Tidak ada data untuk ditampilkan dalam tren saldo.")

# Ekspor data
st.header("Ekspor Data")
if st.button("Unduh Data sebagai CSV"):
    filtered_data.to_csv("export_transaksi.csv", index=False)
    with open("export_transaksi.csv", "rb") as file:
        st.download_button("Unduh CSV", file, file_name="transaksi_hocindo.csv")

# Catatan
st.write("Catatan: Gunakan filter untuk analisis spesifik. Data disimpan secara permanen di transaksi.csv.")
