Proyek Analisis Data: Bike Sharing Dataset 🚴
Informasi Mahasiswa

Nama: Muhamad Saefuloh
Email: fatahelmubarokmuhammadraden@gmail.com
ID Dicoding: muhamad_saefuloh_OnbS


Deskripsi Proyek
Proyek ini merupakan analisis data komprehensif terhadap Bike Sharing Dataset dari Capital Bikeshare, Washington D.C. untuk memahami pola penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, waktu, dan tipe pengguna.
Dataset

Sumber: Capital Bikeshare, Washington D.C.
Periode: 2011-2012 (2 tahun)
Records:

Data Harian: 731 hari
Data Per Jam: 17,379 jam


Variabel: 16 kolom (musim, cuaca, suhu, kelembaban, dll)


Struktur Proyek
submission/
├── dashboard/
│   ├── dashboard.py          # Aplikasi dashboard Streamlit
│   ├── day.csv              # Dataset harian
│   └── hour.csv             # Dataset per jam
│
├── data/
│   ├── day.csv              # Dataset harian (sumber asli)
│   └── hour.csv             # Dataset per jam (sumber asli)
│
├── notebook.ipynb           # Notebook analisis data lengkap
├── README.md                # File dokumentasi ini
├── requirements.txt         # List library Python yang dibutuhkan
└── url.txt                  # URL dashboard (jika sudah di-deploy)

Cara Menjalankan Proyek
1️⃣ Setup Environment
Menggunakan Anaconda (Recommended):
bashconda create --name bike-analysis python=3.9
conda activate bike-analysis
pip install -r requirements.txt
Menggunakan pip:
bashpip install -r requirements.txt
Library yang dibutuhkan:

streamlit >= 1.28.0
pandas >= 2.0.0
numpy >= 1.24.0
matplotlib >= 3.7.0
seaborn >= 0.12.0
jupyter (untuk notebook)

2️⃣ Menjalankan Streamlit Dashboard
bash# Masuk ke folder dashboard
cd dashboard

# Jalankan dashboard
streamlit run dashboard.py
Dashboard akan otomatis terbuka di browser pada http://localhost:8501
3️⃣ Menjalankan Jupyter Notebook
bash# Di root folder submission/
jupyter notebook notebook.ipynb
Atau buka dengan JupyterLab:
bashjupyter lab notebook.ipynb

Fitur Dashboard
Dashboard interaktif ini menyediakan:
🎛️ Filter Interaktif

Filter Tahun: Pilih 2011, 2012, atau keduanya
Filter Musim: Pilih Winter, Spring, Summer, Fall

📊 Visualisasi Data
Section 1: Metrik Utama

Total Penyewaan Sepeda
Rata-rata Penyewaan Harian
Suhu Rata-rata
Kelembaban Rata-rata

Section 2: Analisis Tipe Pengguna

Distribusi Casual vs Registered Users (Pie Chart)
Perbandingan Bulanan (Bar Chart)
Statistik Detail

Section 3: Analisis Temporal

Tab 1: Tren Penyewaan Bulanan (2011 vs 2012)
Tab 2: Distribusi Musiman & Box Plot
Tab 3: Pola Mingguan (Weekday vs Weekend)

Section 4: Analisis Dampak Cuaca

Tab 1: Pengaruh Kondisi Cuaca & Suhu
Tab 2: Heatmap Korelasi Antar Variabel

Section 5: Analisis Pola Per Jam

Line Chart: Pola Penyewaan 24 Jam
Heatmap: Hour × Day Pattern
Identifikasi Peak Hours

Section 6: Data & Download

Preview Data Harian
Statistik Deskriptif
Download CSV Terfilter


Proses Analisis Data
Analisis dilakukan mengikuti tahapan standar Data Science:
1. Data Wrangling

Gathering Data: Load dataset dari CSV
Assessing Data: Eksplorasi struktur, tipe data, missing values, duplicates
Cleaning Data: Konversi tipe data, mapping kategori, denormalisasi nilai

2. Exploratory Data Analysis (EDA)
Pertanyaan Bisnis yang Dijawab:

Bagaimana pola penyewaan sepeda berdasarkan musim dan cuaca?

Analisis distribusi per musim
Dampak kondisi cuaca terhadap penyewaan
Identifikasi musim peak dan low season


Bagaimana perbandingan pola penyewaan antara hari kerja dan akhir pekan?

Analisis pola weekday vs weekend
Perbandingan working day vs holiday
Perbedaan behavior pengguna


Pada jam berapa terjadi peak demand untuk penyewaan sepeda?

Analisis pola per jam (0-23)
Identifikasi peak hours
Heatmap hour × weekday


Bagaimana pengaruh faktor cuaca terhadap jumlah penyewaan?

Analisis korelasi suhu, kelembaban, kecepatan angin
Scatter plots untuk visualisasi hubungan
Identifikasi kondisi optimal


Bagaimana tren penyewaan sepeda dari tahun 2011 ke 2012?

Perbandingan tahunan
Analisis pertumbuhan
Identifikasi pola konsisten



3. Visualization & Explanatory Analysis

15+ visualisasi profesional
Pie charts, bar charts, line charts, heatmaps, box plots
Comprehensive dashboard summary

4. Conclusion

Kesimpulan untuk setiap pertanyaan bisnis
Key findings dan insights
Rekomendasi bisnis yang actionable


Hasil Analisis Utama
📊 Key Findings

Pola Musiman

Fall (Musim Gugur) memiliki jumlah penyewaan tertinggi
Winter memiliki penyewaan terendah karena cuaca dingin
Cuaca cerah meningkatkan penyewaan hingga 50% dibanding cuaca buruk


Pola Temporal

Peak hours: 8 AM (commute pagi) dan 5-6 PM (commute sore)
Weekdays menunjukkan pola bimodal (dua puncak)
Weekends lebih merata sepanjang hari (recreational usage)


Faktor Cuaca

Suhu memiliki korelasi positif terkuat (r ≈ 0.63) dengan penyewaan
Kelembaban tinggi berdampak negatif pada penyewaan
Suhu optimal untuk penyewaan: 20-30°C


User Behavior

Registered users mendominasi dengan 81% dari total penyewaan
Casual users meningkat signifikan di musim panas (liburan)
Registered users menunjukkan pola commuter yang konsisten


Pertumbuhan

Pertumbuhan penyewaan dari 2011 ke 2012: ~66%
Pertumbuhan konsisten di hampir semua bulan
Indikasi adopsi program bike sharing yang meningkat



💡 Rekomendasi Bisnis

Optimasi Inventori

Tambah kapasitas sepeda di musim Fall dan Summer
Jadwalkan maintenance di musim Winter (low demand)
Redistribusi sepeda sebelum peak hours


Strategi Pricing

Implementasi dynamic pricing berdasarkan musim dan cuaca
Promosi khusus di hari hujan untuk casual users
Membership benefits untuk registered users


Penempatan Stasiun

Fokus pada area commuter untuk peak hours
Tambah stasiun di area rekreasi untuk weekend
Weather-based station planning


Marketing & Engagement

Target registered user di area perkantoran
Campaign untuk casual user di musim panas
Weather-based notifications dan reminders




Deploy Dashboard ke Cloud (Opsional)
Streamlit Cloud (Gratis)

Persiapan GitHub:

Buat repository di https://github.com
Upload folder dashboard/ (dashboard.py, day.csv, hour.csv)


Deploy:

Login ke https://share.streamlit.io
Connect GitHub account
Pilih repository dan branch
Main file: dashboard.py
Klik Deploy


Akses:

Dapatkan URL publik
Update file url.txt dengan URL dashboard



Detail lengkap: Lihat dokumentasi di docs.streamlit.io

Dependencies
Proyek ini menggunakan library Python berikut:
streamlit>=1.28.0      # Framework dashboard
pandas>=2.0.0          # Data manipulation
numpy>=1.24.0          # Numerical computing
matplotlib>=3.7.0      # Static visualization
seaborn>=0.12.0        # Statistical visualization
jupyter                # Notebook environment
Install semua dengan:
bashpip install -r requirements.txt

Lisensi Dataset
Dataset ini menggunakan lisensi dari Capital Bikeshare dan harus mengutip publikasi berikut:

Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3


Kontak
Untuk pertanyaan atau feedback mengenai proyek ini:

Email: [Silakan isi email Anda]
LinkedIn: [Silakan isi LinkedIn Anda]
GitHub: [Silakan isi GitHub Anda]


Catatan Tambahan

Semua visualisasi dibuat dengan matplotlib dan seaborn
Dashboard menggunakan Streamlit dengan custom CSS styling
Data telah dibersihkan dan divalidasi
Analisis mengikuti best practices Data Science
Code mengikuti PEP 8 style guide


Proyek ini dibuat sebagai submission untuk kursus:
"Belajar Analisis Data dengan Python"
Platform: Dicoding Indonesia

Last updated: December 2025
© 2025 - Proyek Analisis Data Bike Sharing# dasboard-public-e-comerce
