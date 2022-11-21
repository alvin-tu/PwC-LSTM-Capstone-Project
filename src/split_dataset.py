import pandas as pd
import numpy as np
from tqdm import tqdm

# Load in csv file w/ fire and weather data
df_fire = pd.read_csv('/data/capstone22/IBM/spot-challenge-wildfires/Nov_10/Fire_Weather.csv')
df_fire = df_fire.drop(columns=['Unnamed: 0'])

# Unique regions & their counts
np.unique(df_fire.Region, return_counts=True)

# Split the dataset for test
test_perc = 0.2
df_train = pd.DataFrame(columns=df_fire.columns)
df_test = pd.DataFrame(columns=df_fire.columns)
# need to use * to deference because np.unique returns a list of two arrays instead of two separate arrays
for region, count in zip(*np.unique(df_fire.Region, return_counts=True)):
    # get rows belonging to region
    region_rows = df_fire.loc[df_fire.Region == region]
    region_rows = region_rows.sort_values(by='Date', ascending=True)
    
    # split into train and test dataset
    train_rows = region_rows.iloc[:-int(count*test_perc)]
    test_rows = region_rows.iloc[-int(count*test_perc):]
    
    # join the train and test rows to the train and test dataframes
    df_train = pd.concat([df_train, train_rows], ignore_index=True)
    df_test = pd.concat([df_test, test_rows], ignore_index=True)

print(df_fire.shape)
print(df_train.shape)
print(df_test.shape)
print(df_train.shape[0] + df_test.shape[0] == df_fire.shape[0])

# Save the df as csv files 

df_train.to_csv('Fire_Weather_train.csv')
df_test.to_csv('Fire_Weather_test.csv')
