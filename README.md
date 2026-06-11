# Smart Campus Attendance Analytics

## Author

**Achmad Fauzil 'Adhim**
**NIM:** 230104040222
**Kelas:** TI23A
**Program Studi:** Teknologi Informasi
**Universitas:** UIN Antasari Banjarmasin

---

## Deskripsi Singkat

**Smart Campus Attendance Analytics** adalah proyek akhir mata kuliah **Teknologi Big Data** yang bertujuan untuk menganalisis kepadatan mahasiswa pada beberapa gedung kampus berdasarkan data simulasi tapping kartu mahasiswa.

Sistem ini membangun pipeline Big Data sederhana dari proses pembuatan data, pemrosesan menggunakan Apache Spark, penyimpanan data dalam format Parquet, prediksi kepadatan menggunakan Machine Learning, hingga visualisasi interaktif menggunakan Streamlit.

Pipeline utama pada proyek ini adalah:

```text
Attendance Data → Spark Analytics → Parquet Storage → AI Prediction → Streamlit Dashboard
```

Data yang digunakan merupakan data simulasi dengan field:

```text
timestamp
building
attendance_count
```

Gedung yang dianalisis:

```text
Fakultas Sains dan Teknologi
Perpustakaan
Auditorium
```

---

## Fitur Utama

* Generate data tapping mahasiswa selama 100 menit.
* Analisis total mahasiswa per gedung.
* Analisis tren kehadiran per 20 menit.
* Penyimpanan hasil analisis ke format Parquet.
* Dashboard interaktif berbasis Streamlit.
* Filter data berdasarkan gedung.
* KPI total mahasiswa dan rata-rata kehadiran.
* Grafik tren kehadiran mahasiswa.
* Prediksi kepadatan kampus menggunakan Linear Regression.
* Insight jam sibuk kampus berdasarkan hasil dashboard.

---

## Tech Stack

Proyek ini menggunakan teknologi berikut:

| Kategori                | Teknologi              |
| ----------------------- | ---------------------- |
| Programming Language    | Python                 |
| Development Environment | Linux / WSL Ubuntu     |
| Code Editor             | Visual Studio Code     |
| Big Data Processing     | Apache Spark / PySpark |
| Data Storage            | Parquet                |
| Data Analysis           | Pandas                 |
| Machine Learning        | Scikit-learn           |
| Visualization           | Streamlit, Plotly      |
| CLI                     | Bash                   |
| Version Control         | Git & GitHub           |

---

## Struktur Project

```text
smart-campus-attendance/
│
├── main_uas_230104040222.py
├── dashboard_230104040222.py
├── requirements.txt
├── README.md
│
├── output/
│   ├── attendance_total/
│   ├── attendance_time/
│   └── ml_attendance/
│
├── screenshots/
│
└── laporan/
```

Keterangan folder:

| Folder / File               | Fungsi                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------- |
| `main_uas_230104040222.py`  | Script utama untuk generate data, Spark transformation, dan menyimpan hasil ke Parquet |
| `dashboard_230104040222.py` | Dashboard Streamlit untuk visualisasi dan prediksi                                     |
| `requirements.txt`          | Daftar library Python yang digunakan                                                   |
| `output/attendance_total`   | Hasil total kehadiran mahasiswa per gedung                                             |
| `output/attendance_time`    | Hasil tren kehadiran per 20 menit                                                      |
| `output/ml_attendance`      | Dataset untuk Machine Learning                                                         |
| `screenshots/`              | Folder untuk menyimpan bukti screenshot                                                |
| `laporan/`                  | Folder untuk menyimpan laporan analisis                                                |

---

## Prasyarat Sistem

Sebelum menjalankan project, pastikan perangkat sudah memiliki:

* WSL Ubuntu / Linux Environment
* Python 3.12.3 atau versi Python 3.10+
* Java JDK
* Git
* Visual Studio Code
* Extension WSL pada VS Code

---

## Instalasi Project

### 1. Clone Repository

```bash
git clone https://github.com/username/smart-campus-attendance.git
cd smart-campus-attendance
```

Ganti `username` sesuai username GitHub masing-masing.

---

### 2. Update Package Linux

```bash
sudo apt update
sudo apt upgrade -y
```

---

### 3. Install Java dan Python Environment

Apache Spark membutuhkan Java agar dapat berjalan. Install Java dan Python package pendukung dengan perintah berikut:

```bash
sudo apt install openjdk-17-jdk python3-full python3-venv python3-pip -y
```

Cek versi Java:

```bash
java -version
```

Jika Java berhasil terinstall, terminal akan menampilkan versi Java yang digunakan.

---

### 4. Buat Virtual Environment

Buat virtual environment Python agar dependency project tidak bercampur dengan sistem utama.

```bash
python3 -m venv venv
source venv/bin/activate
```

Jika virtual environment aktif, terminal akan menampilkan tanda seperti ini:

```text
(venv) username@device:~/smart-campus-attendance$
```

---

### 5. Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

---

### 6. Install Library Python

Jika file `requirements.txt` sudah tersedia, jalankan:

```bash
pip install -r requirements.txt
```

Jika belum ada, install manual dengan perintah berikut:

```bash
pip install pyspark pandas streamlit plotly scikit-learn pyarrow
```

Kemudian simpan dependency ke `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Cek Instalasi PySpark

Sebelum menjalankan project, pastikan PySpark dapat berjalan dengan baik.

Jalankan perintah berikut:

```bash
unset SPARK_HOME
unset PYTHONPATH
export SPARK_LOCAL_IP=127.0.0.1
```

Kemudian test PySpark:

```bash
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.appName('TestSpark').master('local[*]').getOrCreate(); spark.sparkContext.setLogLevel('ERROR'); print('Spark OK:', spark.version); spark.stop()"
```

Jika berhasil, output akan menampilkan:

```text
Spark OK: versi_spark
```

Catatan: Warning seperti berikut masih aman selama tidak ada `Traceback` atau error fatal:

```text
WARN NativeCodeLoader: Unable to load native-hadoop library
WARN Utils: Your hostname resolves to a loopback address
```

---

## Cara Menjalankan Project

### 1. Aktifkan Virtual Environment

```bash
source venv/bin/activate
```

---

### 2. Jalankan Engine Spark

Jalankan script utama untuk generate data, melakukan transformasi Spark, dan menyimpan hasil ke Parquet.

```bash
python main_uas_230104040222.py
```

Jika berhasil, terminal akan menampilkan pesan:

```text
SEMUA DATA BERHASIL DISIMPAN KE FORMAT PARQUET
```

Setelah itu, folder `output/` akan berisi:

```text
output/attendance_total
output/attendance_time
output/ml_attendance
```

Cek dengan perintah:

```bash
ls output
```

---

### 3. Jalankan Dashboard Streamlit

Setelah engine berhasil dijalankan dan folder Parquet terbentuk, jalankan dashboard:

```bash
streamlit run dashboard_230104040222.py
```

Kemudian buka browser pada alamat:

```text
http://localhost:8501
```

---

## Alur Penggunaan

Urutan menjalankan project yang benar:

```text
1. Aktifkan virtual environment
2. Jalankan main_uas_230104040222.py
3. Pastikan folder output terbentuk
4. Jalankan dashboard_230104040222.py
5. Buka dashboard di browser
6. Analisis hasil KPI, grafik tren, dan prediksi kepadatan kampus
```

Penting: Dashboard tidak akan berjalan dengan benar jika script engine belum dijalankan terlebih dahulu.

---

## Output Project

Output yang dihasilkan dari project ini adalah:

1. Script Python:

   * `main_uas_230104040222.py`
   * `dashboard_230104040222.py`

2. Folder hasil Parquet:

   * `output/attendance_total`
   * `output/attendance_time`
   * `output/ml_attendance`

3. Dashboard Streamlit:

   * KPI total mahasiswa
   * Filter gedung
   * Grafik tren kehadiran
   * Prediksi kepadatan kampus

4. Analisis jam sibuk kampus:

   * Gedung dengan kehadiran tertinggi
   * Interval waktu tersibuk
   * Insight pengelolaan kepadatan kampus

---

## Ringkasan Analisis

Berdasarkan hasil dashboard, sistem dapat membantu kampus untuk mengetahui pola kepadatan mahasiswa pada beberapa gedung utama. Data tapping mahasiswa diproses menggunakan Spark untuk menghasilkan total kehadiran, tren per 20 menit, serta dataset prediksi berbasis jam.

Informasi ini dapat digunakan untuk mendukung pengambilan keputusan seperti pengaturan keamanan, pengelolaan fasilitas gedung, penyesuaian layanan administrasi, serta antisipasi kepadatan pada jam sibuk kampus.

---

## Troubleshooting

### 1. Error: `ModuleNotFoundError`

Penyebab: Library belum terinstall atau virtual environment belum aktif.

Solusi:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Jika belum ada `requirements.txt`:

```bash
pip install pyspark pandas streamlit plotly scikit-learn pyarrow
```

---

### 2. Error: `Data Parquet belum ditemukan`

Penyebab: Dashboard dijalankan sebelum engine Spark.

Solusi:

```bash
python main_uas_230104040222.py
streamlit run dashboard_230104040222.py
```

---

### 3. Error PySpark: `Java gateway process exited`

Penyebab umum:

* Java belum terinstall.
* Environment Spark bermasalah.
* Konflik `SPARK_HOME` atau `PYTHONPATH`.

Solusi:

```bash
sudo apt install openjdk-17-jdk -y
unset SPARK_HOME
unset PYTHONPATH
export SPARK_LOCAL_IP=127.0.0.1
```

Lalu test ulang:

```bash
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.appName('TestSpark').master('local[*]').getOrCreate(); print('Spark OK:', spark.version); spark.stop()"
```

---

### 4. Dashboard tidak terbuka

Pastikan Streamlit berjalan:

```bash
streamlit run dashboard_230104040222.py
```

Buka browser:

```text
http://localhost:8501
```

Jika port bermasalah, jalankan:

```bash
streamlit run dashboard_230104040222.py --server.port 8502
```

Lalu buka:

```text
http://localhost:8502
```

---

### 5. Warning Native Hadoop Library

Jika muncul warning seperti ini:

```text
WARN NativeCodeLoader: Unable to load native-hadoop library
```

Warning tersebut masih aman untuk praktikum lokal selama program tetap berjalan dan tidak menampilkan `Traceback`.

---

## Catatan Penting

* Jalankan project dari root folder `smart-campus-attendance`.
* Jangan mengubah nama folder output karena dashboard membaca path tersebut.
* Jalankan engine Spark terlebih dahulu sebelum dashboard.
* Gunakan virtual environment agar dependency lebih stabil.
* Jika memakai Python 3.12.3, disarankan menginstall PySpark versi terbaru tanpa mengunci versi lama secara manual.

---

## License

Project ini dibuat untuk keperluan pembelajaran dan tugas akhir mata kuliah **Teknologi Big Data**.
