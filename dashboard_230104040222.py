# ============================================================
# SMART CAMPUS ATTENDANCE ANALYTICS
# Dashboard Streamlit - UAS Teknologi Big Data
# Nama File : dashboard_230104040222.py
# Pipeline  : Parquet Storage -> AI Prediction -> Streamlit
# ============================================================

import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart Campus Attendance Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Smart Campus Attendance Analytics")
st.markdown(
    """
    Dashboard ini digunakan untuk menganalisis kepadatan mahasiswa pada beberapa gedung kampus
    berdasarkan data tapping kartu mahasiswa.
    """
)


# ============================================================
# 2. PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

ATTENDANCE_TOTAL_PATH = os.path.join(OUTPUT_DIR, "attendance_total")
ATTENDANCE_TIME_PATH = os.path.join(OUTPUT_DIR, "attendance_time")
ML_ATTENDANCE_PATH = os.path.join(OUTPUT_DIR, "ml_attendance")


# ============================================================
# 3. DATA LOADING
# ============================================================

@st.cache_data
def load_parquet(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_parquet(path)


attendance_total_df = load_parquet(ATTENDANCE_TOTAL_PATH)
attendance_time_df = load_parquet(ATTENDANCE_TIME_PATH)
ml_attendance_df = load_parquet(ML_ATTENDANCE_PATH)


# ============================================================
# 4. VALIDATION
# ============================================================

if attendance_total_df.empty or attendance_time_df.empty or ml_attendance_df.empty:
    st.error("Data Parquet belum ditemukan atau masih kosong.")
    st.warning("Jalankan engine terlebih dahulu dengan perintah:")
    st.code("python main_uas_230104040222.py")
    st.stop()


# Convert datetime
attendance_time_df["start_time"] = pd.to_datetime(attendance_time_df["start_time"])
attendance_time_df["end_time"] = pd.to_datetime(attendance_time_df["end_time"])
ml_attendance_df["timestamp"] = pd.to_datetime(ml_attendance_df["timestamp"])


# ============================================================
# 5. SIDEBAR FILTER
# ============================================================

st.sidebar.header("🔎 Filter Dashboard")

building_list = sorted(ml_attendance_df["building"].unique())

selected_building = st.sidebar.selectbox(
    "Pilih Gedung",
    building_list
)

filtered_time_df = attendance_time_df[
    attendance_time_df["building"] == selected_building
]

filtered_ml_df = ml_attendance_df[
    ml_attendance_df["building"] == selected_building
]


# ============================================================
# 6. KPI METRICS
# ============================================================

total_all_attendance = int(attendance_total_df["total_attendance"].sum())

selected_building_total = int(
    attendance_total_df.loc[
        attendance_total_df["building"] == selected_building,
        "total_attendance"
    ].sum()
)

average_attendance = round(filtered_ml_df["attendance_count"].mean(), 2)
max_attendance = int(filtered_ml_df["attendance_count"].max())

peak_row = filtered_time_df.loc[
    filtered_time_df["total_attendance"].idxmax()
]

peak_start = peak_row["start_time"].strftime("%H:%M")
peak_end = peak_row["end_time"].strftime("%H:%M")
peak_value = int(peak_row["total_attendance"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Mahasiswa Semua Gedung", total_all_attendance)

with col2:
    st.metric(f"Total di {selected_building}", selected_building_total)

with col3:
    st.metric("Rata-rata Tapping", average_attendance)

with col4:
    st.metric("Tapping Tertinggi", max_attendance)


st.divider()


# ============================================================
# 7. DATA SUMMARY
# ============================================================

st.subheader("📌 Ringkasan Kepadatan Kampus")

top_building_row = attendance_total_df.iloc[0]
top_building = top_building_row["building"]
top_building_value = int(top_building_row["total_attendance"])

st.info(
    f"Gedung dengan total kehadiran tertinggi adalah **{top_building}** "
    f"dengan total **{top_building_value} mahasiswa**. "
    f"Pada gedung **{selected_building}**, interval tersibuk terjadi pada pukul "
    f"**{peak_start} - {peak_end}** dengan total **{peak_value} mahasiswa**."
)


# ============================================================
# 8. TOTAL ATTENDANCE PER BUILDING
# ============================================================

st.subheader("🏢 Total Mahasiswa per Gedung")

fig_total = px.bar(
    attendance_total_df,
    x="building",
    y="total_attendance",
    text="total_attendance",
    title="Total Kehadiran Mahasiswa Berdasarkan Gedung",
    labels={
        "building": "Gedung",
        "total_attendance": "Total Mahasiswa"
    }
)

fig_total.update_traces(textposition="outside")
fig_total.update_layout(xaxis_tickangle=-20)

st.plotly_chart(fig_total, use_container_width=True)


# ============================================================
# 9. ATTENDANCE TREND
# ============================================================

st.subheader("📈 Grafik Tren Kehadiran per 20 Menit")

fig_trend = px.line(
    filtered_time_df,
    x="start_time",
    y="total_attendance",
    markers=True,
    title=f"Tren Kehadiran Mahasiswa - {selected_building}",
    labels={
        "start_time": "Waktu",
        "total_attendance": "Total Mahasiswa"
    }
)

st.plotly_chart(fig_trend, use_container_width=True)


# ============================================================
# 10. RAW DATA PREVIEW
# ============================================================

with st.expander("📄 Lihat Data AI untuk Gedung Terpilih"):
    st.dataframe(
        filtered_ml_df.sort_values("timestamp").tail(30),
        use_container_width=True
    )


# ============================================================
# 11. MACHINE LEARNING PREDICTION
# ============================================================

st.subheader("🤖 Prediksi Kepadatan Kampus dengan Linear Regression")

st.markdown(
    """
    Model Machine Learning menggunakan **Linear Regression** untuk memprediksi
    `attendance_count` berdasarkan fitur `hour`.
    """
)

# Prepare training data
X = filtered_ml_df[["hour"]]
y = filtered_ml_df["attendance_count"]

model = LinearRegression()
model.fit(X, y)

min_hour = int(filtered_ml_df["hour"].min())
max_hour = int(filtered_ml_df["hour"].max())

hour_input = st.slider(
    "Pilih Jam untuk Prediksi",
    min_value=0,
    max_value=23,
    value=min_hour
)

predicted_attendance = model.predict(pd.DataFrame({"hour": [hour_input]}))[0]
predicted_attendance = max(0, int(round(predicted_attendance)))

st.success(
    f"Prediksi jumlah mahasiswa di **{selected_building}** pada pukul "
    f"**{hour_input}:00** adalah sekitar **{predicted_attendance} mahasiswa**."
)

# Prediction trend per hour
prediction_hours = pd.DataFrame({
    "hour": list(range(0, 24))
})

prediction_hours["predicted_attendance"] = model.predict(prediction_hours[["hour"]])
prediction_hours["predicted_attendance"] = prediction_hours["predicted_attendance"].round().astype(int)
prediction_hours["predicted_attendance"] = prediction_hours["predicted_attendance"].clip(lower=0)

fig_prediction = px.line(
    prediction_hours,
    x="hour",
    y="predicted_attendance",
    markers=True,
    title=f"Tren Prediksi Kepadatan - {selected_building}",
    labels={
        "hour": "Jam",
        "predicted_attendance": "Prediksi Jumlah Mahasiswa"
    }
)

st.plotly_chart(fig_prediction, use_container_width=True)


# ============================================================
# 12. FINAL INSIGHT
# ============================================================

st.subheader("🧠 Insight Analisis Jam Sibuk")

st.write(
    f"""
    Berdasarkan hasil dashboard, gedung **{selected_building}** memiliki periode tersibuk
    pada pukul **{peak_start} - {peak_end}** dengan total **{peak_value} mahasiswa**.
    Informasi ini dapat digunakan oleh pihak kampus untuk mengatur layanan gedung,
    keamanan, jadwal operasional, dan fasilitas pendukung pada jam-jam dengan tingkat
    kepadatan tinggi.
    """
)

st.caption("Smart Campus Attendance Analytics - Teknologi Big Data")
