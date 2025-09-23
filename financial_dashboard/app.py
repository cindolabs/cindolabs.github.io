import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ---------------------- THEME & STYLE ----------------------
st.set_page_config(page_title="Dashboard Keuangan Hocindo", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #006847, #004c3f); color: #D4AF37; }
    .sidebar .sidebar-content { background: #1a3c34; color: #D4AF37; }
    h1, h2, h3, h4 { color: #D4AF37; font-weight: bold; }
    .stButton>button { background: linear-gradient(to right, #D4AF37, #b8860b); color: #004c3f; font-weight: bold; border-radius: 8px; }
    .stMetric { background: #2e5d4f; border-radius: 12px; padding: 10px; color: #FFFFFF !important; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# ---------------------- FUNCTIONS ----------------------
def load_data():
    if os.path.exists("transaksi.csv"):
        df = pd.read_csv("transaksi.csv")
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        return df
    else:
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
        df = pd.DataFrame(initial_data)
        df.to_csv("transaksi.csv", index=False)
        return df

def save_data(df):
    df.to_csv("transaksi.csv", index=False)

# ---------------------- LOAD DATA ----------------------
if "transaksi" not in st.session_state:
    st.session_state.transaksi = load_data()

df = st.session_state.transaksi

# ---------------------- TITLE ----------------------
st.title("💼 Dashboard Keuangan Hocindo")

# ---------------------- SIDEBAR INPUT ----------------------
st.sidebar.header("➕ Input Transaksi Baru")
with st.sidebar.form("form_transaksi"):
    tanggal = st.date_input("Tanggal", datetime.today())
    kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil"])
    deskripsi = st.text_input("Deskripsi")
    jumlah = st.number_input("Jumlah (IDR)", format="%.2f")
    investor = st.text_input("Investor (kosongkan jika tidak relevan)", value="N/A")
    submit = st.form_submit_button("Tambah Transaksi")

if submit:
    new_data = pd.DataFrame([{
        "Tanggal": tanggal,
        "Kategori": kategori,
        "Deskripsi": deskripsi,
        "Jumlah": jumlah if kategori in ["Pemasukan", "Pertumbuhan"] else -jumlah,
        "Investor": investor
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    st.session_state.transaksi = df
    st.sidebar.success("✅ Transaksi berhasil ditambahkan!")

# ---------------------- UPLOAD CSV ----------------------
st.sidebar.header("📂 Upload CSV Eksternal")
uploaded_file = st.sidebar.file_uploader("Upload file CSV transaksi", type="csv")

if uploaded_file is not None:
    try:
        new_df = pd.read_csv(uploaded_file)
        new_df["Tanggal"] = pd.to_datetime(new_df["Tanggal"])
        # Gabung data lama + baru, hapus duplikat
        df = pd.concat([df, new_df], ignore_index=True).drop_duplicates().reset_index(drop=True)
        save_data(df)
        st.session_state.transaksi = df
        st.sidebar.success("✅ Data CSV berhasil di-merge!")
    except Exception as e:
        st.sidebar.error(f"Gagal membaca file: {e}")

# ---------------------- FILTER ----------------------
st.header("🔎 Filter Transaksi")
col1, col2 = st.columns(2)
with col1:
    filter_kategori = st.multiselect("Pilih Kategori", df["Kategori"].unique(), default=df["Kategori"].unique())
with col2:
    filter_investor = st.multiselect("Pilih Investor", df["Investor"].unique(), default=df["Investor"].unique())

filtered = df[(df["Kategori"].isin(filter_kategori)) & (df["Investor"].isin(filter_investor))]

# ---------------------- TABEL ----------------------
st.header("📋 Daftar Transaksi")
st.dataframe(filtered, use_container_width=True)

# ---------------------- RINGKASAN ----------------------
st.header("📊 Ringkasan Keuangan")
total_pemasukan = df[df["Kategori"] == "Pemasukan"]["Jumlah"].sum()
total_pengeluaran = abs(df[df["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
dana_manajer = abs(df[df["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
dana_cadangan = abs(df[df["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
pertumbuhan = df[df["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
bagi_hasil = abs(df[df["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
saldo = total_pemasukan - total_pengeluaran - dana_manajer - dana_cadangan - bagi_hasil + pertumbuhan

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Pemasukan", f"Rp {total_pemasukan:,.2f}")
col2.metric("📉 Total Pengeluaran", f"Rp {total_pengeluaran:,.2f}")
col3.metric("📊 Saldo Bersih", f"Rp {saldo:,.2f}")
col4, col5, col6 = st.columns(3)
col4.metric("🧑‍💼 Dana Manajer", f"Rp {dana_manajer:,.2f}")
col5.metric("🏦 Dana Cadangan", f"Rp {dana_cadangan:,.2f}")
col6.metric("📈 Pertumbuhan", f"Rp {pertumbuhan:,.2f}")
st.metric("🤝 Bagi Hasil", f"Rp {bagi_hasil:,.2f}")

# ---------------------- VISUALISASI ----------------------
st.header("📈 Visualisasi Keuangan")
tab1, tab2, tab3, tab4 = st.tabs(["📊 Pie Investor", "📊 Bar Dana", "📈 Tren Saldo", "🌳 TreeMap"])

with tab1:
    pie_data = filtered[filtered["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
    if not pie_data.empty:
        fig = px.pie(pie_data, values="Jumlah", names="Investor", color_discrete_sequence=px.colors.sequential.Golds, hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data pemasukan untuk pie chart.")

with tab2:
    bar_data = pd.DataFrame({
        "Kategori": ["Dana Manajer", "Dana Cadangan", "Bagi Hasil"],
        "Jumlah": [dana_manajer, dana_cadangan, bagi_hasil]
    })
    fig = px.bar(bar_data, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori",
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    if not filtered.empty:
        filtered = filtered.sort_values("Tanggal")
        filtered["Saldo Kumulatif"] = filtered["Jumlah"].cumsum()
        fig = px.line(filtered, x="Tanggal", y="Saldo Kumulatif", markers=True, color_discrete_sequence=["#D4AF37"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk ditampilkan.")

with tab4:
    treemap_data = filtered.groupby(["Kategori", "Investor"])["Jumlah"].sum().reset_index()
    if not treemap_data.empty:
        fig = px.treemap(treemap_data, path=["Kategori", "Investor"], values="Jumlah", color="Jumlah",
                         color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data kosong untuk Treemap.")

# ---------------------- EKSPOR ----------------------
st.header("⬇️ Ekspor Data")
st.download_button("Unduh CSV", data=filtered.to_csv(index=False), file_name="transaksi_hocindo.csv", mime="text/csv")

st.info("ℹ️ Data disimpan otomatis di **transaksi.csv**. Anda juga bisa upload file CSV eksternal untuk digabung dengan data lama.")
