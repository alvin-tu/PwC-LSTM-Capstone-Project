from __future__ import print_function
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib
import seaborn
import sklearn
from sklearn import metrics
from sklearn.utils.multiclass import unique_labels

import csv


def get_average(file):
    file_names = os.path.basename(file).split('.')[0].split('_')
    pred = file_names[0]
    model_name = file_names[1:-1]
    month = file_names[-1]

    with open(file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    # Create a dictionary to hold unique [latitude, longitude] values
    unique_values = {}

    # Loop through data and add prediction values to unique_values dictionary
    for row in data:
        key = (row['latitude'], row['longitude'])
        value = float(row['value'])
        if key in unique_values:
            unique_values[key].append(value)
        else:
            unique_values[key] = [value]

    # Create a new list of dictionaries with unique [latitude, longitude] values and average prediction values
    new_data = []
    for key, values in unique_values.items():
        new_data.append({'latitude': key[0], 'longitude': key[1], 'value': sum(values) / len(values)})

    # Write new data to CSV file
    with open(f'./results/results_averaged/averaged_{pred}_{"_".join(model_name)}_{month}.csv', 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_data:
            writer.writerow(row)


csv_folder = '/home/capstone22/WildFIrePrediction/agni/evaluation_scripts/results'
models = ['model_cali', 'model_cali_3month', 'model_cali_6month', 'model_cali_9month']
months = ['01', '03', '06', '08', '10', '11']

for model in models:
    for month in months:
        pred_csv = os.path.join(csv_folder, f'prediction_{model}_{month}.csv')
        gt_csv = os.path.join(csv_folder, f'gt_{model}_{month}.csv')
        get_average(pred_csv)
        get_average(gt_csv)



