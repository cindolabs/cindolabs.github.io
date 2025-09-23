import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("Dashboard Keuangan Pribadi - Hocindo")

st.sidebar.header("Input Transaksi")
with st.sidebar.form("form_transaksi"):
    tanggal = st.date_input("Tanggal")
    kategori = st.selectbox("Kategori", ["Pendapatan", "Pengeluaran"])
    deskripsi = st.text_input("Deskripsi")
    jumlah = st.number_input("Jumlah (IDR)", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Tambah Transaksi")

if 'transaksi' not in st.session_state:
    st.session_state.transaksi = pd.DataFrame(columns=["Tanggal", "Kategori", "Deskripsi", "Jumlah"])

if submit:
    new_transaksi = pd.DataFrame({
        "Tanggal": [tanggal],
        "Kategori": [kategori],
        "Deskripsi": [deskripsi],
        "Jumlah": [jumlah if kategori == "Pendapatan" else -jumlah]
    })
    st.session_state.transaksi = pd.concat([st.session_state.transaksi, new_transaksi], ignore_index=True)

st.header("Daftar Transaksi")
st.dataframe(st.session_state.transaksi)

total_pendapatan = st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Pendapatan"]["Jumlah"].sum()
total_pengeluaran = abs(st.session_state.transaksi[st.session_state.transaksi["Kategori"] == "Pengeluaran"]["Jumlah"].sum())
saldo = total_pendapatan - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", f"Rp {total_pendapatan:,.2f}")
col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.2f}")
col3.metric("Saldo", f"Rp {saldo:,.2f}")

st.header("Distribusi Keuangan")
if not st.session_state.transaksi.empty:
    pie_data = st.session_state.transaksi.groupby("Kategori")["Jumlah"].sum().abs().reset_index()
    fig_pie = px.pie(pie_data, values="Jumlah", names="Kategori", title="Pendapatan vs Pengeluaran")
    st.plotly_chart(fig_pie)

st.header("Tren Saldo")
if not st.session_state.transaksi.empty:
    st.session_state.transaksi["Tanggal"] = pd.to_datetime(st.session_state.transaksi["Tanggal"])
    tren_data = st.session_state.transaksi.sort_values("Tanggal")
    tren_data["Saldo Kumulatif"] = tren_data["Jumlah"].cumsum()
    fig_tren = px.line(tren_data, x="Tanggal", y="Saldo Kumulatif", title="Tren Saldo Harian")
    st.plotly_chart(fig_tren)

st.write("Catatan: Masukkan transaksi melalui sidebar untuk memperbarui dashboard.")
