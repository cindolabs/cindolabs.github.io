<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catatan Keuangan HOCINDO - September 2025</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    /* CSS tetap sama seperti kode asli Anda */
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      background-color: #f4f4f4;
      color: #333;
    }
    h2, h3 {
      color: #006400;
    }
    .summary {
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      max-width: 1000px;
      border-collapse: collapse;
      margin-top: 20px;
      background-color: white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    th, td {
      border: 1px solid #ddd;
      padding: 10px;
      text-align: left;
    }
    th {
      background-color: #006400;
      color: white;
    }
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    .form-container, .roi-container {
      margin: 20px 0;
      padding: 10px;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    input, button {
      padding: 8px;
      margin: 5px;
      font-size: 14px;
    }
    button {
      background-color: #006400;
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }
    button:hover {
      background-color: #008000;
    }
    .notes {
      margin-top: 20px;
      font-size: 14px;
      color: #555;
    }
    .chart-container {
      max-width: 500px;
      margin: 20px auto;
      padding: 10px;
      background-color: white;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .action-buttons {
      margin: 10px 0;
    }
    .chart-switcher {
      margin: 10px 0;
      text-align: center;
    }
    .chart-switcher button {
      margin: 0 5px;
    }
    .chart-switcher button.active {
      background-color: #004d00;
    }
  </style>
</head>
<body>
  <div class="summary">
    <h2>Catatan Keuangan Investor HOCINDO - September 2025</h2>
    <p><strong>Harga per Lembar Saham:</strong> Rp {{ harga_saham }}</p>
    <p><strong>Total Investasi Bulan Ini:</strong> <span id="totalInvestasi">Rp {{ "{:,.0f}".format(summary.total_investasi) }},00</span></p>
    <p><strong>Total Lembar Saham:</strong> <span id="totalSaham">{{ summary.total_saham }}</span></p>
    <p><strong>Jumlah Investor:</strong> <span id="jumlahInvestor">{{ summary.jumlah_investor }}</span></p>
    <p><strong>Dana Kelolaan:</strong> <span id="danaKelolaan">Rp {{ "{:,.0f}".format(summary.dana_kelolaan) }},00</span></p>
  </div>

  <div class="form-container">
    <h3>Tambah Transaksi</h3>
    <input type="date" id="tanggal" required>
    <input type="text" id="nama" placeholder="Nama Investor" required>
    <input type="text" id="rekening" placeholder="No. Rekening" required>
    <input type="text" id="nominal" placeholder="Nominal (Rp)" required>
    <button onclick="tambahTransaksi()">Tambah</button>
  </div>

  <div class="roi-container">
    <h3>Kalkulator ROI</h3>
    <input type="number" id="roiPercent" placeholder="ROI per bulan (%)" min="0" step="0.1" required>
    <button onclick="hitungROI()">Hitung ROI</button>
    <p><strong>Estimasi Keuntungan:</strong> <span id="roiResult">Rp 0,00</span></p>
  </div>

  <div class="action-buttons">
    <button onclick="exportToCSV()">Export ke CSV</button>
    <button onclick="exportChart()">Export Chart ke PNG</button>
  </div>

  <div class="chart-switcher">
    <button onclick="switchChart('pie')" class="active">Pie Chart</button>
    <button onclick="switchChart('bar')">Bar Chart</button>
    <button onclick="switchChart('line')">Line Chart</button>
    <button onclick="switchChart('pie_saham')">Pie Chart (Saham)</button>
  </div>

  <div class="chart-container">
    <h3 id="chartTitle">Proporsi Investasi per Investor</h3>
    <canvas id="investasiChart"></canvas>
  </div>

  <table id="transaksiTable">
    <tr>
      <th>Tanggal</th>
      <th>Nama Investor</th>
      <th>No. Rekening</th>
      <th>Jenis Transaksi</th>
      <th>Nominal</th>
      <th>Jumlah Lembar Saham</th>
      <th>Saldo</th>
    </tr>
    {% for tx in transaksi %}
    <tr>
      <td>{{ tx.tanggal }}</td>
      <td>{{ tx.nama }}</td>
      <td>{{ tx.rekening }}</td>
      <td>{{ tx.jenis }}</td>
      <td>Rp {{ "{:,.0f}".format(tx.nominal) }},00</td>
      <td>{{ "{:,.0f}".format(tx.saham) }}</td>
      <td>Rp {{ "{:,.0f}".format(tx.saldo) }},00</td>
    </tr>
    {% endfor %}
  </table>

  <div class="notes">
    <h3>Catatan Tambahan</h3>
    <ul>
      <li>Transaksi oleh Mochamad Tabrani merupakan investasi awal untuk produk UMKM Hocindo.</li>
      <li>Transaksi oleh Pipit Puspita dan lainnya merupakan tambahan investasi untuk alokasi saham hotel.</li>
      <li>Dana akan dikelola oleh tim Hocindo untuk alokasi saham hotel, emas, atau aset lainnya.</li>
      <li>Harga saham per lembar adalah Rp {{ harga_saham }}, dengan jumlah lembar saham dihitung berdasarkan nominal investasi.</li>
    </ul>
  </div>

  <script>
    // JavaScript tetap sama seperti kode asli, tapi modifikasi tambahTransaksi untuk POST ke Flask
    const HARGA_PER_SAHAM = {{ harga_saham }};

    // ... (semua fungsi updateChart, switchChart, hitungROI, exportToCSV, exportChart tetap sama seperti kode asli Anda)

    // Modifikasi tambahTransaksi untuk kirim ke server
    async function tambahTransaksi() {
      const tanggal = document.getElementById("tanggal").value;
      const nama = document.getElementById("nama").value;
      const rekening = document.getElementById("rekening").value;
      const nominalInput = document.getElementById("nominal").value.replace(/[^0-9]/g, "");
      if (!tanggal || !nama || !rekening || !nominalInput) {
        alert("Isi semua kolom!");
        return;
      }

      const nominal = parseInt(nominalInput);
      const jumlahSaham = Math.floor(nominal / HARGA_PER_SAHAM);

      try {
        const response = await fetch('/api/add-transaction', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tanggal, nama, rekening, nominal: nominalInput })
        });
        const result = await response.json();
        if (result.success) {
          // Tambah row ke tabel
          const table = document.getElementById("transaksiTable");
          const row = table.insertRow(-1);
          row.innerHTML = `
            <td>${tanggal}</td>
            <td>${nama}</td>
            <td>${rekening}</td>
            <td>Investasi</td>
            <td>Rp ${nominal.toLocaleString("id-ID")},00</td>
            <td>${jumlahSaham.toLocaleString("id-ID")}</td>
            <td>Rp ${result.new_entry.saldo.toLocaleString("id-ID")},00</td>
          `;
          // Update summary dari server
          document.getElementById("totalInvestasi").textContent = `Rp ${result.summary.total_investasi.toLocaleString("id-ID")},00`;
          document.getElementById("totalSaham").textContent = result.summary.total_saham.toLocaleString("id-ID");
          document.getElementById("jumlahInvestor").textContent = result.summary.jumlah_investor;
          document.getElementById("danaKelolaan").textContent = `Rp ${result.summary.dana_kelolaan.toLocaleString("id-ID")},00`;
          updateChart();  // Refresh chart
          // Clear form
          document.getElementById("tanggal").value = "";
          document.getElementById("nama").value = "";
          document.getElementById("rekening").value = "";
          document.getElementById("nominal").value = "";
        } else {
          alert("Gagal menambah transaksi!");
        }
      } catch (error) {
        alert("Error: " + error);
      }
    }

    // Inisialisasi chart saat halaman dimuat
    updateChart();
  </script>
</body>
</html>
