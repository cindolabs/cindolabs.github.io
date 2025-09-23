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

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #FFD700;'>💼 Dashboard Keuangan Hocindo</h1>
    <p style='text-align: center; color: #ccc;'>Visualisasi interaktif dan ringkasan keuangan terkini</p>
    <hr style='border: 1px solid #444;'>
    """, unsafe_allow_html=True
)

# ---------------------- METRICS ----------------------
col1, col2, col3, col4 = st.columns(4)

total_pemasukan = df[df["Kategori"] == "Pemasukan"]["Jumlah"].sum()
total_pengeluaran = abs(df[df["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
dana_manajer = abs(df[df["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
dana_cadangan = abs(df[df["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
pertumbuhan = df[df["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
bagi_hasil = abs(df[df["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
saldo = df["Jumlah"].sum()

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
    colA, colB = st.columns(2)

    # Pie Chart Pemasukan per Investor
    with colA:
        pie_data = df[df["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
        fig_pie = px.pie(pie_data, values="Jumlah", names="Investor", hole=0.4,
                         title="Distribusi Investor", color_discrete_sequence=px.colors.sequential.Gold)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Line Chart Saldo
    with colB:
        df_sorted = df.sort_values("Tanggal")
        df_sorted["Saldo Kumulatif"] = df_sorted["Jumlah"].cumsum()
        fig_line = px.line(df_sorted, x="Tanggal", y="Saldo Kumulatif", markers=True,
                           title="Pergerakan Saldo", color_discrete_sequence=["#FFD700"])
        st.plotly_chart(fig_line, use_container_width=True)

    # Bar Chart Dana
    st.subheader("Dana Manajer, Cadangan, dan Bagi Hasil")
    bar_data = pd.DataFrame({
        "Kategori": ["Dana Manajer", "Dana Cadangan", "Bagi Hasil"],
        "Jumlah": [dana_manajer, dana_cadangan, bagi_hasil]
    })
    fig_bar = px.bar(bar_data, x="Kategori", y="Jumlah", text="Jumlah",
                     title="Perbandingan Dana", color="Kategori",
                     color_discrete_map={
                         "Dana Manajer": "#FFD700",
                         "Dana Cadangan": "#DAA520",
                         "Bagi Hasil": "#B8860B"
                     })
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("📑 Daftar Transaksi")
    st.dataframe(df, use_container_width=True, height=400)

with tab3:
    st.subheader("🏆 Ranking Investor")
    ranking = df[df["Kategori"] == "Pemasukan"].groupby("Investor")["Jumlah"].sum().reset_index()
    ranking = ranking.sort_values("Jumlah", ascending=False)
    st.table(ranking)
