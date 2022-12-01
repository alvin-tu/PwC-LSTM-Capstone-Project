# %%
import pandas as pd
import json

import numpy as np
from tqdm import tqdm

from datetime import datetime
from time import time

import torch

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.utils.data import Dataset
from torch.utils.data import DataLoader

import math

from src.normalizer import Normalizer
from src.dataset import IBMFireDS

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--in_len', dest='in_len', type=int, default=10)
parser.add_argument('--out_len', dest='out_len', type=int, default=10)
parser.add_argument('--gpu', dest='gpu', type=int, default=2)
parser.add_argument('--name', dest='name', type=str, default='model')
args = parser.parse_args()

# %% [markdown]
# # Data Preprocessing

# %%
# Load in training data
df_train = pd.read_csv('/data/capstone22/IBM/spot-challenge-wildfires/Nov_10/Fire_Weather_train.csv')

# %%
# Calculate mean and std for all features

mean = df_train.mean()
std = df_train.std()
mean_std = pd.concat([mean, std], axis=1)
mean_std.columns = ['mean', 'std']

# %%
# Define features to use
# selected_features = ['Estimated_fire_area',
#        'Mean_estimated_fire_brightness', 'Mean_estimated_fire_radiative_power',
#        'Mean_confidence', 'Std_confidence', 'Var_confidence', 'Count', 'Precipitation_min()', 'Precipitation_max()',
#        'Precipitation_mean()', 'Precipitation_variance()',
#        'RelativeHumidity_min()', 'RelativeHumidity_max()',
#        'RelativeHumidity_mean()', 'RelativeHumidity_variance()',
#        'SoilWaterContent_min()', 'SoilWaterContent_max()',
#        'SoilWaterContent_mean()', 'SoilWaterContent_variance()',
#        'SolarRadiation_min()', 'SolarRadiation_max()', 'SolarRadiation_mean()',
#        'SolarRadiation_variance()', 'Temperature_min()', 'Temperature_max()',
#        'Temperature_mean()', 'Temperature_variance()', 'WindSpeed_min()',
#        'WindSpeed_max()', 'WindSpeed_mean()', 'WindSpeed_variance()',
#        'Region_int']

selected_features = ['Estimated_fire_area',
       'Mean_estimated_fire_brightness', 'Mean_estimated_fire_radiative_power',
       'Mean_confidence', 'Std_confidence', 'Var_confidence', 'Count',
       'Precipitation_mean()', 
       'RelativeHumidity_mean()',
       'SoilWaterContent_mean()', 'SolarRadiation_mean()',
       'Temperature_mean()', 'WindSpeed_mean()',
       'Region_int']

# %%
# Mean and std for selected features only
selected_mean_std = mean_std.loc[selected_features]

# %%
INPUT_LENGTH = args.in_len
OUTPUT_LENGTH = args.out_len
SPLIT_PERC = 0.2

normalizer = Normalizer(selected_mean_std)
ibm_train_ds = IBMFireDS(df_train, True, selected_features, INPUT_LENGTH, OUTPUT_LENGTH, SPLIT_PERC , normalizer)
ibm_val_ds = IBMFireDS(df_train, False, selected_features, INPUT_LENGTH, OUTPUT_LENGTH, SPLIT_PERC, normalizer)

# %%
trainloader = DataLoader(ibm_train_ds, batch_size=8, shuffle=False, num_workers=16)
valloader = DataLoader(ibm_val_ds, batch_size=64, shuffle=False, num_workers=8)

# %% [markdown]
# # Model Building

# %%
class LSTM(nn.Module):
    def __init__(self, features, hidden_size, num_layers, device, time_range_out=10):
        super().__init__()
        self.device = device
        self.features = features
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(features, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, features)
        self.time_range_out = time_range_out

    def forward(self, x):
        predictions = list()
        
        batch_size = x.shape[0]
#         time_range = x.shape[1]
        
        
        # Initial states
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(self.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(self.device)
        state = (h0, c0)
        
        # Run input through the lstm
        x, state = self.lstm(x, state)
        prediction = self.fc(x[:,-1,:].view((batch_size, 1, self.hidden_size)))
        predictions.append(prediction)
        
        # Autogressive part
        for regress_step in range(1, self.time_range_out):
            x = prediction
            x, state = self.lstm(x, state)
            prediction = self.fc(x)
            predictions.append(prediction)
            
        # Convert predictions to tensor
        predictions = torch.cat(predictions, dim=1)
        
        return predictions

# %%
# Helper function to get errors for estimated fire area only

def get_estimated_fire_area_errors(model, dataloader, time_range_out=10, error='abs'):
    print('Estimated fire area loss over the entire validation set')
    loss = 0
    fire_feature_indx = 2
    errors = 0
    for samples, labels in dataloader:
        batch_size = samples.shape[0]
#         num_days = samples.shape[1]
        
        prediction = normalizer.denormalize(model(samples.to(DEVICE)).cpu().detach())
        labels = normalizer.denormalize(labels)
        
        prediction_fire = prediction[:,:,fire_feature_indx]
        labels_fire = labels[:,:,fire_feature_indx]
        
        if error == 'abs':
            error = abs(prediction_fire - labels_fire)
        elif error == 'mse':
            error = (prediction_fire-labels_fire)**2
        
        errors += sum(error) / batch_size
    
    errors /= valloader.__len__()
    for i in range(time_range_out):
        print(f'average error for day {i+1} prediction: {errors[i]}')
    return errors


# %% [markdown]
# # Training Loop

# %%
DEVICE = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")

# %%
NUM_FEATURES = len(selected_features)
HIDDEN_SIZE = 512
NUM_LSTM_LAYERS = 3

model = LSTM(NUM_FEATURES, HIDDEN_SIZE, NUM_LSTM_LAYERS, DEVICE, OUTPUT_LENGTH)
# model= nn.DataParallel(model,device_ids = [1, 2])
model.to(DEVICE)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# %%
# total_train_value = 0
# for samples, labels in trainloader:
#     total_train_value += torch.sum(labels)
# print(f'Total sum of train label values: {total_train_value:.8E}')

# total_valid_value = 0
# for samples, labels in valloader:
#     total_valid_value += torch.sum(labels)
# print(f'Total sum of valid label values: {total_valid_value:.8E}')

# %%
# Training Loop

epochs = 100
min_loss = np.inf
best_model = model
tolerance = 40
no_improvement = 0
model_name = f'./saved_ibm_models/varying_output_length/{args.name}'


for e in range(epochs):
    start = time()
    print(f'Epoch {e}: ---------------------------------------------')
    model.train()
    running_loss = 0
    running_loss_denormalized = 0
    for samples, labels in trainloader:
        optimizer.zero_grad()
        
        predictions = model(samples.to(DEVICE))
        loss = criterion(predictions, labels.to(DEVICE))
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        # Denormalized loss
        a = normalizer.denormalize(predictions.cpu().detach())
        b = normalizer.denormalize(labels.cpu().detach())
        denormalize_loss = criterion(a, b)
        running_loss_denormalized += denormalize_loss
    else:
        print(f'Training loss: {running_loss/len(trainloader)}', end = ' ')
        print(f'Training denormalized loss: {running_loss_denormalized/len(trainloader)}')
        
    # Evaluate on Validation Set
    model.eval()
    val_loss = 0
    val_loss_denormalized = 0
    with torch.no_grad():
        for samples, labels in valloader:
            predictions = model(samples.to(DEVICE))
            loss = criterion(predictions, labels.to(DEVICE))
            
            val_loss += loss.item()
            
            # Denormalized loss
            a = normalizer.denormalize(predictions.cpu().detach())
            b = normalizer.denormalize(labels.cpu().detach())
            denormalize_loss = criterion(a, b)
            val_loss_denormalized += denormalize_loss
            
        else:
            val_loss /= len(valloader)
            val_loss_denormalized /= len(valloader)
            
            print(f'Validation loss: {val_loss}', end = ' ')
            print(f'Validation denormalized loss: {val_loss_denormalized}')
            
#             fire_error = get_estimated_fire_area_errors(model, valloader, OUTPUT_LENGTH)
#             fire_error = sum(fire_error) / len(fire_error)
#             print(f'fire_error = {fire_error}')
            
            # Save model based on loss
            if val_loss < min_loss:
                min_loss = val_loss
                best_model = model
                torch.jit.script(model).save(f'{model_name}.pt') 
                print('Model saved!')
            else: 
                no_improvement += 1
                if no_improvement >= tolerance:
                    break
                
    print(f'Epoch time: {round(time()-start, 2)}')
        

# %%
# Get estimated fire area errors for the entire validation set

model = torch.jit.load(f'{model_name}.pt', map_location=DEVICE)
model = model.to(DEVICE)
val_fire_errors = get_estimated_fire_area_errors(model, valloader, time_range_out=OUTPUT_LENGTH)

# %%
# Save model parameters as JSON

model_params = {
    'name': model_name,
    'device': str(DEVICE),
    'input_length': INPUT_LENGTH,
    'output_length': OUTPUT_LENGTH,
    'hidden_size': HIDDEN_SIZE,
    'num_lstm_layers': NUM_LSTM_LAYERS,
    'num_features': len(selected_features),
    'features': selected_features,
    'validation_fire_errors': val_fire_errors.numpy().tolist(),
}

json_object = json.dumps(model_params)

with open(f'{model_name}_params.json', 'w') as outfile:
    outfile.write(json_object)

# %%
# # Check prediction for 1 sample

# best_model = torch.jit.load('./best_model.pt', map_location=device)

# X, y = ibm_val_ds.__getitem__(50) 
# best_model = best_model.to(device)

# prediction = best_model(X.to(device).unsqueeze(dim=0))
# prediction = prediction.squeeze(dim=0)

# first_pred = prediction[0]
# denormalized_first_pred = normalizer.denormalize(first_pred.cpu().detach())

# gt = y[0]
# denormalized_y = normalizer.denormalize(gt.cpu().detach())

# for feature, truth, prediction in zip(selected_features, denormalized_y, denormalized_first_pred):
#     print(f'{feature}: truth = {truth}, prediction = {prediction} abs_diff = {abs(prediction - truth)}')



