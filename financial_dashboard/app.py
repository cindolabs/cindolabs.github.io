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

# ---------------------- CUSTOM THEME ----------------------
st.markdown("""
    <style>
    /* Background & font */
    .main { background: linear-gradient(to bottom right, #002f25, #004c3f); color: #D4AF37; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3, h4 { color: #FFD700; font-weight: 700; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background: #1a3c34; color: #FFD700; }
    [data-testid="stSidebar"] h2 { color: #FFD700; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FFD700, #b8860b);
        color: #004c3f;
        font-weight: bold;
        border-radius: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #b8860b, #FFD700);
    }

    /* Metrics */
    .stMetric {
        background: #2e5d4f;
        border-radius: 12px;
        padding: 15px;
        color: #FFFFFF !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }

    /* Dataframe */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

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

# ---------------------- LOAD SESSION ----------------------
if "transaksi" not in st.session_state:
    st.session_state.transaksi = load_data()
df = st.session_state.transaksi

# ---------------------- TITLE ----------------------
st.title("💼 Dashboard Keuangan Hocindo")
st.caption("📊 Manajemen keuangan modern dengan visualisasi interaktif")

# ---------------------- SIDEBAR ----------------------
st.sidebar.header("📌 Menu")
menu = st.sidebar.radio("Navigasi", ["Input Transaksi", "Upload Data", "Ringkasan & Grafik", "Export Data"])

# ---------------------- INPUT TRANSAKSI ----------------------
if menu == "Input Transaksi":
    st.subheader("➕ Tambah Transaksi Baru")
    with st.form("form_transaksi", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal", datetime.today())
            kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil"])
        with col2:
            jumlah = st.number_input("Jumlah (IDR)", format="%.2f")
            investor = st.text_input("Investor", value="N/A")
        deskripsi = st.text_input("Deskripsi")
        submit = st.form_submit_button("Simpan Transaksi")

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
        st.success("✅ Transaksi berhasil ditambahkan!")

# ---------------------- UPLOAD CSV ----------------------
if menu == "Upload Data":
    st.subheader("📂 Upload CSV/XLSX")
    uploaded = st.file_uploader("Upload file transaksi", type=["csv", "xlsx"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                new_df = pd.read_csv(uploaded)
            else:
                new_df = pd.read_excel(uploaded)
            new_df["Tanggal"] = pd.to_datetime(new_df["Tanggal"])
            df = pd.concat([df, new_df], ignore_index=True).drop_duplicates().reset_index(drop=True)
            save_data(df)
            st.session_state.transaksi = df
            st.success("✅ Data berhasil digabung!")
        except Exception as e:
            st.error(f"❌ Gagal membaca file: {e}")

# ---------------------- RINGKASAN ----------------------
if menu == "Ringkasan & Grafik":
    st.subheader("📋 Daftar Transaksi")
    st.dataframe(df, use_container_width=True)

    # Hitung ringkasan
    total_pemasukan = df[df["Kategori"] == "Pemasukan"]["Jumlah"].sum()
    total_pengeluaran = abs(df[df["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
    dana_manajer = abs(df[df["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
    dana_cadangan = abs(df[df["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
    pertumbuhan = df[df["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
    bagi_hasil = abs(df[df["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
    saldo = total_pemasukan - total_pengeluaran - dana_manajer - dana_cadangan - bagi_hasil + pertumbuhan

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Pemasukan", f"Rp {total_pemasukan:,.0f}")
    col2.metric("📉 Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    col3.metric("📊 Saldo", f"Rp {saldo:,.0f}")
    col4, col5, col6 = st.columns(3)
    col4.metric("🧑‍💼 Dana Manajer", f"Rp {dana_manajer:,.0f}")
    col5.metric("🏦 Dana Cadangan", f"Rp {dana_cadangan:,.0f}")
    col6.metric("📈 Pertumbuhan", f"Rp {pertumbuhan:,.0f}")
    st.metric("🤝 Bagi Hasil", f"Rp {bagi_hasil:,.0f}")

    # Tabs Visualisasi
    st.subheader("📊 Visualisasi Interaktif")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pie Investor", "Bar Dana", "Tren Saldo", "Treemap", "Ranking Investor"])

    with tab1:
        pie_data = df[df["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
        if not pie_data.empty:
            fig = px.pie(pie_data, values="Jumlah", names="Investor", hole=0.3,
                         color_discrete_sequence=px.colors.sequential.Golds)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        bar_data = pd.DataFrame({
            "Kategori": ["Dana Manajer", "Dana Cadangan", "Bagi Hasil"],
            "Jumlah": [dana_manajer, dana_cadangan, bagi_hasil]
        })
        fig = px.bar(bar_data, x="Kategori", y="Jumlah", text="Jumlah",
                     color="Kategori", color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        df_sorted = df.sort_values("Tanggal")
        df_sorted["Saldo Kumulatif"] = df_sorted["Jumlah"].cumsum()
        fig = px.line(df_sorted, x="Tanggal", y="Saldo Kumulatif", markers=True,
                      color_discrete_sequence=["#FFD700"])
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        treemap_data = df.groupby(["Kategori", "Investor"])["Jumlah"].sum().reset_index()
        if not treemap_data.empty:
            fig = px.treemap(treemap_data, path=["Kategori", "Investor"], values="Jumlah", color="Jumlah",
                             color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        ranking = df[df["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
        ranking = ranking.sort_values("Jumlah", ascending=False).head(5)
        st.table(ranking)

# ---------------------- EXPORT ----------------------
if menu == "Export Data":
    st.subheader("⬇️ Unduh Data")
    st.download_button("💾 Unduh CSV", data=df.to_csv(index=False), file_name="transaksi_hocindo.csv", mime="text/csv")
    st.download_button("📊 Unduh Excel", data=df.to_excel("export.xlsx", index=False), file_name="transaksi_hocindo.xlsx", mime="application/vnd.ms-excel")
