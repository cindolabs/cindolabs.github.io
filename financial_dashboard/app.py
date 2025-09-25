import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
import io
import os

# Konfigurasi Streamlit
st.set_page_config(page_title="Dashboard Keuangan HOCINDO", layout="wide", initial_sidebar_state="expanded")

# Harga saham per lembar
HARGA_SAHAM = 100
GITHUB_RAW_URL = "https://raw.githubusercontent.com/hocindo/hocindo.github.io/main/financial_dashboard/transaksi.json"
GITHUB_API_URL = "https://api.github.com/repos/hocindo/hocindo.github.io/contents/financial_dashboard/transaksi.json"

# Autentikasi sederhana
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            # Ganti dengan autentikasi Anda (misalnya, cek database)
            if username == "admin" and password == "hocindo2025":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.sidebar.error("Username atau password salah!")
        return False
    return True

# Load data dari GitHub
@st.cache_data
def load_data_from_github(_timestamp):
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        st.warning("Gagal load data dari GitHub. Menggunakan data default.")
        return get_default_data()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return get_default_data()

def get_default_data():
    return pd.DataFrame([
        {"tanggal": "2025-09-08", "nama": "Mochamad Tabrani", "rekening": "Blu BCA 0022 2858 8888", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 50000},
        {"tanggal": "2025-09-08", "nama": "Pipit Puspita", "rekening": "BCA 1234 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 100000},
        {"tanggal": "2025-09-10", "nama": "Sangaji", "rekening": "BRI 5678 **** ****", "jenis": "Investasi", "nominal": 100000, "saham": 1000, "saldo": 200000},
        {"tanggal": "2025-09-10", "nama": "Asmini", "rekening": "Mandiri 5678 **** ****", "jenis": "Investasi", "nominal": 135000, "saham": 1350, "saldo": 335000},
        {"tanggal": "2025-09-10", "nama": "Rasyid", "rekening": "BNI 5678 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 385000},
    ])

# Update data ke GitHub
def save_to_github(df):
    try:
        token = st.secrets.get("GITHUB_TOKEN", None)
        if not token:
            st.error("GitHub token tidak ditemukan di secrets.toml!")
            return False
        content = base64.b64encode(json.dumps(df.to_dict('records'), indent=4).encode()).decode()
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        
        # Get SHA file saat ini
        response = requests.get(GITHUB_API_URL, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        # Update file
        payload = {
            "message": f"Update transaksi.json pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": content,
            "sha": sha
        }
        response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            st.success("Data berhasil diupdate ke GitHub!")
            return True
        else:
            st.error(f"Gagal update GitHub: {response.json().get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error updating GitHub: {e}")
        return False

# Hitung summary
def calculate_summary(df):
    if df.empty:
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}
    return {
        "total_investasi": df["nominal"].sum(),
        "total_saham": df["saham"].sum(),
        "jumlah_investor": len(df["nama"].unique()),
        "dana_kelolaan": df["nominal"].sum()
    }

# Tambah transaksi
def add_transaction(df, new_data):
    nominal = int(new_data["nominal"])
    if nominal % HARGA_SAHAM != 0:
        st.error("Nominal harus kelipatan Rp 100!")
        return df
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

# Hapus transaksi
def delete_transaction(df, index):
    df = df.drop(index).reset_index(drop=True)
    # Recalculate saldo
    saldo = 0
    for i in range(len(df)):
        saldo += df.iloc[i]["nominal"]
        df.at[i, "saldo"] = saldo
    return df

# Export ke PDF
def export_to_pdf(df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "Laporan Keuangan HOCINDO - September 2025")
    y = 700
    for _, row in df.iterrows():
        text = f"{row['tanggal']} | {row['nama']} | {row['rekening']} | {row['nominal']:,.0f} | {row['saham']:,.0f} | {row['saldo']:,.0f}"
        c.drawString(30, y, text)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    buffer.seek(0)
    return buffer

# Main App
if check_login():
    # Sidebar
    st.sidebar.header("Navigasi")
    action = st.sidebar.radio("Pilih Aksi", ["Dashboard", "Tambah Transaksi", "Kalkulator ROI"])

    # Load data
    df = load_data_from_github(datetime.now().timestamp())
    summary = calculate_summary(df)

    if action == "Dashboard":
        st.title("📊 Dashboard Keuangan HOCINDO")
        st.markdown(f"Harga per Lembar Saham: **Rp {HARGA_SAHAM}**")

        # Summary
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Investasi", f"Rp {summary['total_investasi']:,.0f}")
        col2.metric("Total Lembar Saham", f"{summary['total_saham']:,.0f}")
        col3.metric("Jumlah Investor", summary['jumlah_investor'])
        col4.metric("Dana Kelolaan", f"Rp {summary['dana_kelolaan']:,.0f}")

        # Tabel Interaktif
        st.subheader("📋 Daftar Transaksi")
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True)
        gb.configure_selection("single")
        grid_response = AgGrid(df, gridOptions=gb.build(), update_mode=GridUpdateMode.MODEL_CHANGED)
        df = grid_response["data"]

        # Tombol Hapus
        if grid_response["selected_rows"]:
            if st.button("🗑️ Hapus Transaksi Terpilih"):
                selected_index = grid_response["selected_rows"][0]["_selectedRowNodeId"]
                df = delete_transaction(df, selected_index)
                if save_to_github(df):
                    st.cache_data.clear()
                    st.rerun()

        # Chart
        st.subheader("📊 Visualisasi")
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{"type": "pie"}, {"type": "bar"}, {"type": "xy"}]],
            subplot_titles=("Proporsi Saham", "Investasi per Tanggal", "Tren Saldo")
        )
        # Pie Saham
        fig.add_trace(
            go.Pie(labels=df["nama"], values=df["saham"], name="Saham"),
            row=1, col=1
        )
        # Bar per Tanggal
        daily_sum = df.groupby("tanggal")["nominal"].sum().reset_index()
        fig.add_trace(
            go.Bar(x=daily_sum["tanggal"], y=daily_sum["nominal"], name="Nominal"),
            row=1, col=2
        )
        # Line Saldo
        fig.add_trace(
            go.Scatter(x=df["tanggal"], y=df["saldo"], mode="lines", name="Saldo"),
            row=1, col=3
        )
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        # Export
        col_export1, col_export2, col_export3 = st.columns(3)
        with col_export1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", csv, "hocindo-transaksi.csv", "text/csv")
        with col_export2:
            pdf_buffer = export_to_pdf(df)
            st.download_button("📄 Export PDF", pdf_buffer, "hocindo-laporan.pdf", "application/pdf")
        with col_export3:
            if st.button("🔄 Refresh dari GitHub"):
                st.cache_data.clear()
                st.rerun()

    elif action == "Tambah Transaksi":
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
                    if save_to_github(df):
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.error("Isi semua kolom!")

    elif action == "Kalkulator ROI":
        st.subheader("💰 Kalkulator ROI")
        roi_percent = st.number_input("ROI per bulan (%)", min_value=0.0, step=0.1)
        if roi_percent > 0:
            keuntungan = (summary['total_investasi'] * roi_percent) / 100
            st.success(f"Estimasi Keuntungan: **Rp {keuntungan:,.0f}**")

    # Catatan
    st.subheader("📝 Catatan")
    st.info("""
    - Transaksi awal untuk UMKM dan saham hotel.
    - Data disimpan di GitHub via API.
    - Harga saham: Rp 100/lembar.
    """)
else:
    st.warning("Silakan login di sidebar untuk mengakses dashboard.")
