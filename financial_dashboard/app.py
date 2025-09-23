# ---------------------- METRICS STYLING ----------------------
st.markdown("""
    <style>
    .metric-card {
        background: rgba(0, 128, 0, 0.15); /* hijau transparan */
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #006400; /* hijau tua */
    }
    .metric-value {
        font-size: 20px;
        color: #004d00; /* hijau gelap */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("### 📌 Ringkasan Keuangan")

# Baris 1 (4 kolom)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>💰 Pemasukan</div><div class='metric-value'>Rp {total_pemasukan:,.0f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📉 Pengeluaran</div><div class='metric-value'>Rp {total_pengeluaran:,.0f}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🧑‍💼 Dana Manajer</div><div class='metric-value'>Rp {dana_manajer:,.0f}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📊 Saldo</div><div class='metric-value'>Rp {saldo:,.0f}</div></div>", unsafe_allow_html=True)

# Baris 2 (3 kolom)
col5, col6, col7 = st.columns(3)
with col5:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🏦 Dana Cadangan</div><div class='metric-value'>Rp {dana_cadangan:,.0f}</div></div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>📈 Pertumbuhan</div><div class='metric-value'>Rp {pertumbuhan:,.0f}</div></div>", unsafe_allow_html=True)
with col7:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>🤝 Bagi Hasil</div><div class='metric-value'>Rp {bagi_hasil:,.0f}</div></div>", unsafe_allow_html=True)
