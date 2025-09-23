import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Dashboard Keuangan Modern",
    page_icon="💰",
    layout="wide"
)

# ---------------------- DATA AWAL ----------------------
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
df = pd.DataFrame(data)

# ---------------------- TAMBAH KOLOM BUNGA ----------------------
def hitung_bunga(row):
    if row["Kategori"] == "Pemasukan":
        return row["Jumlah"] * 0.05  # bunga 5%
    return 0

df["Bunga"] = df.apply(hitung_bunga, axis=1)
df = df[["Tanggal", "Kategori", "Deskripsi", "Jumlah", "Investor", "Bunga"]]

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #2ecc71;'>💼 Dashboard Keuangan Hocindo</h1>
    <p style='text-align: center; color: #27ae60;'>Visualisasi interaktif dan ringkasan keuangan terkini</p>
    <hr style='border: 1px solid #27ae60;'>
    """, unsafe_allow_html=True
)

# ---------------------- METRICS ----------------------
total_pemasukan = df[df["Kategori"] == "Pemasukan"]["Jumlah"].sum()
total_pengeluaran = abs(df[df["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
dana_manajer = abs(df[df["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
dana_cadangan = abs(df[df["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
pertumbuhan = df[df["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
bagi_hasil = abs(df[df["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
saldo = df["Jumlah"].sum()

# Styling untuk metrics
st.markdown("""
    <style>
    .metric-card {
        background: rgba(46, 204, 113, 0.15);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #006400;
    }
    .metric-value {
        font-size: 20px;
        color: #004d00;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("### 📌 Ringkasan Keuangan")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>💰 Pemasukan</div><div class='metric-value'>Rp {total_pemasukan:,.0f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📉 Pengeluaran</div><div class='metric-value'>Rp {total_pengeluaran:,.0f}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🧑‍💼 Dana Manajer</div><div class='metric-value'>Rp {dana_manajer:,.0f}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📊 Saldo</div><div class='metric-value'>Rp {saldo:,.0f}</div></div>", unsafe_allow_html=True)

col5, col6, col7 = st.columns(3)
with col5:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🏦 Dana Cadangan</div><div class='metric-value'>Rp {dana_cadangan:,.0f}</div></div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📈 Pertumbuhan</div><div class='metric-value'>Rp {pertumbuhan:,.0f}</div></div>", unsafe_allow_html=True)
with col7:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🤝 Bagi Hasil</div><div class='metric-value'>Rp {bagi_hasil:,.0f}</div></div>", unsafe_allow_html=True)

# ---------------------- NAVIGASI ----------------------
menu = st.sidebar.radio("Navigasi", ["📊 Grafik", "📑 Transaksi", "🏆 Investor"])

if menu == "📊 Grafik":
    st.subheader("📊 Grafik Keuangan")
    colA, colB, colC = st.columns(3)

    with colA:
        pie_chart = px.pie(
            df[df["Kategori"] == "Pemasukan"],
            names="Investor",
            values="Jumlah",
            title="Distribusi Pemasukan per Investor",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        st.plotly_chart(pie_chart, use_container_width=True)

    with colB:
        line_chart = px.line(
            df,
            x="Tanggal",
            y="Jumlah",
            color="Kategori",
            markers=True,
            title="Tren Keuangan",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        st.plotly_chart(line_chart, use_container_width=True)

    with colC:
        bar_chart = px.bar(
            df[df["Kategori"] == "Pemasukan"],
            x="Investor",
            y="Bunga",
            title="Bunga per Investor",
            color="Investor",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        st.plotly_chart(bar_chart, use_container_width=True)

elif menu == "📑 Transaksi":
    st.subheader("📑 Daftar Transaksi Lengkap")
    st.dataframe(df, use_container_width=True, height=400)

    # Tambahan tabel pemasukan
    st.markdown("### 💰 Rincian Pemasukan")
    pemasukan_df = df[df["Kategori"] == "Pemasukan"][["Tanggal", "Deskripsi", "Jumlah", "Investor", "Bunga"]]
    st.dataframe(
        pemasukan_df.style.format({"Jumlah": "Rp {:,.0f}", "Bunga": "Rp {:,.0f}"}).applymap(
            lambda _: "background-color: rgba(0,255,0,0.2)", subset=["Jumlah", "Bunga"]
        ),
        use_container_width=True,
        height=300
    )

    # Tambahan tabel pengeluaran
    st.markdown("### 📉 Rincian Pengeluaran")
    pengeluaran_df = df[df["Kategori"] == "Pengeluaran"][["Tanggal", "Deskripsi", "Jumlah"]]
    st.dataframe(
        pengeluaran_df.style.format({"Jumlah": "Rp {:,.0f}"}).applymap(
            lambda _: "background-color: rgba(255,0,0,0.2)", subset=["Jumlah"]
        ),
        use_container_width=True,
        height=200
    )

elif menu == "🏆 Investor":
    st.subheader("🏆 Ranking Investor (Pemasukan + Bunga)")
    ranking = df[df["Kategori"] == "Pemasukan"].groupby("Investor")[["Jumlah", "Bunga"]].sum().reset_index()
    ranking["Total"] = ranking["Jumlah"] + ranking["Bunga"]
    ranking = ranking.sort_values("Total", ascending=False)
    st.table(ranking)
