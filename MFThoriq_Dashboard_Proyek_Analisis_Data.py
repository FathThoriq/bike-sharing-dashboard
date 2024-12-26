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
st.sidebar.write("**Filter berdasarkan kategori:**")
category = st.sidebar.radio(
  "Pilih kategori:",
  options=["casual", "registered", "cnt"],
  index=2 # Default "cnt"
)

# Judul Dashboard
st.title("Dashboard Analisis Bike Sharing")

# Analisis Clustering
st.header("Penggunaan Sepeda Berdasarkan Jam")
rental_hour = hour_df.groupby("hr")[category].mean()
low_threshold = rental_hour.quantile(0.33)
high_threshold = rental_hour.quantile(0.67)
rental_hour_cluster = rental_hour.apply(
  lambda x: "Low Usage" if x <= low_threshold else "High Usage" if x > high_threshold else "Medium Usage"
)

# Visualisasi Clustering
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=rental_hour.index, y=rental_hour.values, hue=rental_hour_cluster, dodge=False, palette="Set2", ax=ax1)
ax1.set_title(f"Clustering Jam Berdasarkan Penggunaan Sepeda ({category.capitalize()})", fontsize=16)
ax1.set_xlabel("Jam", fontsize=12)
ax1.set_ylabel(f"Rata-rata Penyewaan ({category.capitalize()})", fontsize=12)
ax1.legend(title="Cluster", loc="upper left")
st.pyplot(fig1)

# Analisis Total Penyewaan
st.header(f"Jumlah Total Penyewaan Sepeda ({category.capitalize()}) per Tahun")
rental_year = day_df.groupby(day_df["dteday"].dt.year)[category].sum()

# Tampilkan Hasil Analisis
st.write(f"**Jumlah total penyewaan ({category.capitalize()}) di tahun 2011:** {rental_year[2011]:,.0f}")
st.write(f"**Jumlah total penyewaan ({category.capitalize()}) di tahun 2012:** {rental_year[2012]:,.0f}")
increase = (rental_year[2012] - rental_year[2011]) / rental_year[2011] * 100
st.write(f"**Perubahan jumlah penyewaan ({category.capitalize()}) dari 2011 ke 2012:** {increase:.2f}%")

# Visualisasi  Penyewaan Sepeda per Tahun
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(x=["2011", "2012"], y=rental_year.values, palette="Blues", ax=ax2)
ax2.set_title(f"Jumlah Total Penyewaan Sepeda ({category.capitalize()}) per Tahun", fontsize=16)
ax2.set_xlabel("Tahun", fontsize=12)
ax2.set_ylabel(f"Jumlah Penyewaan ({category.capitalize()})", fontsize=12)
st.pyplot(fig2)

# Footer
st.sidebar.write("Dashboard dibuat menggunakan Streamlit.")
st.sidebar.write("@ 2024, Analisis Data Bike Sharing")
