import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

print("#############################################################")
print("#                                                           #")
print("#                                                           #")
print("#                                                           #")
print("#                Data wragling                              #")
print("#                                                           #")
print("#                                                           #")
print("#                                                           #")
print("#############################################################")

# A. accessing data
print("A. accessing data")

bike_hour = pd.read_csv('data/hour.csv')

print(bike_hour.head())
print(bike_hour.info())

print("Describe data")
print(bike_hour.describe(include="all"))


print("#############################################################")
print("#                                                           #")
print("#                                                           #")
print("#                                                           #")
print("#                Exploratory Analysis & Visualisasi         #")
print("#                                                           #")
print("#                                                           #")
print("#                                                           #")
print("#############################################################")

# #Kategori: Pengguna dan Pola Penyewaan
print("\nQ1 -Pada musim apa jumlah pengguna sepeda tertinggi dan terendah terjadi?")
bike_hour_by_season = bike_hour.groupby(by="season").agg({
    "cnt": "sum",
})
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
bike_hour_by_season.index = bike_hour_by_season.index.map(season_labels)
bike_hour_by_season = bike_hour_by_season.sort_values(by="cnt", ascending=False)
print(bike_hour_by_season)

# Menentukan musim dengan pengguna tertinggi dan terendah
max_season = bike_hour_by_season["cnt"].idxmax()
min_season = bike_hour_by_season["cnt"].idxmin()
print(f"Musim dengan jumlah pengguna tertinggi: {max_season}")
print(f"Musim dengan jumlah pengguna terendah: {min_season}")

formatter = FuncFormatter(lambda x, _: f'{int(x):,}')  # Menambahkan koma s
plt.figure(figsize=(8,6))
bike_hour_by_season['cnt'].plot(kind='bar')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')  # Label diagonal dengan perataan kanan
plt.title('Jumlah Pengguna Sepeda Berdasarkan Musim', fontsize=16)
plt.xlabel('Musim', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.tight_layout()
plt.show()







print("\nQ2 - Bagaimana tren penggunaan sepeda dari tahun ke tahun, dan apakah terdapat peningkatan atau penurunan signifikan antar tahun?")
bike_hour_by_year = bike_hour.groupby(by="yr").agg({
    "cnt": "sum"
})
year_label = {0: "2011", 1: "2012"}
bike_hour_by_year.index = bike_hour_by_year.index.map(year_label)
print(bike_hour_by_year)

# Menghitung perubahan jumlah penyewaan
change = bike_hour_by_year["cnt"].pct_change().iloc[1] * 100
if change > 0:
    print(f"Terdapat peningkatan jumlah pengguna sepeda sebesar {change:.2f}% dari 2011 ke 2012.")
else:
    print(f"Terdapat penurunan jumlah pengguna sepeda sebesar {-change:.2f}% dari 2011 ke 2012.")

plt.figure(figsize=(7,7))
plt.pie(bike_hour_by_year['cnt'], labels=bike_hour_by_year.index, autopct='%1.1f%%', startangle=90)
plt.title('Perbandingan Jumlah Penyewaan Sepeda antara Tahun 2011 dan 2012', fontsize=16)
plt.axis('equal')
plt.show()






print("\nQ3 - Bagaimana perbandingan tingkat penyewaan sepeda antar bulan dalam satu tahun?")
# Memfilter data hanya untuk tahun 2012 (yr == 1)
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
print("Jumlah pengguna sepeda per bulan di tahun 2012:")
print(bike_hour_by_month_2012)

# Membuat line chart
plt.figure(figsize=(10,6))
plt.plot(bike_hour_by_month_2012["mnth"], bike_hour_by_month_2012["cnt"], marker='o', color='g', linestyle='-', linewidth=2, markersize=5)
plt.title('Jumlah Penyewaan Sepeda per Bulan di Tahun 2012', fontsize=16)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)  # Menambahkan rotasi untuk label bulan agar mudah dibaca
plt.tight_layout()
plt.show()







print("\n Q4 - Bagaimana pengaruh berbagai kondisi cuaca terhadap jumlah penyewaan sepeda, dan kondisi cuaca mana yang paling mendukung peningkatan penggunaan?")
# Menghitung korelasi antara kondisi cuaca dan jumlah penyewaan sepeda
correlation = bike_hour["weathersit"].corr(bike_hour["cnt"])
print(f"Korelasi antara kondisi cuaca (weathersit) dan jumlah penyewaan sepeda (cnt): {correlation:.2f}")

# Menghitung rata-rata penyewaan sepeda berdasarkan kondisi cuaca
avg_rentals_by_weather = bike_hour.groupby("weathersit").agg({
    "cnt": "mean"
}).reset_index()

# Memberi label pada kategori kondisi cuaca
weather_labels = {
    1: "Clear/Partly Cloudy",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

avg_rentals_by_weather["weathersit"] = avg_rentals_by_weather["weathersit"].map(weather_labels)
# Menampilkan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca
print("\nRata-rata penyewaan sepeda berdasarkan kondisi cuaca:")
print(avg_rentals_by_weather)
plt.figure(figsize=(10,6))
plt.bar(avg_rentals_by_weather["weathersit"], avg_rentals_by_weather["cnt"], color=['skyblue', 'orange', 'green', 'red'])

plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=16)
plt.xlabel('Kondisi Cuaca', fontsize=12)
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()







print("\n Q5 - Bagaimana perbandingan tingkat penyewaan sepeda antar hari")
# Kelompokkan data berdasarkan hari dalam seminggu (weekday) dan hitung jumlah penyewaan sepeda
bike_hour_by_day = bike_hour.groupby('weekday').agg({
    'cnt': 'sum'
})

# Menambahkan label hari untuk memudahkan interpretasi (0: Minggu, 1: Senin, ..., 6: Sabtu)
day_labels = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
bike_hour_by_day.index = bike_hour_by_day.index.map(day_labels)
print(bike_hour_by_day)
plt.figure(figsize=(10,6))
plt.bar(bike_hour_by_day.index, bike_hour_by_day['cnt'], color='skyblue')
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu', fontsize=16)
plt.xlabel('Hari dalam Seminggu', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()





print("\n Q6 - Bagaimana perbandingan tingkat penyewaan sepeda antara hari kerja (working day) dan hari non-kerja (non-working day)?")
# Kelompokkan data berdasarkan kolom 'workingday' (1 = hari kerja, 0 = non-hari kerja)
bike_hour_by_workingday = bike_hour.groupby('workingday').agg({
    'cnt': 'sum'
})

# Menambahkan label untuk lebih mudah memahami (1: Hari Kerja, 0: Non-Hari Kerja)
workingday_labels = {0: 'Non-Hari Kerja', 1: 'Hari Kerja'}
bike_hour_by_workingday.index = bike_hour_by_workingday.index.map(workingday_labels)
print(bike_hour_by_workingday)

# Membuat grafik pie chart
plt.figure(figsize=(7, 7))
plt.pie(bike_hour_by_workingday['cnt'], labels=bike_hour_by_workingday.index, autopct='%1.1f%%', colors=['#66b3ff','#99ff99'])
plt.title('Perbandingan Penyewaan Sepeda antara Hari Kerja dan Non-Hari Kerja', fontsize=16)
plt.tight_layout()
plt.show()






print("\n Q7 - Bagaimana perbandingan pola penggunaan sepeda antara pengguna kasual dan pengguna terdaftar?")
# Menghitung jumlah penyewaan sepeda untuk pengguna kasual dan terdaftar
bike_hour_by_user_type = bike_hour[['casual', 'registered', 'cnt']].agg({
    'casual': 'sum',     # Total penyewaan oleh pengguna kasual
    'registered': 'sum'  # Total penyewaan oleh pengguna terdaftar
})

# Membuat DataFrame yang lebih mudah dibaca
bike_hour_by_user_type = bike_hour_by_user_type.reset_index()
bike_hour_by_user_type.columns = ['User_Type', 'Total_Rentals']

# Mengubah nilai kolom User_Type untuk label yang lebih jelas
bike_hour_by_user_type['User_Type'] = bike_hour_by_user_type['User_Type'].map({
    'casual': 'Pengguna Kasual',
    'registered': 'Pengguna Terdaftar'
})
print(bike_hour_by_user_type)

# Membuat grafik pie chart
plt.figure(figsize=(7, 7))
plt.pie(bike_hour_by_user_type['Total_Rentals'], labels=bike_hour_by_user_type['User_Type'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
plt.title('Perbandingan Penyewaan Sepeda antara Pengguna Kasual dan Pengguna Terdaftar', fontsize=16)
plt.tight_layout()
plt.show()



print("\nQ8 - Bagaimana pola penggunaan sepeda pada berbagai jam dalam sehari, dan jam berapa saja yang menunjukkan puncak penggunaan?")

bike_hour_by_hour = bike_hour.groupby(by="hr").agg({
    "cnt": "sum"
})
print(bike_hour_by_hour)

# Menentukan jam puncak dan terendah
peak_hour = bike_hour_by_hour["cnt"].idxmax()
low_hour = bike_hour_by_hour["cnt"].idxmin()
print(f"Jam dengan jumlah pengguna tertinggi: {peak_hour}:00")
print(f"Jam dengan jumlah pengguna terendah: {low_hour}:00")

plt.figure(figsize=(10,6))
plt.plot(bike_hour_by_hour.index, bike_hour_by_hour['cnt'], marker='o', color='b', linestyle='-', linewidth=2, markersize=5)
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Jam', fontsize=16)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
plt.xticks(ticks=range(0, 24), labels=range(0, 24))
plt.grid(True)
plt.tight_layout()
plt.show()


kesimpulan :
- data peminjaman tertinggi ada di musim panas ( Fall ) dan terendah ada di munsim semi ( Spring )
- Terdapat peningkatan jumlah pengguna sepeda sebesar 64.88% dari 2011 ke 2012.
- pada tahun 2012 berdasarkan bulan jumlah peminjaman tertinggi berada di bulan september dan terendah ada di bulan januari
- jumlah peminjaman terbanyak terjadi pada cuaca cerah dan jumlah peminjaman terkecil pada cuaca hujan/berawan
- jumlah peminjaman jika di total untuk setiap harinya relative sama, dan yan tertinggi ada pada hari jumat
- jumlah peminjaman pada hari kerja lebih tinggi dari non hari kerja
- jumlah peminjaman oleh pengguna terdaftar lebih banyak dari pengguna kasual
- berdasarkan jam, total jumlah peminjaman tertinggi berada pada jam 17 dan terendah pada jam 4 