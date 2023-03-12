from __future__ import print_function

import os
import datetime
import sys
import time
import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt
import pickle
import copy
import random
import tensorflow.keras.backend as K
from numpy.core import multiarray
from collections import deque

import datetime

from tqdm import tqdm

import argparse

import csv

# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument('--model', dest='model')
parser.add_argument('--eval_path', dest='eval_path')
args = parser.parse_args()

#######################
# USER SET PARAMETERS
#######################

MODEL_DIR = '/home/capstone22/WildFIrePrediction/agni/models/cali_models/'

model_name = args.model.split('.')[0]
model_to_len = {
    'model_cali_3month': 6,
    'model_cali_6month': 12,
    'model_cali_9month': 18,
}
month = args.eval_path.split('/')[-2]

model_filename = os.path.join(MODEL_DIR, args.model)
eval_set_log_filename = f'./logs/{model_name}_{month}.txt'
eval_set_directory = args.eval_path
prediction_output_file = f'./results/{model_name}_{month}.pickle'
COORD_INFO_FILE = f'/home/capstone22/WildFIrePrediction/agni/cali_data/evaluation_data/coordinates_{month}.csv'

#######################

# set up GPU -------------------------------------------------------------------
gpus = tf.config.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)
# -------------------------------------------------------------------

model_file = model_filename

# load csv file with coordinate information
with open(COORD_INFO_FILE, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    file_to_coords = {row[0]: [float(coord) for coord in row[1:]] for row in reader}

# print(file_to_coords)

# defining custom loss function
def custom_loss(y_true,y_pred):
    # mean abs error implementation from keras
#     mae_tensor = K.mean(K.abs(y_pred - y_true), axis=-1)
    # +ve means real more than predicted, penalize
    # -ve means predicted more than real, normal loss
    diff_tensor = y_true - y_pred
    
    exponential_tensor = K.exp(diff_tensor * 100.0 / 30.0)
#     exponential_tensor = K.exp(diff_tensor * 100.0 / 20.0)
#     exponential_tensor = K.exp(diff_tensor * 100.0 / 11.0)
    exponential_tensor = K.clip(exponential_tensor, min_value=1.0, max_value=10000.0)
    abs_tensor = K.abs(diff_tensor)
    output_tensor = K.mean(abs_tensor * exponential_tensor)
#     clipped_tensor = K.clip(exponential_tensor, 1.0, 10000.0)
    return output_tensor

net = tf.keras.models.load_model(model_file, custom_objects={'custom_loss':custom_loss})

# test_dataset_dir = './preprocessed_data_2018_test_set/'
# test_dataset_dir = './preprocessed_data_2019_july_with_aug_fire_test/'
test_dataset_dir = eval_set_directory

testset_filename_list = os.listdir(test_dataset_dir)

testset_filepath_list = [test_dataset_dir + x for x in testset_filename_list]
testset_length = len(testset_filename_list)

def parse_input_data_function(filename):
    histogram_data, label = pickle.load(open(filename, 'rb'))
    histogram_data = histogram_data.transpose(1, 0)
    histogram_data = histogram_data.reshape([-1, 8, 32, 1])
    histogram_data = histogram_data[::-1, :, :, :]
    histogram_data = histogram_data.reshape([1, -1, 8, 32, 1])
#     data = tf.convert_to_tensor(histogram_data, dtype=tf.float32)
#     label = tf.convert_to_tensor(label, dtype=tf.float32)
    label = np.array(float(label) / 100.0)
    label = label.reshape(1, 1)
    return histogram_data.astype('float32'), label

def parse_input_data(filenames):
    min_length = np.inf
    datas, labels = [], []
    for filename in filenames:
        histogram_data, label = pickle.load(open(filename, 'rb'))
        histogram_data = histogram_data.transpose(1, 0)
        histogram_data = histogram_data.reshape([-1, 8, 32, 1])

        length = histogram_data.shape[0]
        min_length = min(length, min_length)

        datas.append(histogram_data)

        label = np.array(float(label) / 100.0)
        label = label.reshape(1, 1)
        labels.append(label)

    if model_name != 'model_cali' and min_length > model_to_len[model_name]:
        min_length = model_to_len[model_name]

    #truncate to min_length
    for i, data in enumerate(datas):
        data = data[:min_length, :, :, :]
        data = data[::-1, :, :, :].astype('float32')
        datas[i] = data

    #stack
    return np.stack(datas), labels

real_label = []
model_prediction = []
all_coordinates = []

batch_size = 64


for i in tqdm(range(0, testset_length, batch_size)):
    if testset_length - 0 < batch_size:
        current_files = testset_filepath_list[i:]
        coordinates = [file_to_coords[os.path.basename(file)] for file in current_files]

        input_datas, labels = parse_input_data(current_files)
    else:
        current_files = testset_filepath_list[i : i + batch_size]
        # print(current_files)
        # print(current_files[0])
        # print(os.path.basename(current_files[0]))
        coordinates = [file_to_coords[os.path.basename(file)] for file in current_files]

        input_datas, labels = parse_input_data(current_files)

    real_label.extend(labels)

    prediction = net.predict(input_datas)
    model_prediction.extend(prediction)
    all_coordinates.extend(coordinates)

# for i in range(testset_length):
#     current_file = testset_filepath_list[i]
#     input_data, label = parse_input_data_function(current_file)
#     real_label.append(label)
#     prediction = net.predict(input_data)
#     model_prediction.append(prediction[0])

# record prediction w/ coordinate information in a csv file ------------------------------------------------------------------------------------------------------

# results_folder = f'./results/{model_name}_{month}/'
# if not os.path.exists(results_folder):
#     os.makedirs(results_folder)

results_file_name = f'./results/prediction_{model_name}_{month}.csv'
file_exists = os.path.exists(results_file_name)  

header = ['latitude', 'longitude', 'value']

with open(results_file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header) 

    if not file_exists:
        writer.writeheader() 

    for i in range(len(model_prediction)):
        writer.writerow({'latitude': all_coordinates[i][0], 'longitude': all_coordinates[i][1], 'value': model_prediction[i][0]})
    
    csvfile.close()

gt_file_name = f'./results/gt_{model_name}_{month}.csv'
file_exists = os.path.exists(gt_file_name)  

with open(gt_file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header) 

    if not file_exists:
        writer.writeheader() 

    for i in range(len(real_label)):
        writer.writerow({'latitude': all_coordinates[i][0], 'longitude': all_coordinates[i][1], 'value': real_label[i][0][0]})
    
    csvfile.close()

# convert csv to json
# with open(f'{results_file_name}.csv', 'r', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     data = [row for row in reader]

# with open(f'{results_file_name}.json', 'w') as jsonfile:
#     json.dump(data, jsonfile)

# ------------------------------------------------------------------------------------------------------

# prediction_array = np.array(model_prediction)
# test_label_array = np.array(real_label)
# test_label_array = test_label_array.reshape(-1, 1)

# pickle.dump((model_prediction, real_label), open(prediction_output_file, 'wb'))

# diff_array = test_label_array - prediction_array

# log_file = open(eval_set_log_filename, 'a+')

# log_file.write('Total number of instances in test set : ' + str(len(test_label_array)) + '\n')
# log_file.write('Number of fire in test set : ' + str(len(test_label_array[test_label_array > 0])) + '\n')

# # we are considering > 50% = fire
# log_file.write('True positive number(fire and predicted fire) : ' + str(sum(prediction_array[test_label_array > 0] > 0.5)) + '\n')
# log_file.write('True negative number : ' + str(sum(prediction_array[test_label_array == 0] <= 0.5)) + '\n')
# log_file.write('False positive number : ' + str(sum(test_label_array[prediction_array > 0.5] == 0)) + '\n')
# log_file.write('False negative number : ' + str(sum(test_label_array[prediction_array <= 0.5] > 0)) + '\n')

# num_correct_predictions = sum(prediction_array[test_label_array > 0] > 0.5) + sum(prediction_array[test_label_array == 0] <= 0.5) * 1.0
# num_wrong_predictions = sum(test_label_array[prediction_array > 0.5] == 0) + sum(test_label_array[prediction_array <= 0.5] > 0) * 1.0

# log_file.write('Percentage correctly predicted : ' + str(num_correct_predictions / (num_correct_predictions + num_wrong_predictions)) + '\n')

# log_file.write('For fire instances, average difference(real label - prediction) : ' + str(np.mean(diff_array[test_label_array > 0])) + '\n')
# log_file.write('For non fire instances, average difference : ' + str(np.std(diff_array[test_label_array == 0])) + '\n')

# log_file.close()
