import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.header('Bike Sharing Dashboard :sparkles:')


st.subheader('Q1 - Pada musim apa jumlah pengguna sepeda tertinggi dan terendah terjadi?')
bike_hour = pd.read_csv('data/hour.csv')
bike_hour_by_season = bike_hour.groupby(by="season").agg({
    "cnt": "sum",
})

season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
bike_hour_by_season.index = bike_hour_by_season.index.map(season_labels)
bike_hour_by_season = bike_hour_by_season.sort_values(by="cnt", ascending=False)

max_season = bike_hour_by_season["cnt"].idxmax()
min_season = bike_hour_by_season["cnt"].idxmin()

st.write("Musim dengan jumlah pengguna sepeda tertinggi adalah **{}**.".format(max_season))
st.write("Musim dengan jumlah pengguna sepeda terendah adalah **{}**.".format(min_season))
st.dataframe(bike_hour_by_season)

fig, ax = plt.subplots(figsize=(8, 6))
bike_hour_by_season['cnt'].plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Jumlah Pengguna Sepeda Berdasarkan Musim', fontsize=16)
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))  # Menampilkan angka dengan format ribuan
plt.xticks(rotation=45, ha='right')  # Label sumbu x diagonal
plt.tight_layout()
st.pyplot(fig)





st.subheader('Q2 - Bagaimana tren penggunaan sepeda dari tahun ke tahun, dan apakah terdapat peningkatan atau penurunan signifikan antar tahun?')
bike_hour_by_year = bike_hour.groupby(by="yr").agg({
    "cnt": "sum"
})
year_label = {0: "2011", 1: "2012"}
bike_hour_by_year.index = bike_hour_by_year.index.map(year_label)
st.dataframe(bike_hour_by_year)
change = bike_hour_by_year["cnt"].pct_change().iloc[1] * 100
if change > 0:
    st.write(f"Terdapat peningkatan jumlah pengguna sepeda sebesar **{change:.2f}%** dari 2011 ke 2012.")
else:
    st.write(f"Terdapat penurunan jumlah pengguna sepeda sebesar **{-change:.2f}%** dari 2011 ke 2012.")

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(
    bike_hour_by_year['cnt'], 
    labels=bike_hour_by_year.index, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=['skyblue', 'lightcoral']
)
ax.set_title('Perbandingan Jumlah Penyewaan Sepeda antara Tahun 2011 dan 2012', fontsize=16)
ax.axis('equal')  # Menjaga bentuk pie tetap bulat
st.pyplot(fig)




st.subheader('Q3 - Bagaimana perbandingan tingkat penyewaan sepeda antar bulan dalam satu tahun?')
bike_hour_2012 = bike_hour[bike_hour["yr"] == 1]
bike_hour_by_month_2012 = bike_hour_2012.groupby(by="mnth").agg({
    "cnt": "sum"
}).reset_index()
month_labels = {
    1: "January", 2: "February", 3: "March", 4: "April", 
    5: "May", 6: "June", 7: "July", 8: "August", 
    9: "September", 10: "October", 11: "November", 12: "December"
}
bike_hour_by_month_2012["mnth"] = bike_hour_by_month_2012["mnth"].map(month_labels)
max_month = bike_hour_by_month_2012.loc[bike_hour_by_month_2012["cnt"].idxmax()]
min_month = bike_hour_by_month_2012.loc[bike_hour_by_month_2012["cnt"].idxmin()]
st.dataframe(bike_hour_by_month_2012.rename(columns={"mnth": "Bulan", "cnt": "Jumlah Penyewaan"}))
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    bike_hour_by_month_2012["mnth"], 
    bike_hour_by_month_2012["cnt"], 
    marker='o', 
    color='g', 
    linestyle='-', 
    linewidth=2, 
    markersize=5
)
ax.set_title('Jumlah Penyewaan Sepeda per Bulan di Tahun 2012', fontsize=16)
ax.set_xlabel('Bulan', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
ax.grid(True)
plt.xticks(rotation=45)  # Menambahkan rotasi untuk label bulan agar mudah dibaca
plt.tight_layout()
st.pyplot(fig)
st.subheader('Kesimpulan:')
st.write(
    f"Pada tahun 2012, jumlah peminjaman tertinggi berada di bulan **{max_month['mnth']}** "
    f"dengan total peminjaman sebanyak **{int(max_month['cnt']):,}**. "
    f"Sebaliknya, jumlah peminjaman terendah terjadi di bulan **{min_month['mnth']}** "
    f"dengan total peminjaman sebanyak **{int(min_month['cnt']):,}**."
)





st.subheader(
    'Q4 - Bagaimana pengaruh berbagai kondisi cuaca terhadap jumlah penyewaan sepeda, dan kondisi cuaca mana yang paling mendukung peningkatan penggunaan?'
)
correlation = bike_hour["weathersit"].corr(bike_hour["cnt"])
avg_rentals_by_weather = bike_hour.groupby("weathersit").agg({
    "cnt": "mean"
}).reset_index()
weather_labels = {
    1: "Clear/Partly Cloudy",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}
avg_rentals_by_weather["weathersit"] = avg_rentals_by_weather["weathersit"].map(weather_labels)
max_weather = avg_rentals_by_weather.loc[avg_rentals_by_weather["cnt"].idxmax()]
min_weather = avg_rentals_by_weather.loc[avg_rentals_by_weather["cnt"].idxmin()]
st.dataframe(avg_rentals_by_weather.rename(columns={
    "weathersit": "Kondisi Cuaca",
    "cnt": "Rata-rata Penyewaan"
}))
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(
    avg_rentals_by_weather["weathersit"],
    avg_rentals_by_weather["cnt"],
    color=['skyblue', 'orange', 'green', 'red']
)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=12)
ax.set_xticks(range(len(avg_rentals_by_weather["weathersit"])))
ax.set_xticklabels(avg_rentals_by_weather["weathersit"], rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)
st.subheader('Kesimpulan:')
st.write(
    f"Korelasi antara kondisi cuaca dengan jumlah penyewaan sepeda adalah **{correlation:.2f}**, "
    f"yang menunjukkan {'korelasi negatif' if correlation < 0 else 'korelasi positif'}. "
    f"Kondisi cuaca yang paling mendukung peningkatan jumlah pengguna adalah **{max_weather['weathersit']}**, "
    f"dengan rata-rata penyewaan sebanyak **{max_weather['cnt']:.2f}**. "
    f"Sebaliknya, kondisi cuaca yang paling tidak mendukung adalah **{min_weather['weathersit']}**, "
    f"dengan rata-rata penyewaan sebanyak **{min_weather['cnt']:.2f}**."
)






st.subheader(
    'Q5 - Bagaimana perbandingan tingkat penyewaan sepeda antar hari dalam seminggu?'
)
bike_hour_by_day = bike_hour.groupby('weekday').agg({
    'cnt': 'sum'
})
day_labels = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
bike_hour_by_day.index = bike_hour_by_day.index.map(day_labels)
max_day = bike_hour_by_day['cnt'].idxmax()
min_day = bike_hour_by_day['cnt'].idxmin()
max_rentals = bike_hour_by_day.loc[max_day, 'cnt']
min_rentals = bike_hour_by_day.loc[min_day, 'cnt']
st.dataframe(bike_hour_by_day.rename(columns={'cnt': 'Jumlah Penyewaan'}))
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(
    bike_hour_by_day.index,
    bike_hour_by_day['cnt'],
    color='skyblue'
)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', fontsize=16)
ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)
st.subheader('Kesimpulan:')
st.write(
    f"Hari dengan jumlah penyewaan sepeda tertinggi adalah **{max_day}**, "
    f"dengan total penyewaan sebanyak **{max_rentals:,}**. "
    f"Sebaliknya, hari dengan jumlah penyewaan sepeda terendah adalah **{min_day}**, "
    f"dengan total penyewaan sebanyak **{min_rentals:,}**."
)






st.subheader(
    'Q6 - Bagaimana perbandingan tingkat penyewaan sepeda antara hari kerja dan hari non-kerja?'
)
bike_hour_by_workingday = bike_hour.groupby('workingday').agg({
    'cnt': 'sum'
})
workingday_labels = {0: 'Non-Hari Kerja', 1: 'Hari Kerja'}
bike_hour_by_workingday.index = bike_hour_by_workingday.index.map(workingday_labels)
max_day_type = bike_hour_by_workingday['cnt'].idxmax()
min_day_type = bike_hour_by_workingday['cnt'].idxmin()
max_rentals = bike_hour_by_workingday.loc[max_day_type, 'cnt']
min_rentals = bike_hour_by_workingday.loc[min_day_type, 'cnt']
st.dataframe(bike_hour_by_workingday.rename(columns={'cnt': 'Jumlah Penyewaan'}))
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(
    bike_hour_by_workingday['cnt'],
    labels=bike_hour_by_workingday.index,
    autopct='%1.1f%%',
    colors=['#66b3ff', '#99ff99'],
    startangle=90
)
ax.set_title(
    'Perbandingan Penyewaan Sepeda antara Hari Kerja dan Non-Hari Kerja', fontsize=16
)
st.pyplot(fig)
st.subheader('Kesimpulan:')
st.write(
    f"Kategori dengan jumlah penyewaan sepeda tertinggi adalah **{max_day_type}**, "
    f"dengan total penyewaan sebanyak **{max_rentals:,}**. "
    f"Sebaliknya, kategori dengan jumlah penyewaan sepeda terendah adalah **{min_day_type}**, "
    f"dengan total penyewaan sebanyak **{min_rentals:,}**."
)





st.subheader('Q7 - Bagaimana perbandingan pola penggunaan sepeda antara pengguna kasual dan pengguna terdaftar?')
bike_hour_by_user_type = bike_hour[['casual', 'registered', 'cnt']].agg({
    'casual': 'sum',     # Total penyewaan oleh pengguna kasual
    'registered': 'sum'  # Total penyewaan oleh pengguna terdaftar
})
bike_hour_by_user_type = bike_hour_by_user_type.reset_index()
bike_hour_by_user_type.columns = ['User_Type', 'Total_Rentals']
bike_hour_by_user_type['User_Type'] = bike_hour_by_user_type['User_Type'].map({
    'casual': 'Pengguna Kasual',
    'registered': 'Pengguna Terdaftar'
})
st.dataframe(bike_hour_by_user_type)
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(
    bike_hour_by_user_type['Total_Rentals'],
    labels=bike_hour_by_user_type['User_Type'],
    autopct='%1.1f%%',
    colors=['#ff9999', '#66b3ff'],
    startangle=90
)
ax.set_title('Perbandingan Penyewaan Sepeda antara Pengguna Kasual dan Pengguna Terdaftar', fontsize=16)
st.pyplot(fig)
st.subheader('Kesimpulan:')
casual_rentals = bike_hour_by_user_type[bike_hour_by_user_type['User_Type'] == 'Pengguna Kasual']['Total_Rentals'].values[0]
registered_rentals = bike_hour_by_user_type[bike_hour_by_user_type['User_Type'] == 'Pengguna Terdaftar']['Total_Rentals'].values[0]
st.write(
    f"Jumlah total penyewaan sepeda oleh **Pengguna Kasual** adalah **{casual_rentals:,}**, "
    f"sedangkan jumlah total penyewaan sepeda oleh **Pengguna Terdaftar** adalah **{registered_rentals:,}**."
)





st.subheader('Q8 - Bagaimana pola penggunaan sepeda pada berbagai jam dalam sehari, dan jam berapa saja yang menunjukkan puncak penggunaan?')
bike_hour_by_hour = bike_hour.groupby(by="hr").agg({
    "cnt": "sum"
})
st.dataframe(bike_hour_by_hour)
peak_hour = bike_hour_by_hour["cnt"].idxmax()
low_hour = bike_hour_by_hour["cnt"].idxmin()
st.write(f"Jam dengan jumlah pengguna tertinggi: {peak_hour}:00")
st.write(f"Jam dengan jumlah pengguna terendah: {low_hour}:00")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    bike_hour_by_hour.index, 
    bike_hour_by_hour['cnt'], 
    marker='o', color='b', linestyle='-', linewidth=2, markersize=5
)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Jam', fontsize=16)
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
ax.set_xticks(range(0, 24))  # Menampilkan label jam dari 0-23
ax.set_xticklabels(range(0, 24))
ax.grid(True)
st.pyplot(fig)
st.subheader('Kesimpulan:')
st.write(f"Jam dengan jumlah pengguna sepeda tertinggi adalah jam **{peak_hour}:00**, "
         f"sedangkan jam dengan jumlah pengguna sepeda terendah adalah jam **{low_hour}:00**.")
if peak_hour >= 6 and peak_hour <= 9:
    st.write("Puncak penggunaan sepeda terjadi pada jam pagi hari, kemungkinan besar terkait dengan jam kerja atau aktivitas pagi.")
elif peak_hour >= 17 and peak_hour <= 19:
    st.write("Puncak penggunaan sepeda terjadi pada jam sore hari, kemungkinan besar terkait dengan pulang kerja atau aktivitas sore.")
else:
    st.write("Puncak penggunaan sepeda terjadi di luar jam kerja, mungkin berkaitan dengan aktivitas lain seperti olahraga atau rekreasi.")








# Memuat data (asumsi data sudah ada dalam bike_hour)
def time_based_cluster(hour):
    if 6 <= hour <= 11:
        return 'Pagi'
    elif 12 <= hour <= 17:
        return 'Siang'
    elif 18 <= hour <= 23:
        return 'Sore/Malam'
    else:
        return 'Dini Hari'
bike_hour['time_cluster'] = bike_hour['hr'].apply(time_based_cluster)
bike_hour_by_time_cluster = bike_hour.groupby('time_cluster').agg({
    'cnt': 'sum'
}).reset_index()
time_order = ['Dini Hari', 'Pagi', 'Siang', 'Sore/Malam']
bike_hour_by_time_cluster['time_cluster'] = pd.Categorical(
    bike_hour_by_time_cluster['time_cluster'], categories=time_order, ordered=True
)
bike_hour_by_time_cluster = bike_hour_by_time_cluster.sort_values('time_cluster')
st.subheader('Q8 - Bagaimana pola penggunaan sepeda berdasarkan cluster waktu?')
st.dataframe(bike_hour_by_time_cluster)
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(bike_hour_by_time_cluster['time_cluster'], bike_hour_by_time_cluster['cnt'], color='skyblue')
ax.set_title('Jumlah Penggunaan Sepeda Berdasarkan Cluster Waktu', fontsize=16)
ax.set_xlabel('Cluster Waktu', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
ax.set_xticks(range(len(bike_hour_by_time_cluster['time_cluster'])))
ax.set_xticklabels(bike_hour_by_time_cluster['time_cluster'])
plt.tight_layout()
st.pyplot(fig)
st.subheader('Kesimpulan:')
total_rentals = bike_hour_by_time_cluster['cnt'].sum()
peak_cluster = bike_hour_by_time_cluster.iloc[bike_hour_by_time_cluster['cnt'].idxmax()]
low_cluster = bike_hour_by_time_cluster.iloc[bike_hour_by_time_cluster['cnt'].idxmin()]
st.write(f"Jumlah penyewaan sepeda terbanyak terjadi pada cluster waktu **{peak_cluster['time_cluster']}** "
         f" dengan total penyewaan sebanyak **{peak_cluster['cnt']}**.")
st.write(f"Sementara itu, jumlah penyewaan sepeda terendah terjadi pada cluster waktu **{low_cluster['time_cluster']}** "
         f" dengan total penyewaan sebanyak **{low_cluster['cnt']}**.")
if peak_cluster['time_cluster'] == 'Pagi':
    st.write("Puncak penggunaan sepeda terjadi pada pagi hari, yang kemungkinan berkaitan dengan aktivitas kerja atau sekolah.")
elif peak_cluster['time_cluster'] == 'Siang':
    st.write("Puncak penggunaan sepeda terjadi pada siang hari, kemungkinan besar berkaitan dengan jam istirahat atau kegiatan luar ruangan.")
elif peak_cluster['time_cluster'] == 'Sore/Malam':
    st.write("Puncak penggunaan sepeda terjadi pada sore atau malam hari, mungkin berkaitan dengan waktu pulang kerja atau aktivitas rekreasi.")
else:
    st.write("Puncak penggunaan sepeda terjadi pada dini hari, kemungkinan besar berhubungan dengan kegiatan olahraga atau transportasi untuk pekerja malam.")