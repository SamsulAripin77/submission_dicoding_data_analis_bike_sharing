# Bike Sharing Dashboard 📊

Dashboard ini memberikan analisis visual tentang penggunaan sepeda berdasarkan berbagai faktor seperti musim, tahun, bulan, hari, kondisi cuaca, dan pola penggunaan antara pengguna kasual dan pengguna terdaftar. Proyek ini menggunakan **Streamlit**, **Pandas**, **Matplotlib**, dan **Seaborn** untuk memvisualisasikan data sepeda sharing.

---

## Fitur Dashboard
- Visualisasi penggunaan sepeda berdasarkan musim.
- Perbandingan jumlah penyewaan sepeda antara tahun 2011 dan 2012.
- Tren penyewaan sepeda per bulan untuk tahun 2012.
- Pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda.
- Perbandingan penyewaan sepeda antara hari kerja dan non-hari kerja.
- Pola penggunaan sepeda berdasarkan waktu dalam sehari.

---

## Setup Environment

1. Membuat Virtual Environment
Langkah pertama adalah membuat environment virtual untuk menjaga agar dependensi tetap terisolasi.

- Windows:
  python -m venv env
  .\env\Scripts\activate

- MacOS/Linux:
  python3 -m venv env
  source env/bin/activate

Setelah menjalankan perintah di atas, kamu akan masuk ke dalam environment virtual yang baru. Cek prompt terminal yang akan menampilkan (env) untuk memastikan environment sudah aktif.

2. Install Dependensi
Setelah environment aktif, install semua dependensi yang dibutuhkan dengan menjalankan perintah berikut:
pip install -r requirements.txt

Perintah ini akan menginstal semua paket yang tercantum dalam file requirements.txt, termasuk **Streamlit**, **Pandas**, **Matplotlib**, dan **Seaborn**.

3. Menjalankan Streamlit App
Setelah dependensi terinstal, jalankan aplikasi Streamlit dengan perintah:
streamlit run dashboard.py

Streamlit akan otomatis membuka aplikasi di browser default kamu. Jika tidak terbuka secara otomatis, buka browser dan kunjungi alamat berikut:
http://localhost:8501

4. Buka Dashboard di Browser
Setelah aplikasi berjalan, buka URL di browser kamu untuk melihat dashboard interaktif yang menampilkan visualisasi data sepeda.