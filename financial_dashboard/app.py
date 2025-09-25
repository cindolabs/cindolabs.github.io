import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.express as px
import os
from io import BytesIO
import base64
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    st.warning("Library 'reportlab' tidak terinstall. Fitur export PDF tidak tersedia. Install dengan: pip install reportlab")

# Cek apakah streamlit-aggrid terinstall
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False
    st.warning("streamlit-aggrid tidak terinstall. Menggunakan tabel standar. Install dengan: pip install streamlit-aggrid")

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
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            required_columns = ["tanggal", "nama", "rekening", "jenis", "nominal", "saham", "saldo"]
            if all(col in df.columns for col in required_columns):
                return df
            else:
                st.error("Format transaksi.json tidak valid: kolom hilang.")
                return get_default_data()
        else:
            st.warning(f"Gagal load data dari GitHub (status: {response.status_code}). Menggunakan data default.")
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
            st.error("GitHub token tidak ditemukan di secrets.toml! Data disimpan lokal.")
            df.to_json("transaksi.json", orient="records", indent=4)
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
        df.to_json("transaksi.json", orient="records", indent=4)
        return False

# Hitung summary
def calculate_summary(df):
    try:
        if df.empty:
            return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}
        return {
            "total_investasi": df["nominal"].sum(),
            "total_saham": df["saham"].sum(),
            "jumlah_investor": len(df["nama"].unique()),
            "dana_kelolaan": df["nominal"].sum()
        }
    except Exception as e:
        st.error(f"Error calculating summary: {e}")
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": 0}

# Hitung perkiraan pendapatan per investor
def calculate_investor_earnings(df, roi_percent):
    try:
        if df.empty or roi_percent <= 0:
            return pd.DataFrame(columns=["nama", "total_investasi", "total_saham", "estimasi_pendapatan"])
        investor_summary = df.groupby("nama").agg({
            "nominal": "sum",
            "saham": "sum"
        }).reset_index()
        investor_summary["estimasi_pendapatan"] = investor_summary["nominal"] * (roi_percent / 100)
        return investor_summary[["nama", "total_investasi", "total_saham", "estimasi_pendapatan"]]
    except Exception as e:
        st.error(f"Error calculating investor earnings: {e}")
        return pd.DataFrame(columns=["nama", "total_investasi", "total_saham", "estimasi_pendapatan"])

# Tambah transaksi
def add_transaction(df, new_data):
    try:
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
    except Exception as e:
        st.error(f"Error adding transaction: {e}")
        return df

# Hapus transaksi
def delete_transaction(df, index):
    try:
        df = df.drop(index).reset_index(drop=True)
        saldo = 0
        for i in range(len(df)):
            saldo += df.iloc[i]["nominal"]
            df.at[i, "saldo"] = saldo
        return df
    except Exception as e:
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
        return buffer
    except Exception as e:
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
            st.error(f"Error rendering chart: {e}")

        # Export
        col_export1, col_export2, col_export3 = st.columns(3)
        with col_export1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", csv, "hocindo-transaksi.csv", "text/csv")
        with col_export2:
            if REPORTLAB_AVAILABLE:
                pdf_buffer = export_to_pdf(df)
                if pdf_buffer:
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
            try:
                keuntungan = (summary['total_investasi'] * roi_percent) / 100
                st.success(f"Estimasi Keuntungan Total: **Rp {keuntungan:,.0f}**")
                
                # Perkiraan Pendapatan Investor
                st.subheader("📈 Perkiraan Pendapatan per Investor")
                investor_earnings = calculate_investor_earnings(df, roi_percent)
                if not investor_earnings.empty:
                    # Format columns for display
                    investor_earnings_display = investor_earnings.copy()
                    investor_earnings_display["total_investasi"] = investor_earnings_display["total_investasi"].apply(lambda x: f"Rp {x:,.0f}")
                    investor_earnings_display["total_saham"] = investor_earnings_display["total_saham"].apply(lambda x: f"{x:,.0f}")
                    investor_earnings_display["estimasi_pendapatan"] = investor_earnings_display["estimasi_pendapatan"].apply(lambda x: f"Rp {x:,.0f}")
                    st.dataframe(investor_earnings_display, use_container_width=True)
                    
                    # Bar chart for earnings
                    fig_earnings = px.bar(
                        investor_earnings,
                        x="nama",
                        y="estimasi_pendapatan",
                        title="Perkiraan Pendapatan per Investor",
                        labels={"estimasi_pendapatan": "Estimasi Pendapatan (Rp)", "nama": "Nama Investor"}
                    )
                    st.plotly_chart(fig_earnings, use_container_width=True)
                else:
                    st.warning("Tidak ada data investor untuk menghitung pendapatan.")
            except Exception as e:
                st.error(f"Error calculating ROI: {e}")

    # Catatan
    st.subheader("📝 Catatan")
    st.info("""
    - Transaksi awal untuk UMKM dan saham hotel.
    - Data disimpan di GitHub via API (atau lokal jika token tidak tersedia).
    - Harga saham: Rp 100/lembar.
    - Login: Username 'admin', Password 'hocindo2025'.
    """)
else:
    st.warning("Silakan login di sidebar untuk mengakses dashboard.")
