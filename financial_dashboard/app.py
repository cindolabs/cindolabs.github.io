import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.express as px
import os
from io import BytesIO
import base64
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for streamlit-aggrid
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False
    st.warning("streamlit-aggrid not installed. Using standard table. Install with: pip install streamlit-aggrid")

# Streamlit configuration
st.set_page_config(
    page_title="HOCINDO Financial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="hocindo.svg"
)

# Constants
HARGA_SAHAM = 100
DANA_KELOLAAN_BARU = 500000
GITHUB_RAW_URL = "https://raw.githubusercontent.com/hocindo/hocindo.github.io/main/financial_dashboard/transaksi.json"
GITHUB_API_URL = "https://api.github.com/repos/hocindo/hocindo.github.io/contents/financial_dashboard/transaksi.json"

# Load data from GitHub with improved error handling
@st.cache_data(ttl=300)
def load_data_from_github(_timestamp):
    try:
        logger.info(f"Fetching data from {GITHUB_RAW_URL}")
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        required_columns = ["tanggal", "nama", "rekening", "jenis", "nominal", "saham", "saldo"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Invalid transaksi.json format: Missing required columns")
        df["tanggal"] = pd.to_datetime(df["tanggal"])
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        st.error(f"Failed to load data from GitHub: {e}. Using default data.")
        return get_default_data()

def get_default_data():
    logger.info("Using default data")
    return pd.DataFrame([
        {"tanggal": "2025-09-08", "nama": "Mochamad Tabrani", "rekening": "Blu BCA 0022 2858 8888", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 50000},
        {"tanggal": "2025-09-08", "nama": "Pipit Puspita", "rekening": "BCA 1234 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 100000},
        {"tanggal": "2025-09-10", "nama": "Sangaji", "rekening": "BRI 5678 **** ****", "jenis": "Investasi", "nominal": 100000, "saham": 1000, "saldo": 200000},
        {"tanggal": "2025-09-10", "nama": "Asmini", "rekening": "Mandiri 5678 **** ****", "jenis": "Investasi", "nominal": 135000, "saham": 1350, "saldo": 335000},
        {"tanggal": "2025-09-10", "nama": "Rasyid", "rekening": "BNI 5678 **** ****", "jenis": "Investasi", "nominal": 50000, "saham": 500, "saldo": 385000},
    ]).assign(tanggal=lambda x: pd.to_datetime(x["tanggal"]))

# Save data to GitHub
def save_to_github(df):
    try:
        token = st.secrets.get("GITHUB_TOKEN", None)
        if not token:
            raise ValueError("GitHub token not found in secrets.toml")
        
        content = base64.b64encode(json.dumps(df.to_dict('records'), indent=4).encode()).decode()
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        
        response = requests.get(GITHUB_API_URL, headers=headers)
        response.raise_for_status()
        sha = response.json().get("sha")
        
        payload = {
            "message": f"Update transaksi.json on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": content,
            "sha": sha
        }
        response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        logger.info("Successfully updated transaksi.json on GitHub")
        st.success("Data successfully updated to GitHub!")
        return True
    except Exception as e:
        logger.error(f"Error updating GitHub: {str(e)}")
        st.error(f"Failed to update GitHub: {e}. Saving locally.")
        df.to_json("transaksi.json", orient="records", indent=4)
        return False

# Calculate summary metrics
def calculate_summary(df):
    if df.empty:
        logger.warning("DataFrame is empty")
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": DANA_KELOLAAN_BARU}
    try:
        return {
            "total_investasi": df["nominal"].sum(),
            "total_saham": df["saham"].sum(),
            "jumlah_investor": len(df["nama"].unique()),
            "dana_kelolaan": DANA_KELOLAAN_BARU
        }
    except Exception as e:
        logger.error(f"Error calculating summary: {str(e)}")
        st.error(f"Error calculating summary: {e}")
        return {"total_investasi": 0, "total_saham": 0, "jumlah_investor": 0, "dana_kelolaan": DANA_KELOLAAN_BARU}

# Calculate fund allocation per investor
def calculate_fund_allocation(df):
    if df.empty:
        logger.warning("DataFrame is empty for fund allocation")
        return pd.DataFrame(columns=["nama", "saham", "proporsi_saham", "bagian_dana"])
    try:
        investor_summary = df.groupby("nama").agg({"saham": "sum"}).reset_index()
        total_saham = investor_summary["saham"].sum()
        if total_saham == 0:
            return pd.DataFrame(columns=["nama", "saham", "proporsi_saham", "bagian_dana"])
        investor_summary["proporsi_saham"] = investor_summary["saham"] / total_saham
        investor_summary["bagian_dana"] = investor_summary["proporsi_saham"] * DANA_KELOLAAN_BARU
        return investor_summary
    except Exception as e:
        logger.error(f"Error calculating fund allocation: {str(e)}")
        st.error(f"Error calculating fund allocation: {e}")
        return pd.DataFrame(columns=["nama", "saham", "proporsi_saham", "bagian_dana"])

# Calculate investor earnings (fixed)
def calculate_investor_earnings(df, roi_percent):
    if df.empty or roi_percent <= 0:
        logger.warning("DataFrame empty or invalid ROI")
        return pd.DataFrame(columns=["nama", "total_investasi", "total_saham", "estimasi_pendapatan"])
    try:
        investor_summary = df.groupby("nama").agg({
            "nominal": "sum",
            "saham": "sum"
        }).reset_index()
        # Rename columns to match expected output
        investor_summary = investor_summary.rename(columns={
            "nominal": "total_investasi",
            "saham": "total_saham"
        })
        investor_summary["estimasi_pendapatan"] = investor_summary["total_investasi"] * (roi_percent / 100)
        return investor_summary[["nama", "total_investasi", "total_saham", "estimasi_pendapatan"]]
    except Exception as e:
        logger.error(f"Error calculating investor earnings: {str(e)}")
        st.error(f"Error calculating investor earnings: {e}")
        return pd.DataFrame(columns=["nama", "total_investasi", "total_saham", "estimasi_pendapatan"])

# Add transaction
def add_transaction(df, new_data):
    try:
        nominal = int(new_data["nominal"])
        if nominal % HARGA_SAHAM != 0:
            raise ValueError("Nominal must be a multiple of Rp 100")
        saham = nominal // HARGA_SAHAM
        saldo_terakhir = df["saldo"].iloc[-1] if not df.empty else 0
        saldo_baru = saldo_terakhir + nominal
        new_row = pd.DataFrame([{
            "tanggal": pd.to_datetime(new_data["tanggal"]),
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

# Delete transaction
def delete_transaction(df, index):
    try:
        logger.info(f"Deleting transaction at index {index}")
        df = df.drop(index).reset_index(drop=True)
        if not df.empty:
            df["saldo"] = df["nominal"].cumsum()
        return df
    except Exception as e:
        logger.error(f"Error deleting transaction: {str(e)}")
        st.error(f"Error deleting transaction: {e}")
        return df

# Main App
st.title("📊 HOCINDO Financial Dashboard - September 2025")
st.markdown(f"**Share Price per Unit: Rp {HARGA_SAHAM}** | **Managed Funds: Rp {DANA_KELOLAAN_BARU:,.0f}**")

# Sidebar
st.sidebar.header("Navigation")
action = st.sidebar.radio("Select Action", ["Dashboard", "Add Transaction", "ROI Calculator"], index=0)

# Load data
df = load_data_from_github(datetime.now().timestamp())
summary = calculate_summary(df)

if action == "Dashboard":
    # Summary Metrics
    st.subheader("📈 Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Investment", f"Rp {summary['total_investasi']:,.0f}")
    col2.metric("Total Shares", f"{summary['total_saham']:,.0f}")
    col3.metric("Number of Investors", summary['jumlah_investor'])
    col4.metric("Managed Funds", f"Rp {summary['dana_kelolaan']:,.0f}")

    # Transaction Table
    st.subheader("📋 Transaction List")
    if AGGRID_AVAILABLE:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, minWidth=100)
        gb.configure_column("tanggal", type=["dateColumn"], dateFormatter="yyyy-mm-dd")
        gb.configure_selection("single")
        grid_response = AgGrid(
            df,
            gridOptions=gb.build(),
            update_mode=GridUpdateMode.MODEL_CHANGED,
            height=400,
            theme="streamlit",
            fit_columns_on_grid_load=True
        )
        df = grid_response["data"]
        if grid_response["selected_rows"]:
            selected_index = grid_response["selected_rows"][0]["_selectedRowNodeId"]
            if st.button("🗑️ Delete Selected Transaction"):
                df = delete_transaction(df, selected_index)
                if save_to_github(df):
                    st.cache_data.clear()
                    st.rerun()
    else:
        df_display = df.copy()
        df_display["tanggal"] = df_display["tanggal"].dt.strftime("%Y-%m-%d")
        df_display["saham"] = df_display["saham"].apply(lambda x: f"{x:,.0f}")
        df_display["saldo"] = df_display["saldo"].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(df_display, use_container_width=True)

    # Fund Allocation
    st.subheader("📊 Fund Allocation per Investor")
    fund_allocation = calculate_fund_allocation(df)
    if not fund_allocation.empty:
        fund_allocation_display = fund_allocation.copy()
        fund_allocation_display["saham"] = fund_allocation_display["saham"].apply(lambda x: f"{x:,.0f}")
        fund_allocation_display["proporsi_saham"] = fund_allocation_display["proporsi_saham"].apply(lambda x: f"{x:.2%}")
        fund_allocation_display["bagian_dana"] = fund_allocation_display["bagian_dana"].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(fund_allocation_display, use_container_width=True)
        
        fig_allocation = px.bar(
            fund_allocation,
            x="nama",
            y="bagian_dana",
            title="Fund Allocation per Investor",
            labels={"bagian_dana": "Allocated Funds (Rp)", "nama": "Investor Name"},
            color="nama",
            template="plotly_white"
        )
        st.plotly_chart(fig_allocation, use_container_width=True)
    else:
        st.warning("No investor data available for fund allocation.")

    # Visualization
    st.subheader("📊 Investment Visualization")
    chart_type = st.selectbox("Select Chart Type", ["Pie Investment", "Pie Shares", "Bar by Date", "Line Balance"], key="chart_type")
    try:
        if chart_type == "Pie Investment":
            fig = px.pie(df, values="nominal", names="nama", title="Investment Proportion per Investor", template="plotly_white")
        elif chart_type == "Pie Shares":
            fig = px.pie(df, values="saham", names="nama", title="Share Proportion per Investor", template="plotly_white")
        elif chart_type == "Bar by Date":
            daily_sum = df.groupby("tanggal")["nominal"].sum().reset_index()
            fig = px.bar(daily_sum, x="tanggal", y="nominal", title="Investment by Date", template="plotly_white")
        else:
            fig = px.line(df, x="tanggal", y="saldo", title="Cumulative Balance Trend", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f"Error rendering chart: {str(e)}")
        st.error(f"Error rendering chart: {e}")

    # Export and Refresh
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export as CSV", csv, "hocindo-transaksi.csv", "text/csv")
    with col_export2:
        if st.button("🔄 Refresh Data from GitHub"):
            st.cache_data.clear()
            st.rerun()

elif action == "Add Transaction":
    st.subheader("➕ Add New Transaction")
    with st.form("add_transaction_form"):
        tanggal = st.date_input("Date", value=datetime.now(), key="add_tanggal")
        nama = st.text_input("Investor Name", key="add_nama")
        rekening = st.text_input("Account Number", key="add_rekening")
        nominal = st.number_input("Amount (Rp)", min_value=100, step=100, key="add_nominal")
        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if nama.strip() and rekening.strip():
                new_data = {"tanggal": tanggal.strftime("%Y-%m-%d"), "nama": nama.strip(), "rekening": rekening.strip(), "nominal": nominal}
                df = add_transaction(df, new_data)
                if save_to_github(df):
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.error("Please fill in all fields!")

elif action == "ROI Calculator":
    st.subheader("💰 ROI Calculator")
    roi_percent = st.number_input("Monthly ROI (%)", min_value=0.0, max_value=100.0, step=0.1, key="roi_percent")
    if roi_percent > 0:
        try:
            keuntungan = (summary['total_investasi'] * roi_percent) / 100
            st.success(f"Estimated Total Profit: **Rp {keuntungan:,.0f}**")
            
            st.subheader("📈 Estimated Earnings per Investor")
            investor_earnings = calculate_investor_earnings(df, roi_percent)
            if not investor_earnings.empty:
                investor_earnings_display = investor_earnings.copy()
                investor_earnings_display["total_investasi"] = investor_earnings_display["total_investasi"].apply(lambda x: f"Rp {x:,.0f}")
                investor_earnings_display["total_saham"] = investor_earnings_display["total_saham"].apply(lambda x: f"{x:,.0f}")
                investor_earnings_display["estimasi_pendapatan"] = investor_earnings_display["estimasi_pendapatan"].apply(lambda x: f"Rp {x:,.0f}")
                st.dataframe(investor_earnings_display, use_container_width=True)
                
                fig_earnings = px.bar(
                    investor_earnings,
                    x="nama",
                    y="estimasi_pendapatan",
                    title="Estimated Earnings per Investor",
                    labels={"estimasi_pendapatan": "Estimated Earnings (Rp)", "nama": "Investor Name"},
                    color="nama",
                    template="plotly_white"
                )
                st.plotly_chart(fig_earnings, use_container_width=True)
            else:
                st.warning("No investor data available for earnings calculation.")
        except Exception as e:
            logger.error(f"Error calculating ROI: {str(e)}")
            st.error(f"Error calculating ROI: {e}")

# Footer Notes
st.subheader("📝 Notes")
st.info("""
- Initial transactions for MSMEs and hotel shares.
- Current managed funds: Rp 500,000, distributed based on share proportion.
- Data is stored on GitHub via API (or locally if token is unavailable).
- Share price: Rp 100 per share.
- With HOCINDO's new constitution prioritizing privacy, investor data is kept confidential.
- Pyramid scheme simulation is available on a separate page for educational purposes about illegal schemes.
""")
