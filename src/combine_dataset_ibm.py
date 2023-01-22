import pandas as pd
import numpy as np
from tqdm import tqdm

# Script to combine the fire and weather dataset

df_weather = pd.read_csv('/data/capstone22/IBM/spot-challenge-wildfires/Nov_10/HistoricalWeather.csv')
df_fire = pd.read_csv('/data/capstone22/IBM/spot-challenge-wildfires/Nov_10/Historical_Wildfires.csv')
df_weather.info()
df_fire.info()

# #check that every date in fire is in weather
# weather_dates = df_weather.Date.unique()
# df_fire['Date'] = pd.to_datetime(df_fire.Date)
# df_fire['Date'] = df_fire['Date'].dt.strftime('%Y-%m-%d')
# fire_dates = df_fire.Date.unique()
# print(set(fire_dates) - set(weather_dates)) 

# create new weather columns in fire df
weather_columns = ['Precipitation', 'RelativeHumidity', 'SoilWaterContent', 'SolarRadiation', 'Temperature', 'WindSpeed']
stats = ['min()', 'max()', 'mean()', 'variance()']
for col in weather_columns:
    for stat in stats:
        df_fire[f'{col}_{stat}'] = np.nan
        
        
# Combine datasets
for index, fire_row in tqdm(df_fire.iterrows()):
    region, date = fire_row.Region, fire_row.Date
    weather_rows = df_weather.loc[(df_weather.Region == region) & (df_weather.Date == date)]
    for i, weather_row in weather_rows.iterrows():
        param = weather_row['Parameter']
        for stat in stats:
            col = f'{param}_{stat}'
            df_fire.loc[index, col] = weather_row[stat]
            
# # Save the new df as csv and pickle files
df_fire.to_csv('Fire_Weather.csv')
df_fire.to_pickle('Fire_Weather.pkl')
               