import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime  # Impor datetime untuk memperbaiki error
import logging

# Setup logging untuk debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Simulasi Piramida Edukatif",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul dan peringatan
st.title("📈 Simulasi Skema Piramida (Hanya untuk Edukasi)")
st.markdown("""
**Peringatan**: Ini adalah simulasi edukatif untuk memahami bahaya skema piramida. 
Skema piramida **ilegal** di Indonesia berdasarkan UU No. 7 Tahun 2014 tentang Perdagangan. 
**Jangan digunakan untuk praktik nyata!**
""")

# Parameter simulasi di sidebar
st.sidebar.header("Parameter Simulasi")
biaya_masuk = st.sidebar.number_input(
    "Biaya Masuk per Orang (Rp)",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000,
    key="biaya_masuk"
)
faktor_rekrut = st.sidebar.slider(
    "Faktor Rekrutmen (Orang per Anggota)",
    min_value=1,
    max_value=5,
    value=2,
    key="faktor_rekrut"
)
bonus_persen = st.sidebar.slider(
    "Persentase Bonus dari Downline (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=5.0,
    key="bonus_persen"
) / 100
level_max = st.sidebar.slider(
    "Jumlah Level Maksimum",
    min_value=1,
    max_value=15,
    value=10,
    key="level_max"
)

# Fungsi simulasi piramida
@st.cache_data(ttl=300)
def simulasi_piramida(level_max, biaya_masuk, faktor_rekrut, bonus_persen, _cache_buster):
    try:
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
                'Uang Masuk Level Numerik': uang_level,
                'Keuntungan Pendiri Kumulatif (Rp)': f"{keuntungan_pendiri:,.0f}",
                'Keuntungan Pendiri Numerik': keuntungan_pendiri,
                'Total Anggota': total_anggota,
                'Total Uang Masuk (Rp)': f"{total_uang:,.0f}",
                'Total Uang Masuk Numerik': total_uang
            })

        df = pd.DataFrame(data)
        logger.info(f"Simulasi selesai untuk {level_max} level")
        return df
    except Exception as e:
        logger.error(f"Error dalam simulasi: {str(e)}")
        st.error(f"Error menjalankan simulasi: {e}")
        return pd.DataFrame()

# Tombol untuk membersihkan cache
if st.button("🔄 Bersihkan Cache dan Refresh"):
    st.cache_data.clear()
    st.rerun()

# Jalankan simulasi
cache_buster = str(datetime.now().timestamp())
df = simulasi_piramida(level_max, biaya_masuk, faktor_rekrut, bonus_persen, cache_buster)

# Tampilkan tabel
st.subheader("Hasil Simulasi Piramida")
if not df.empty:
    df_display = df[['Level', 'Jumlah Anggota', 'Uang Masuk Level (Rp)', 
                     'Keuntungan Pendiri Kumulatif (Rp)', 'Total Anggota', 
                     'Total Uang Masuk (Rp)']].copy()
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("Tidak ada data untuk ditampilkan. Periksa parameter simulasi.")

# Peringatan tentang keruntuhan skema
if not df.empty:
    st.warning(
        f"Pada level {level_max}, total anggota: {df['Total Anggota'].iloc[-1]:,.0f}. "
        "Realitas: Skema ini runtuh karena tidak cukup orang untuk direkrut!"
    )

# Visualisasi grafik
st.subheader("Visualisasi Pertumbuhan")
if not df.empty:
    try:
        fig = px.line(
            df,
            x='Level',
            y=['Jumlah Anggota', 'Total Uang Masuk Numerik'],
            title="Pertumbuhan Jumlah Anggota dan Total Uang Masuk",
            labels={'value': 'Skala', 'variable': 'Metrik'},
            log_y=True,
            template="plotly_white"
        )
        fig.update_layout(
            yaxis_title="Skala (Logaritmik)",
            xaxis_title="Level",
            legend_title="Metrik"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f"Error menampilkan grafik: {str(e)}")
        st.error(f"Error menampilkan grafik: {e}")
else:
    st.warning("Tidak ada data untuk visualisasi.")

# Ekspor data
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Ekspor sebagai CSV",
        data=csv,
        file_name="simulasi_piramida.csv",
        mime="text/csv"
    )

# Catatan tambahan
st.subheader("📝 Catatan")
st.info("""
- Simulasi ini menunjukkan pertumbuhan eksponensial skema piramida dan keruntuhannya yang tak terhindarkan.
- Parameter dapat disesuaikan di sidebar untuk mengeksplorasi skenario berbeda.
- Gunakan alat ini hanya untuk tujuan edukasi guna memahami risiko skema ilegal.
""")
