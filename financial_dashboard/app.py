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
    {"Tanggal": datetime(2025, 9, 23, 8, 0), "Kategori": "Pemasukan", "Deskripsi": "Investasi Mochamad Tabrani", "Jumlah": 50000, "Investor": "Mochamad Tabrani"},
    {"Tanggal": datetime(2025, 9, 23, 9, 30), "Kategori": "Pemasukan", "Deskripsi": "Investasi Pipit", "Jumlah": 50000, "Investor": "Pipit"},
    {"Tanggal": datetime(2025, 9, 23, 10, 0), "Kategori": "Pemasukan", "Deskripsi": "Investasi Sangaji", "Jumlah": 100000, "Investor": "Sangaji"},
    {"Tanggal": datetime(2025, 9, 23, 11, 15), "Kategori": "Pemasukan", "Deskripsi": "Investasi Asmin", "Jumlah": 135000, "Investor": "Asmin"},
    {"Tanggal": datetime(2025, 9, 23, 13, 45), "Kategori": "Pemasukan", "Deskripsi": "Investasi Rasyid", "Jumlah": 50000, "Investor": "Rasyid"},
    {"Tanggal": datetime(2025, 9, 23, 14, 0), "Kategori": "Pengeluaran", "Deskripsi": "Biaya Operasional", "Jumlah": -10000, "Investor": "N/A"},
    {"Tanggal": datetime(2025, 9, 23, 15, 0), "Kategori": "Dana Manajer", "Deskripsi": "Dana Dikelola Manajer", "Jumlah": -100000, "Investor": "N/A"},
    {"Tanggal": datetime(2025, 9, 23, 16, 0), "Kategori": "Dana Cadangan", "Deskripsi": "Dana Cadangan", "Jumlah": -275000, "Investor": "N/A"},
    {"Tanggal": datetime(2025, 9, 23, 17, 0), "Kategori": "Pertumbuhan", "Deskripsi": "Pertumbuhan Dana Manajer", "Jumlah": 900, "Investor": "N/A"},
    {"Tanggal": datetime(2025, 9, 23, 18, 0), "Kategori": "Bagi Hasil", "Deskripsi": "Bagi Hasil Investor", "Jumlah": -100, "Investor": "N/A"},
]
df = pd.DataFrame(data)

# ---------------------- TAMBAH KOLOM BUNGA ----------------------
def hitung_bunga(row):
    if row["Kategori"] == "Pemasukan":
        return row["Jumlah"] * 0.05  # bunga 5%
    return 0

df["Bunga"] = df.apply(hitung_bunga, axis=1)
df = df[["Tanggal", "Kategori", "Deskripsi", "Jumlah", "Investor", "Bunga"]]

# ---------------------- FORM INPUT ----------------------
st.sidebar.header("➕ Tambah Transaksi Baru")

with st.sidebar.form("form_transaksi"):
    tgl = st.date_input("Tanggal", datetime.now())
    jam = st.time_input("Jam", datetime.now().time())
    kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran", "Dana Manajer", "Dana Cadangan", "Pertumbuhan", "Bagi Hasil"])
    deskripsi = st.text_input("Deskripsi")
    jumlah = st.number_input("Jumlah (Rp)", step=1000, format="%d")
    investor = st.text_input("Investor (isi N/A jika tidak ada)")
    submit = st.form_submit_button("Tambah")

    if submit:
        new_datetime = datetime.combine(tgl, jam)
        new_data = {"Tanggal": new_datetime, "Kategori": kategori, "Deskripsi": deskripsi, "Jumlah": jumlah, "Investor": investor}
        new_data["Bunga"] = jumlah * 0.05 if kategori == "Pemasukan" else 0
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        st.success("✅ Transaksi berhasil ditambahkan!")

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

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Pemasukan", f"Rp {total_pemasukan:,.0f}")
col2.metric("📉 Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col3.metric("🧑‍💼 Dana Manajer", f"Rp {dana_manajer:,.0f}")
col4.metric("📊 Saldo", f"Rp {saldo:,.0f}")

col5, col6, col7 = st.columns(3)
col5.metric("🏦 Dana Cadangan", f"Rp {dana_cadangan:,.0f}")
col6.metric("📈 Pertumbuhan", f"Rp {pertumbuhan:,.0f}")
col7.metric("🤝 Bagi Hasil", f"Rp {bagi_hasil:,.0f}")

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
    df_fmt = df.copy()
    df_fmt["Tanggal"] = pd.to_datetime(df_fmt["Tanggal"]).dt.strftime("%d-%m-%Y %H:%M")
    st.dataframe(df_fmt, use_container_width=True, height=450)

elif menu == "🏆 Investor":
    st.subheader("🏆 Ranking Investor (Pemasukan + Bunga)")
    ranking = df[df["Kategori"] == "Pemasukan"].groupby("Investor")[["Jumlah", "Bunga"]].sum().reset_index()
    ranking["Total"] = ranking["Jumlah"] + ranking["Bunga"]
    ranking = ranking.sort_values("Total", ascending=False)
    st.table(ranking)
