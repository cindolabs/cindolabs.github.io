import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.express as px
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try importing reportlab, fallback if not available
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    st.warning("Library 'reportlab' tidak terinstall. Fitur export PDF tidak tersedia. Install dengan: pip install reportlab")

# Try importing streamlit-aggrid
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False
    st.warning("Library 'streamlit-aggrid' tidak terinstall. Menggunakan tabel standar. Install dengan: pip install streamlit-aggrid")

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
        logger.info(f"Fetching data from {GITHUB_RAW_URL}")
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            required_columns = ["tanggal", "nama", "rekening", "jenis", "nominal", "saham", "saldo"]
            if all(col in df.columns for col in required_columns):
                return df
            else:
                logger.error("Invalid transaksi.json format: Missing required columns")
                st.error("Format transaksi.json tidak valid: kolom hilang.")
                return get_default_data()
        else:
            logger.warning(f"Failed to fetch data from GitHub: Status {response.status_code}")
            st.warning(f"Gagal load data dari GitHub (status: {response.status_code}). Menggunakan data default.")
            return get_default_data()
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        st.error(f"Error fetching data: {e}")
        return get_default_data()

def get_default_data():
    logger.info("Using default data")
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
            logger.warning("GitHub token not found. Saving locally.")
            st.error("GitHub token tidak ditemukan di secrets.toml! Data disimpan lokal.")
            df.to_json("transaksi.json", orient="records", indent=4)
            return False
        content = base64.b64encode(json.dumps(df.to_dict('records'), indent=4).encode()).decode()
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        
        logger.info(f"Fetching SHA from {GITHUB_API_URL}")
        response = requests.get(GITHUB_API_URL, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        payload = {
            "message": f"Update transaksi.json pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": content,
            "sha": sha
        }
        logger.info("Updating transaksi.json on GitHub")
        response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            logger.info("Successfully updated transaksi.json on GitHub")
            st.success("Data berhasil diupdate ke GitHub!")
            return True
        else:
            logger.error(f"Failed to update GitHub: {response.json().get('message', 'Unknown error')}")
            st.error(f"Gagal update GitHub: {response.json().get('message', 'Unknown error')}")
            df.to_json("transaksi.json", orient="records", indent=4)
            return False
    except Exception as e:
        logger.error(f"Error updating GitHub: {str(e)}")
        st.error(f"Error updating GitHub: {e}")
        df.to_json("transaksi.json", orient="records", indent=4)
        return False

# Hitung summary
def calculate_summary(df):
    try:
        if df.empty:
            logger.warning("DataFrame is empty")
            return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}
        return {
            "total_investasi": df["nominal"].sum(),
            "total_saham": df["saham"].sum(),
            "jumlah_investor": len(df["nama"].unique()),
            "dana_kelolaan": df["nominal"].sum()
        }
    except Exception as e:
        logger.error(f"Error calculating summary: {str(e)}")
        st.error(f"Error calculating summary: {e}")
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}

# Tambah transaksi
def add_transaction(df, new_data):
    try:
        nominal = int(new_data["nominal"])
        if nominal % HARGA_SAHAM != 0:
            logger.error("Nominal is not a multiple of 100")
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
        logger.info(f"Adding new transaction: {new_data}")
        return pd.concat([df, new_row], ignore_index=True)
    except Exception as e:
        logger.error(f"Error adding transaction: {str(e)}")
        st.error(f"Error adding transaction: {e}")
        return df

# Hapus transaksi
def delete_transaction(df, index):
    try:
        logger.info(f"Deleting transaction at index {index}")
        df = df.drop(index).reset_index(drop=True)
        saldo = 0
        for i in range(len(df)):
            saldo += df.iloc[i]["nominal"]
            df.at[i, "saldo"] = saldo
        return df
    except Exception as e:
        logger.error(f"Error deleting transaction: {str(e)}")
        st.error(f"Error deleting transaction: {e}")
        return df

# Export ke PDF
def export_to_pdf(df):
    if not REPORTLAB_AVAILABLE:
        st.error("Cannot generate PDF: reportlab not installed.")
        return None
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(30, 750, "Laporan Keuangan HOCINDO - September 2025")
        y = 700
        for _, row in df.iterrows():
            text = f"{row['tanggal']} | {row['nama']} | {row['rekening']} | Rp {row['nominal']:,.0f} | {row['saham']:,.0f} | Rp {row['saldo']:,.0f}"
            c.drawString(30, y, text)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        buffer.seek(0)
        logger.info("PDF generated successfully")
        return buffer
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        st.error(f"Error generating PDF: {e}")
        return None

# Main App
if check_login():
    st.title("📊 Dashboard Keuangan HOCINDO - September 2025")
    st.markdown(f"Harga per Lembar Saham: **Rp {HARGA_SAHAM}**")

    # Sidebar
    st.sidebar.header("Navigasi")
    action = st.sidebar.radio("Pilih Aksi", ["Dashboard", "Tambah Transaksi", "Kalkulator ROI"])

    # Load data
    df = load_data_from_github(datetime.now().timestamp())
    summary = calculate_summary(df)

    if action == "Dashboard":
        # Summary
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Investasi", f"Rp {summary['total_investasi']:,.0f}")
        col2.metric("Total Lembar Saham", f"{summary['total_saham']:,.0f}")
        col3.metric("Jumlah Investor", summary['jumlah_investor'])
        col4.metric("Dana Kelolaan", f"Rp {summary['dana_kelolaan']:,.0f}")

        # Tabel Interaktif
        st.subheader("📋 Daftar Transaksi")
        if AGGRID_AVAILABLE:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=True)
            gb.configure_selection("single")
            grid_response = AgGrid(df, gridOptions=gb.build(), update_mode=GridUpdateMode.MODEL_CHANGED, height=300)
            df = grid_response["data"]
            if grid_response["selected_rows"]:
                if st.button("🗑️ Hapus Transaksi Terpilih"):
                    selected_index = grid_response["selected_rows"][0]["_selectedRowNodeId"]
                    df = delete_transaction(df, selected_index)
                    if save_to_github(df):
                        st.cache_data.clear()
                        st.rerun()
        else:
            st.dataframe(df, use_container_width=True)

        # Chart
        st.subheader("📊 Visualisasi")
        chart_type = st.selectbox("Pilih Jenis Chart", ["Pie Investasi", "Pie Saham", "Bar per Tanggal", "Line Saldo"])
        try:
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
        except Exception as e:
            logger.error(f"Error rendering chart: {str(e)}")
            st.error(f"
