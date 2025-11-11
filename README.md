# CindoEth *(dibaca: cindut)*

<p align="center">
  <img src="https://raw.githubusercontent.com/cindoeth/cindoeth.github.io/main/cindo.svg" alt="CindoEth Logo" width="180">
</p>

<p align="center">
  <a href="https://www.instagram.com/cindolabs/">
    <img src="https://img.shields.io/badge/Instagram-cindolabs-E4405F?logo=instagram&logoColor=white" alt="Instagram">
  </a>
  <a href="https://x.com/cindolabs">
    <img src="https://img.shields.io/badge/X-%40cindolabs-000000?logo=x&logoColor=white" alt="X (Twitter)">
  </a>
  <a href="https://www.facebook.com/cindolabs">
    <img src="https://img.shields.io/badge/Facebook-cindolabs-1877F2?logo=facebook&logoColor=white" alt="Facebook">
  </a>
</p>

<p align="center">
  <b>Laboratorium Fintech Terbuka</b> yang menggabungkan <b>riset perbankan global</b>, <b>replikasi DeFi</b>, dan <b>investasi berbasis blockchain</b> dengan transparansi Web3.
</p>

---

## Tentang CindoEth
**CindoEth** adalah **inti inovasi** dari tim **Puncak Lembah**, **Cindo Labs**, dan identitas Web3:  
[`cindo.eth`](https://app.ens.domains/cindo.eth) | [`arema.eth`](https://app.ens.domains/arema.eth)

Kami **bukan bank**.  
Kami adalah **blueprint masa depan keuangan terdesentralisasi** — mempelajari **ICBC, CCB, ABC, BOC, JPMorgan Chase** untuk direplikasi dalam ekosistem **DeFi**.

### Visi
> Membangun **laboratorium fintech terbuka** yang menggabungkan **data perbankan global** dengan **teknologi blockchain** untuk menciptakan **sistem keuangan generasi baru**.

### Misi
- Replikasi strategi perbankan raksasa dalam **smart contract auditabel**
- Ciptakan **produk DeFi**: pinjaman, tabungan, investasi
- Sediakan **open-source tools** bagi developer & peneliti keuangan

### Produk CindoEth
- **Riset Perbankan Global**: Analisis mendalam model bisnis & risiko kredit bank terbesar dunia.
- **DeFi Replication Lab**: Prototipe smart contract yang meniru layanan perbankan tradisional.
- **Investasi Saham Berbasis Blockchain**: Tokenisasi aset properti & bagi hasil transparan via smart contract.

---

## Tech Stack

| Kategori                | Teknologi                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| Website             | [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [Python](https://www.python.org/) |
| Desain              | [SVG](https://developer.mozilla.org/en-US/docs/Web/SVG), Figma, Canva     |
| Deployment          | [GitHub Pages](https://pages.github.com/)                                |
| Blockchain          | Ethereum, Polygon, Bitcoin, TON, Solana                                   |
| Data & Analitik     | [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/python/), Google Analytics |
| Pembukuan           | [CindoEth Streamlit Dashboard](https://cindoeth.streamlit.app/)           |

### Penggunaan Python
Python digunakan untuk **CindoEth Financial Dashboard**, aplikasi berbasis [Streamlit](https://streamlit.io/) yang mengelola:
- **Manajemen Investasi**: Transaksi saham blockchain, saldo, & profit-sharing
- **Visualisasi Interaktif**: Grafik ROI, pertumbuhan dana, & distribusi investor
- **Integrasi GitHub API**: Sinkronisasi data real-time
- **Keamanan Web3**: Autentikasi via wallet (MetaMask), ENS verification
- **Smart Contract Simulator**: Kalkulator bagi hasil otomatis

Contoh kode untuk tabel investor interaktif:
```python
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Data investor (contoh)
df = st.session_state.get('investors', pd.DataFrame({
    'investor': ['Alice.eth', 'Bob.sol', 'Charlie.ton'],
    'saham': [100, 250, 150],
    'saldo': [50000000, 125000000, 75000000],
    'roi': [12.5, 15.0, 11.8]
}))

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("investor", headerName="Investor", width=140)
gb.configure_column("saham", headerName="Saham", width=100)
gb.configure_column("saldo", headerName="Saldo (Rp)", width=130, type=["numericColumn", "numberColumnFilter"])
gb.configure_column("roi", headerName="ROI (%)", width=90, valueFormatter="value.toFixed(2) + '%'")
gb.configure_selection("single")
AgGrid(df, gridOptions=gb.build(), height=350, fit_columns_on_grid_load=True)
```

---

## 🛣️ Roadmap

| Tahun | Fokus Utama | Rencana Strategis |
|-------|-------------|------------------|
| **2025** | Fondasi & Branding | - Peluncuran platform `Hocindo` <br> - Logo & identitas visual <br> - Website resmi & profil investasi |
| **2026** | Ekspansi & Produk | - Pembukaan hotel kreatif pertama <br> - Paket pengalaman romantis & bisnis <br> - Program investasi properti tahap awal |
| **2027** | Skala & Globalisasi | - Ekspansi ke beberapa kota besar di Indonesia <br> - Kemitraan internasional <br> - Platform investasi berbasis blockchain |

---

## 📬 Kontak
📍 Jl. Panglima Sudirman No. 19, Bandarkedungmulyo – Jombang, Jawa Timur – Indonesia 🇮🇩
📧 Email: [ringinbambu@gmail.com](mailto:ringinbambu@gmail.com)  
📱 WhatsApp: [+62 8999 587 888](https://wa.me/628999587888)  

---

<p align="center">
  © 2025 <b>Cindoeth</b> – Semua hak dilindungi
</p>
