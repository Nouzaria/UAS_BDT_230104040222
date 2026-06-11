# ============================================================
# SMART CAMPUS ATTENDANCE ANALYTICS
# Engine Spark - UAS Teknologi Big Data
# Nama File : main_uas_230104040222.py
# Pipeline  : Generate Data -> Spark Analytics -> Parquet Storage
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, sum as _sum, hour, minute, desc
from datetime import datetime, timedelta
import random
import os
import shutil


# ============================================================
# 1. PATH CONFIGURATION
# ============================================================

# Menggunakan absolute path agar aman dijalankan dari WSL/Linux
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

print("============================================================")
print(" SMART CAMPUS ATTENDANCE ANALYTICS - SPARK ENGINE")
print("============================================================")
print(f"Base Directory  : {BASE_DIR}")
print(f"Output Directory: {OUTPUT_DIR}")
print("============================================================")


# ============================================================
# 2. INIT SPARK SESSION
# ============================================================

spark = SparkSession.builder \
    .appName("SmartCampusAttendanceAnalytics") \
    .master("local[*]") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session berhasil dijalankan.")
print(f"Spark Version: {spark.version}")
print("------------------------------------------------------------")


# ============================================================
# 3. PREPARE OUTPUT FOLDER
# ============================================================

# Membersihkan folder output lama agar data tidak tercampur
if os.path.exists(OUTPUT_DIR):
    print("Folder output lama ditemukan. Menghapus folder output lama...")
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Folder output siap digunakan.")
print("------------------------------------------------------------")


# ============================================================
# 4. GENERATE DUMMY ATTENDANCE DATA
# ============================================================

buildings = [
    "Fakultas Sains dan Teknologi",
    "Perpustakaan",
    "Auditorium"
]

# Data 100 menit, dimulai dari jam operasional kampus
start_time = datetime(2026, 1, 1, 7, 0, 0)

attendance_data = []

# Seed agar hasil random stabil ketika script dijalankan ulang
random.seed(42)

for i in range(100):
    current_time = start_time + timedelta(minutes=i)

    for building in buildings:
        attendance_count = random.randint(20, 300)

        attendance_data.append((
            current_time,
            building,
            attendance_count
        ))

attendance_df = spark.createDataFrame(
    attendance_data,
    ["timestamp", "building", "attendance_count"]
)

print("Data simulasi berhasil dibuat.")
print(f"Total baris data: {attendance_df.count()}")
print("Contoh data:")
attendance_df.show(10, truncate=False)
print("------------------------------------------------------------")


# ============================================================
# 5. SPARK TRANSFORMATION
# ============================================================

# 5.1 Total mahasiswa per gedung
attendance_total_df = attendance_df.groupBy("building") \
    .agg(_sum("attendance_count").alias("total_attendance")) \
    .orderBy(desc("total_attendance"))

print("Total mahasiswa per gedung:")
attendance_total_df.show(truncate=False)


# 5.2 Tren kehadiran per 20 menit
attendance_time_df = attendance_df.groupBy(
    window(col("timestamp"), "20 minutes"),
    col("building")
).agg(
    _sum("attendance_count").alias("total_attendance")
).select(
    col("window.start").alias("start_time"),
    col("window.end").alias("end_time"),
    col("building"),
    col("total_attendance")
).orderBy(
    col("start_time"),
    col("building")
)

print("Tren kehadiran per 20 menit:")
attendance_time_df.show(20, truncate=False)


# 5.3 Dataset AI berbasis jam
ml_attendance_df = attendance_df.withColumn(
    "hour", hour(col("timestamp"))
).withColumn(
    "minute", minute(col("timestamp"))
).select(
    "timestamp",
    "building",
    "hour",
    "minute",
    "attendance_count"
).orderBy(
    "timestamp",
    "building"
)

print("Dataset AI berbasis jam:")
ml_attendance_df.show(10, truncate=False)
print("------------------------------------------------------------")


# ============================================================
# 6. SAVE TO PARQUET
# ============================================================

def save_to_parquet(df, folder_name):
    path = os.path.join(OUTPUT_DIR, folder_name)
    print(f"Menyimpan data ke: {path}")
    df.write.mode("overwrite").parquet(path)
    print(f"Berhasil menyimpan: output/{folder_name}")


try:
    save_to_parquet(attendance_total_df, "attendance_total")
    save_to_parquet(attendance_time_df, "attendance_time")
    save_to_parquet(ml_attendance_df, "ml_attendance")

    print("------------------------------------------------------------")
    print("SEMUA DATA BERHASIL DISIMPAN KE FORMAT PARQUET")
    print("Folder yang terbentuk:")
    print("1. output/attendance_total")
    print("2. output/attendance_time")
    print("3. output/ml_attendance")
    print("------------------------------------------------------------")

except Exception as e:
    print("ERROR SAAT MENYIMPAN DATA:")
    print(e)


# ============================================================
# 7. STOP SPARK
# ============================================================

spark.stop()

print("Spark Session ditutup.")
print("ENGINE SELESAI DIJALANKAN.")
print("============================================================")
