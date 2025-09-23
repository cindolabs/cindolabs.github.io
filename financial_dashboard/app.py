import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Dashboard Keuangan Hocindo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- FUNGSI UTILITAS ----------------------
def load_data():
    """Memuat dan memvalidasi data awal."""
    data = [
        {"Tanggal": datetime(2025, 9, 23, 8, 0), "Kategori": "Pemasukan", "Deskripsi": "Investasi Mochamad Tabrani", "Jumlah": 50000, "Investor": "Mochamad Tabrani"},
        {"Tanggal": datetime(2025, 9, 23, 9, 30), "Kategori": "Pemasukan", "Deskripsi": "Investasi Pipit", "Jumlah": 50000, "Investor": "Pipit"},
        {"Tanggal": datetime(2025, 9, 23, 10, 15), "Kategori": "Pemasukan", "Deskripsi": "Investasi Sangaji", "Jumlah": 100000, "Investor": "Sangaji"},
        {"Tanggal": datetime(2025, 9, 23, 11, 0), "Kategori": "Pemasukan", "Deskripsi": "Investasi Asmin", "Jumlah": 135000, "Investor": "Asmin"},
        {"Tanggal": datetime(2025, 9, 23, 12, 45), "Kategori": "Pemasukan", "Deskripsi": "Investasi Rasyid", "Jumlah": 50000, "Investor": "Rasyid"},
        {"Tanggal": datetime(2025, 9, 23, 13, 0), "Kategori": "Pengeluaran", "Deskripsi": "Biaya Operasional", "Jumlah": -10000, "Investor": "N/A"},
        {"Tanggal": datetime(2025, 9, 23, 14, 30), "Kategori": "Dana Manajer", "Deskripsi": "Dana Dikelola Manajer", "Jumlah": -100000, "Investor": "N/A"},
        {"Tanggal": datetime(2025, 9, 23, 15, 15), "Kategori": "Dana Cadangan", "Deskripsi": "Dana Cadangan", "Jumlah": -275000, "Investor": "N/A"},
        {"Tanggal": datetime(2025, 9, 23, 16, 0), "Kategori": "Pertumbuhan", "Deskripsi": "Pertumbuhan Dana Manajer", "Jumlah": 900, "Investor": "N/A"},
        {"Tanggal": datetime(2025, 9, 23, 17, 30), "Kategori": "Bagi Hasil", "Deskripsi": "Bagi Hasil Investor", "Jumlah": -100, "Investor": "N/A"},
    ]
    df = pd.DataFrame(data)
    
    # Validasi data
    if df.empty:
        st.error("Data kosong! Silakan masukkan data yang valid.")
        return None
    
    # Tambah kolom bunga
    df["Bunga"] = df.apply(lambda row: row["Jumlah"] * 0.05 if row["Kategori"] == "Pemasukan" else 0, axis=1)
    df = df[["Tanggal", "Kategori", "Deskripsi", "Jumlah", "Investor", "Bunga"]]
    
    # Format tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.strftime("%d-%m-%Y %H:%M")
    return df

def calculate_metrics(df):
    """Menghitung metrik keuangan."""
    if df is None:
        return 0, 0, 0, 0, 0, 0, 0
    
    total_pemasukan = df[df["Kategori"] == "Pemasukan"]["Jumlah"].sum()
    total_pengeluaran = abs(df[df["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
    dana_manajer = abs(df[df["Kategori"] == "Dana Manajer"]["Jumlah"].sum())
    dana_cadangan = abs(df[df["Kategori"] == "Dana Cadangan"]["Jumlah"].sum())
    pertumbuhan = df[df["Kategori"] == "Pertumbuhan"]["Jumlah"].sum()
    bagi_hasil = abs(df[df["Kategori"] == "Bagi Hasil"]["Jumlah"].sum())
    saldo = df["Jumlah"].sum()
    
    return total_pemasukan, total_pengeluaran, dana_manajer, dana_cadangan, pertumbuhan, bagi_hasil, saldo

def display_metrics(total_pemasukan, total_pengeluaran, dana_manajer, dana_cadangan, pertumbuhan, bagi_hasil, saldo):
    """Menampilkan metrik keuangan dalam kartu."""
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

def apply_filters(df):
    """Menambahkan filter interaktif untuk data."""
    if df is None:
        return None
    
    st.sidebar.markdown("### 🔍 Filter Data")
    
    # Filter tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d-%m-%Y %H:%M")
    min_date = df["Tanggal"].min().date()
    max_date = df["Tanggal"].max().date()
    date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df["Tanggal"].dt.date >= start_date) & (df["Tanggal"].dt.date <= end_date)]
    
    # Filter kategori
    categories = ["Semua"] + list(df["Kategori"].unique())
    selected_category = st.sidebar.selectbox("Pilih Kategori", categories)
    if selected_category != "Semua":
        df = df[df["Kategori"] == selected_category]
    
    # Filter investor
    investors = ["Semua"] + list(df["Investor"].unique())
    selected_investor = st.sidebar.selectbox("Pilih Investor", investors)
    if selected_investor != "Semua":
        df = df[df["Investor"] == selected_investor]
    
    # Format ulang tanggal setelah filter
    df["Tanggal"] = df["Tanggal"].dt.strftime("%d-%m-%Y %H:%M")
    return df

def download_data(df, filename="data_keuangan.csv"):
    """Fungsi untuk mengunduh data sebagai CSV."""
    if df is None:
        return
    
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Unduh Data (CSV)",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #2ecc71;'>💼 Dashboard Keuangan Hocindo</h1>
    <p style='text-align: center; color: #27ae60;'>Visualisasi interaktif dan ringkasan keuangan terkini</p>
    <hr style='border: 1px solid #27ae60;'>
    """, unsafe_allow_html=True
)

# ---------------------- LOAD DATA ----------------------
df = load_data()

# ---------------------- FILTER DATA ----------------------
filtered_df = apply_filters(df)

# ---------------------- METRIK ----------------------
total_pemasukan, total_pengeluaran, dana_manajer, dana_cadangan, pertumbuhan, bagi_hasil, saldo = calculate_metrics(filtered_df)
display_metrics(total_pemasukan, total_pengeluaran, dana_manajer, dana_cadangan, pertumbuhan, bagi_hasil, saldo)

# ---------------------- DOWNLOAD DATA ----------------------
download_data(filtered_df)

# ---------------------- NAVIGASI ----------------------
menu = st.sidebar.radio("Navigasi", ["📊 Grafik", "📑 Transaksi", "🏆 Investor", "🔥 Heatmap"])

if menu == "📊 Grafik":
    st.subheader("📊 Grafik Keuangan")
    if filtered_df is not None and not filtered_df.empty:
        colA, colB, colC = st.columns(3)
        
        with colA:
            pie_chart = px.pie(
                filtered_df[filtered_df["Kategori"] == "Pemasukan"],
                names="Investor",
                values="Jumlah",
                title="Distribusi Pemasukan per Investor",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(pie_chart, use_container_width=True)
        
        with colB:
            line_chart = px.line(
                filtered_df,
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
                filtered_df[filtered_df["Kategori"] == "Pemasukan"],
                x="Investor",
                y="Bunga",
                title="Bunga per Investor",
                color="Investor",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(bar_chart, use_container_width=True)

elif menu == "📑 Transaksi":
    st.subheader("📑 Daftar Transaksi Lengkap")
    if filtered_df is not None and not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Tabel pemasukan
        st.markdown("### 💰 Rincian Pemasukan")
        pemasukan_df = filtered_df[filtered_df["Kategori"] == "Pemasukan"][["Tanggal", "Deskripsi", "Jumlah", "Investor", "Bunga"]]
        st.dataframe(
            pemasukan_df.style.format({"Jumlah": "Rp {:,.0f}", "Bunga": "Rp {:,.0f}"}).apply(
                lambda _: ["background-color: rgba(0,255,0,0.2)"] * len(_), axis=1
            ),
            use_container_width=True,
            height=300
        )
        
        # Tabel pengeluaran
        st.markdown("### 📉 Rincian Pengeluaran")
        pengeluaran_df = filtered_df[filtered_df["Jumlah"] < 0][["Tanggal", "Kategori", "Deskripsi", "Jumlah"]]
        st.dataframe(
            pengeluaran_df.style.format({"Jumlah": "Rp {:,.0f}"}).apply(
                lambda _: ["background-color: rgba(255,0,0,0.2)"] * len(_), axis=1
            ),
            use_container_width=True,
            height=250
        )
        
        # Ringkasan pengeluaran per kategori
        st.markdown("### 🧾 Ringkasan Pengeluaran per Kategori")
        ringkasan_pengeluaran = pengeluaran_df.groupby("Kategori")[["Jumlah"]].sum().reset_index()
        ringkasan_pengeluaran["Jumlah"] = ringkasan_pengeluaran["Jumlah"].abs()
        st.dataframe(
            ringkasan_pengeluaran.style.format({"Jumlah": "Rp {:,.0f}"}).apply(
                lambda _: ["background-color: rgba(255,200,200,0.5)"] * len(_), axis=1
            ),
            use_container_width=True,
            height=200
        )
        
        # Grafik pie chart pengeluaran
        st.markdown("### 📊 Grafik Pengeluaran per Kategori")
        pie_pengeluaran = px.pie(
            ringkasan_pengeluaran,
            names="Kategori",
            values="Jumlah",
            title="Distribusi Pengeluaran per Kategori",
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(pie_pengeluaran, use_container_width=True)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter.")

elif menu == "🏆 Investor":
    st.subheader("🏆 Ranking Investor (Pemasukan + Bunga)")
    if filtered_df is not None and not filtered_df.empty:
        ranking = filtered_df[filtered_df["Kategori"] == "Pemasukan"].groupby("Investor")[["Jumlah", "Bunga"]].sum().reset_index()
        ranking["Total"] = ranking["Jumlah"] + ranking["Bunga"]
        ranking = ranking.sort_values("Total", ascending=False)
        st.dataframe(
            ranking.style.format({"Jumlah": "Rp {:,.0f}", "Bunga": "Rp {:,.0f}", "Total": "Rp {:,.0f}"}),
            use_container_width=True
        )
    else:
        st.warning("Tidak ada data investor yang sesuai dengan filter.")

elif menu == "🔥 Heatmap":
    st.subheader("🔥 Heatmap Korelasi Keuangan")
    if filtered_df is not None and not filtered_df.empty:
        # Membuat pivot table untuk heatmap
        pivot_table = filtered_df.pivot_table(values="Jumlah", index="Kategori", columns="Investor", aggfunc="sum", fill_value=0)
        heatmap = px.imshow(
            pivot_table,
            title="Heatmap Kontribusi Keuangan per Kategori dan Investor",
            color_continuous_scale="Greens",
            labels={"color": "Jumlah (Rp)"}
        )
        st.plotly_chart(heatmap, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk heatmap.")
