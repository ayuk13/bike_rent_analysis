import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Melakukan impor data
day_df = pd.read_csv('day.csv')
day_df.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['instant', 'hum', 'windspeed']

for i in day_df.columns:
    if i in drop_col:
        day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

day_df['month']= day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
}) 

day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Membuat fungsi untuk menampilkan jumlah penyewa sepeda harian
# Menyiapkan create_daily_count_rent
def create_daily_count_rent(df):
    daily_count_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_count_rent_df

# Menyiapkan create_daily_casual_rent
def create_daily_casual_rent(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan create_daily_reg_rent
def create_daily_reg_rent(df):
    daily_reg_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_reg_rent_df

# Menyiapkan create_weekday_rent
def create_weekday_rent(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan create_monthly_rent
def create_monthly_rent(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })

    monthly_rent_df = monthly_rent_df.reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fill_value=0)
    return monthly_rent_df

#Menyiapkan create_season_rent
def create_season_rent(df):
    season_rent_df = df.groupby(by='season').agg({
        'casual': 'sum',
        'registered': 'sum',
    }).reset_index()
    return season_rent_df

# Menyiapkan create_workingday_rent
def create_workingday_rent(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan create_holiday_rent
def create_holiday_rent(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan create_weather_rent
def create_weather_rent(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df


min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    # Menambahkan logo bisnis
    st.image("https://i.pinimg.com/280x280_RS/3b/ed/3c/3bed3c85cb285b41f24c3f5d6cd44d7e.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dateday"] >= str(start_date)) & 
                (day_df["dateday"] <= str(end_date))]

# Menampilkan berbagai dataframe
daily_count_rent_df = create_daily_count_rent(main_df)
daily_casual_rent_df = create_daily_casual_rent(main_df)
daily_registered_rent_df = create_daily_reg_rent(main_df)
weekday_rent_df = create_weekday_rent(main_df)
season_rent_df = create_season_rent(main_df)
monthly_rent_df = create_monthly_rent(main_df)
workingday_rent_df = create_workingday_rent(main_df)
holiday_rent_df = create_holiday_rent(main_df)
weather_rent_df = create_weather_rent(main_df)

# Membuat dashboard

# Menampilkan header
st.header('Bike Rent Dashboard :sparkles:')

# Penyewaan sepeda harian (daily)
st.subheader('Daily Rental')
 
col1, col2, col3 = st.columns(3)
with col1:
    total_count_rent = daily_count_rent_df['count'].sum()
    st.metric("Total user", value=total_count_rent)
 
with col2:
    total_casual_rent = daily_casual_rent_df['casual'].sum()
    st.metric("Casual user", value=total_casual_rent)

with col3:
    total_registered_rent = daily_registered_rent_df['registered'].sum()
    st.metric("Registered user", value=total_registered_rent)

# Penyewaan sepeda bulanan (monthly)
st.subheader('Monthly Rental')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:orange'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Penyewaan sepeda berdasarkan musim (season)
st.subheader('Seasonal Rental')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:green',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=15)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=15)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# Penyewaan sepeda berdasarkan musim (Weather)
st.subheader('Weatherly Rental')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    data=weather_rent_df,
    palette=['tab:blue', 'tab:orange', 'tab:green'],
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)



# Penyewaan sepeda berdasarkan working day, weekday, dan holiday
st.subheader('Working day, Weekday, and Holiday Rental')
col1, col2 = st.columns(2)
colors_1=["tab:blue", "tab:green"]
colors_2=["tab:blue", "tab:green", "tab:orange", "tab:red", "tab:brown", "tab:pink", "tab:purple"]


fig, ax = plt.subplots(figsize=(20,10))
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors_2,
    ax=ax
)

for index, row in enumerate(weekday_rent_df['count']):
        ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Number rent on weekday", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        x='holiday',
        y='count',
        data=holiday_rent_df,
        palette=colors_1,
        ax=ax
    )

    for index, row in enumerate(holiday_rent_df['count']):
        ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Number rent on holiday", loc="center", fontsize=30)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        x='workingday',
        y='count',
        data=workingday_rent_df,
        palette=colors_1,
        ax=ax
    )

    for index, row in enumerate(workingday_rent_df['count']):
        ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=15)

    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Number rent on working day", loc="center", fontsize=30)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

st.caption('Copyright (c) Ayu Kirana 2023')






