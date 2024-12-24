import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fungsi untuk memuat data
@st.cache_data
def load_data():
  day_url = "https://docs.google.com/spreadsheets/d/1FcYHP3OCtglJ4a3YxfkCjS9wzmxJmt9gKqvmjdcWTU4/export?format=csv"
  hour_url = "https://docs.google.com/spreadsheets/d/1Px60wcBo7nyyjt5oCKx1T614VR4lNWGv-Amupgy1HgY/export?format=csv"
  day_df = pd.read_csv(day_url)
  hour_df = pd.read_csv(hour_url)
  day_df["dteday"] = pd.to_datetime(day_df["dteday"])
  hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
  return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Sidebar
st.sidebar.title("Bike Sharing Dashboard")

# Judul Dashboard
st.title("Dashboard Analisis Bike Sharing")

# Analisis Clustering
st.header("Penggunaan Sepeda Berdasarkan Jam")
rental_hour = hour_df.groupby("hr")["cnt"].mean()
low_threshold = rental_hour.quantile(0.33)
high_threshold = rental_hour.quantile(0.67)
rental_hour_cluster = rental_hour.apply(
  lambda x: "Low Usage" if x <= low_threshold else "High Usage" if x > high_threshold else "Medium Usage"
)

# Visualisasi Clustering
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=rental_hour.index, y=rental_hour.values, hue=rental_hour_cluster, dodge=False, palette="Set2", ax=ax1)
ax1.set_title("Clustering Jam Berdasarkan Penggunaan Sepeda", fontsize=16)
ax1.set_xlabel("Jam", fontsize=12)
ax1.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax1.legend(title="Cluster", loc="upper left")
st.pyplot(fig1)

# Analisis Tren Penyewaan
st.header("Tren Penyewaan Sepeda per Tahun")
rental_year = day_df.groupby("yr")["cnt"].sum()
increase = (rental_year[1] - rental_year[0]) / rental_year[0] * 100

# Tampilkan Hasil Analisis
st.write(f"**Jumlah total penyewaan di tahun 2011:** {rental_year[0]:,.0f}")
st.write(f"**Jumlah total penyewaan di tahun 2012:** {rental_year[1]:,.0f}")
st.write(f"**Perubahan jumlah penyewaan dari 2011 ke 2012:** {increase:.2f}%")

# Visualisasi  Penyewaan Sepeda per Tahun
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x=["2011", "2012"], y=rental_year.values, palette="Blues", ax=ax2)
ax2.set_title("Jumlah Total Penyewaan Sepeda per Tahun", fontsize=16)
ax2.set_xlabel("Tahun", fontsize=12)
ax2.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig2)

# Footer
st.sidebar.write("Dashboard dibuat menggunakan Streamlit.")
st.sidebar.write("@ 2024, Analisis Data Bike Sharing")