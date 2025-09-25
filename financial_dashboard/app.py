import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Konfigurasi Streamlit
st.set_page_config(page_title="Dashboard Keuangan HOCINDO", layout="wide")

# Harga saham per lembar
HARGA_SAHAM = 100

# URL GitHub Raw untuk data (ganti dengan repo Anda)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/hocindo/hocindo.github.io/main/financial_dashboard/transaksi.json"

@st.cache_data
def load_data_from_github():
    """Load data transaksi dari GitHub Raw."""
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            st.warning("Gagal load data dari GitHub. Menggunakan data default.")
            return get_default_data()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return get_default_data()

def get_default_data():
    """Data default jika GitHub gagal."""
    return pd.DataFrame([
        {"tanggal": "2025-09-08", "nama": "Mochamad Tabrani", "rekening": "Blu BCA 0022 2858 8888", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 50000},
        {"tanggal": "2025-09-08", "nama": "Pipit Puspita", "rekening": "BCA 1234 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 100000},
        {"tanggal": "2025-09-10", "nama": "Sangaji", "rekening": "BRI 5678 **** ****", "jenis": "Investasi", "nominal": 100000, "saham": 1000, "saldo": 200000},
        {"tanggal": "2025-09-10", "nama": "Asmini", "rekening": "Mandiri 5678 **** ****", "jenis": "Investasi", "nominal": 135000, "saham": 1350, "saldo": 335000},
        {"tanggal": "2025-09-10", "nama": "Rasyid", "rekening": "BNI 5678 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 385000},
    ])

def calculate_summary(df):
    """Hitung summary."""
    if df.empty:
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}
    return {
        "total_investasi": df["nominal"].sum(),
        "total_saham": df["saham"].sum(),
        "jumlah_investor": len(df),
        "dana_kelolaan": df["nominal"].sum()
    }

def add_transaction(df, new_data):
    """Tambah transaksi baru."""
    nominal = int(new_data["nominal"])
    saham = nominal // HARGA_SAHAM
    saldo_terakhir = df["saldo"].iloc[-1] if not df.empty else 0
    saldo_baru = saldo_terakhir + nominal
    new_row = pd.DataFrame([{
        "tanggal": new_data["tanggal"],
        "nama": new_data["nama"],
        "rekening": new_data["rekening"],
        "jenis": "Investasi",
        "nominal": nominal,
        "saham": saham,
        "saldo": saldo_baru
    }])
    return pd.concat([df, new_row], ignore_index=True)

# Main App
st.title("📊 Catatan Keuangan Investor HOCINDO - September 2025")
st.markdown("Harga per Lembar Saham: **Rp 100**")

# Load data
df = load_data_from_github()
summary = calculate_summary(df)

# Kolom 1: Summary dan Form
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Summary")
    st.metric("Total Investasi", f"Rp {summary['total_investasi']:,.0f}")
    st.metric("Total Lembar Saham", f"{summary['total_saham']:,.0f}")
    st.metric("Jumlah Investor", summary['jumlah_investor'])
    st.metric("Dana Kelolaan", f"Rp {summary['dana_kelolaan']:,.0f}")

    # Kalkulator ROI
    st.subheader("💰 Kalkulator ROI")
    roi_percent = st.number_input("ROI per bulan (%)", min_value=0.0, step=0.1)
    if roi_percent > 0:
        keuntungan = (summary['total_investasi'] * roi_percent) / 100
        st.success(f"Estimasi Keuntungan: **Rp {keuntungan:,.0f}**")

with col2:
    # Form Tambah Transaksi
    st.subheader("➕ Tambah Transaksi")
    with st.form("add_transaction"):
        tanggal = st.date_input("Tanggal", value=datetime.now())
        nama = st.text_input("Nama Investor")
        rekening = st.text_input("No. Rekening")
        nominal = st.number_input("Nominal (Rp)", min_value=100, step=100)
        submitted = st.form_submit_button("Tambah")
        if submitted:
            if nama and rekening:
                new_data = {"tanggal": tanggal.strftime("%Y-%m-%d"), "nama": nama, "rekening": rekening, "nominal": nominal}
                df = add_transaction(df, new_data)
                st.success("Transaksi ditambahkan!")
                st.rerun()  # Refresh app
            else:
                st.error("Isi semua kolom!")

# Tabel Transaksi
st.subheader("📋 Daftar Transaksi")
st.dataframe(df, use_container_width=True)

# Chart
st.subheader("📊 Visualisasi")
chart_type = st.selectbox("Pilih Jenis Chart", ["Pie Investasi", "Pie Saham", "Bar per Tanggal", "Line Saldo"])

if chart_type == "Pie Investasi":
    fig = px.pie(df, values="nominal", names="nama", title="Proporsi Investasi per Investor")
elif chart_type == "Pie Saham":
    fig = px.pie(df, values="saham", names="nama", title="Proporsi Lembar Saham per Investor")
elif chart_type == "Bar per Tanggal":
    daily_sum = df.groupby("tanggal")["nominal"].sum().reset_index()
    fig = px.bar(daily_sum, x="tanggal", y="nominal", title="Investasi per Tanggal")
else:  # Line Saldo
    fig = px.line(df, x="tanggal", y="saldo", title="Tren Saldo Kumulatif")

st.plotly_chart(fig, use_container_width=True)

# Export
col_export1, col_export2 = st.columns(2)
with col_export1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export ke CSV", csv, "hocindo-transaksi.csv", "text/csv")
with col_export2:
    if st.button("🔄 Refresh dari GitHub"):
        st.cache_data.clear()
        st.rerun()

# Catatan
st.subheader("📝 Catatan")
st.info("""
- Transaksi awal untuk UMKM dan saham hotel.
- Data disimpan lokal; untuk update ke GitHub, gunakan Git CLI.
- Harga saham: Rp 100/lembar.
""")
