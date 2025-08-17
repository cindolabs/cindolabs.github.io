---
title: Menggunakan Moving Average
layout: default
---

# Indikator Moving Average 📊

Moving Average (MA) membantu trader mengidentifikasi tren harga.

## Jenis Moving Average
- **Simple Moving Average (SMA)**: Rata-rata harga sederhana.
- **Exponential Moving Average (EMA)**: Memberi bobot lebih pada harga terbaru.

> **Strategi**: Gunakan crossover MA untuk sinyal beli/jual.

<details>
  <summary>🔍 Contoh Strategi Golden Cross</summary>
  <p>Ketika EMA 50 memotong EMA 200 ke atas, ini adalah sinyal beli yang kuat.</p>
  <p>"Ikuti tren, bukan emosi." – Trader Profesional</p>
</details>

```python
# Pseudocode untuk menghitung SMA
def calculate_sma(prices, period):
    return sum(prices[-period:]) / period
