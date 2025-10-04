import streamlit as st
import pandas as pd
import plotly.express as px

# Judul halaman (otomatis tampil di multi-page)
st.title("Simulasi Skema Piramida (Hanya untuk Edukasi)")

st.markdown("""
**Peringatan**: Ini adalah simulasi edukatif untuk memahami bahaya skema piramida. 
Skema piramida adalah **ilegal** di Indonesia berdasarkan UU No. 7 Tahun 2014 tentang Perdagangan. 
Jangan gunakan untuk praktik nyata!
""")

# Parameter simulasi
biaya_masuk = 1_000_000  # Rp 1 juta per orang
faktor_rekrut = 2  # Setiap anggota rekrut 2 orang
bonus_persen = 0.5  # 50% dari biaya masuk downline
level_max = st.slider("Pilih Jumlah Level (Maksimum)", min_value=1, max_value=15, value=10)

# Fungsi simulasi piramida
@st.cache_data  # Cache untuk performa lebih baik
def simulasi_piramida(level_max):
    data = []
    total_anggota = 0
    total_uang = 0
    keuntungan_pendiri = 0
    
    for level in range(1, level_max + 1):
        anggota_level = faktor_rekrut ** (level - 1)
        uang_level = anggota_level * biaya_masuk
        total_anggota += anggota_level
        total_uang += uang_level
        keuntungan_level = uang_level * bonus_persen
        keuntungan_pendiri += keuntungan_level
        data.append({
            'Level': level,
            'Jumlah Anggota': anggota_level,
            'Uang Masuk Level (Rp)': f"{uang_level:,.0f}",
            'Keuntungan Pendiri Kumulatif (Rp)': f"{keuntungan_pendiri:,.0f}",
            'Total Anggota': total_anggota,
            'Total Uang Masuk (Rp)': f"{total_uang:,.0f}"
        })
    
    return pd.DataFrame(data)

# Jalankan simulasi
df = simulasi_piramida(level_max)

# Tampilkan tabel
st.subheader("Tabel Simulasi Piramida")
st.dataframe(df, use_container_width=True)

# Peringatan
st.warning(f"Pada level {level_max}, total anggota: {df['Total Anggota'].iloc[-1]:,.0f}. "
           "Realitas: Skema ini runtuh karena tidak ada cukup orang untuk direkrut!")

# Visualisasi grafik
st.subheader("Grafik Pertumbuhan")
fig = px.line(df, x='Level', y=['Jumlah Anggota', 'Total Uang Masuk (Rp)'],
              title="Pertumbuhan Jumlah Anggota dan Total Uang Masuk",
              labels={'value': 'Skala', 'variable': 'Metrik'},
              log_y=True)  # Skala logaritmik untuk menangani nilai besar
fig.update_layout(yaxis_title="Skala (Logaritmik)", xaxis_title="Level")
st.plotly_chart(fig, use_container_width=True)
