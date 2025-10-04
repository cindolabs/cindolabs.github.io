# Simulasi Piramida Edukatif - JANGAN GUNAKAN UNTUK PR AKTIK!
biaya_masuk = 1000000  # Rp 1jt per orang
faktor_rekrut = 2  # Setiap rekrut 2 orang
bonus_persen = 0.5  # 50% dari biaya downline

def simulasi_piramida(level_max=10):
    import pandas as pd
    data = []
    total_anggota = 0
    total_uang = 0
    keuntungan_pendiri = 0
    
    for level in range(1, level_max + 1):
        anggota_level = faktor_rekrut ** (level - 1)
        uang_level = anggota_level * biaya_masuk
        total_anggota += anggota_level
        total_uang += uang_level
        keuntungan_level = uang_level * bonus_persen  # Sederhana: pendiri ambil sebagian
        keuntungan_pendiri += keuntungan_level
        data.append({
            'Level': level,
            'Jumlah Anggota': anggota_level,
            'Uang Masuk Level (Rp)': f"{uang_level:,.0f}",
            'Keuntungan Pendiri Kumulatif (Rp)': f"{keuntungan_pendiri:,.0f}",
            'Total Anggota': total_anggota,
            'Total Uang Masuk (Rp)': f"{total_uang:,.0f}"
        })
    
    df = pd.DataFrame(data)
    print("Tabel Simulasi Piramida (Edukasi Saja):")
    print(df)
    print(f"\nPeringatan: Pada level {level_max}, total anggota: {total_anggota}. Realitas: Runtuh karena tak cukup orang!")

simulasi_piramida(10)
