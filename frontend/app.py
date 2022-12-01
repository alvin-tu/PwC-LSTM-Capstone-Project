from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import torch
from datetime import datetime, timedelta
import json

'''
LSTM Logic
'''
MODEL_PATH = '../saved_ibm_models/lstm_alvin_1_layer.pt'
DS_PATH = '../IBM/spot-challenge-wildfires/Nov_10/Fire_Weather.csv'
DATA_JSON = open('../saved_ibm_models/lstm_alvin_1_layer_params.json')

model_params = json.load(DATA_JSON)

FEATURES = model_params['features']

DEVICE = model_params['device']

INPUT_LENGTH = model_params['input_length']

OUTPUT_LENGTH = model_params['output_length']

model = torch.jit.load(MODEL_PATH, map_location=DEVICE)
model = model.to(DEVICE)
model.eval()

#prepare data
df = pd.read_csv(DS_PATH)

df= df.drop(columns=['Unnamed: 0'])

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.date

def region_to_int(region):
    mapping = {'NSW':0, 'NT':1, 'QL':2, 'SA':3, 'TA':4, 'VI':5, 'WA':6}
    return mapping[region]

df['Region_int'] = df['Region'].apply(region_to_int)

mean = df.mean()
std = df.std()

def getFireAreas(region, prevDate, currentDate, numForecastDays):
    print('Prev Date:', prevDate)
    #get samples that correspond to the region 
    sample = df.loc[(df['Region'] == region) & (df['Date'] > prevDate) & (df['Date'] <= currentDate)]
    numPrevDays = len(sample)
    print('Number of previous days:', numPrevDays)
    #no data in range
    if (numPrevDays == 0):
        return [0] * numForecastDays
    
    #take only the selected features
    sample = sample[FEATURES]
    
    #Alvin's Model
    sample = sample.values.astype(np.float32)
    sample = torch.tensor(sample).reshape(1,numPrevDays,len(FEATURES)).to(DEVICE)
    prediction = model(sample).cpu().detach().numpy().reshape(OUTPUT_LENGTH)
    fireAreas = []
    fireAreas.append(prediction)
    
    '''
    #Kelly's Model
    
    #normalize the features
    sample_norm = (sample - mean)/std
    #convert to format where it can be turned into torch tensor
    sample_norm = sample_norm.values.astype(np.float32)
    
    fireAreas = []
    #convert it to LSTM input
    sample_norm = torch.tensor(sample_norm).reshape(1,numPrevDays,len(FEATURES)).to(DEVICE)
    print(sample_norm)
    #run sample through model
    prediction_norm = model(sample_norm).cpu().detach().numpy().reshape(OUTPUT_LENGTH)
    print(prediction_norm)
    #denormalize results
    prediction = prediction_norm * std.to_numpy().reshape(1,32) + mean.to_numpy().reshape(1,32)
    
    for pred in prediction:
        fireAreas.append(pred[0])
    '''
    return fireAreas

'''
Frontend
'''
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/response', methods=['POST'])
def response():
    regionVal = request.form.get('region')
    dateVal = request.form.get('currentDate')
    forecastDaysVal = request.form.get('forecastDays')

    currentDate = datetime.strptime(dateVal, "%Y-%m-%d").date()
    numForecastDays = int(forecastDaysVal)
    dates = [currentDate + timedelta(days=x) for x in range(1, numForecastDays+1)]
    #get the beginning date for the sequence
    prevDate = currentDate - timedelta(INPUT_LENGTH)
    fireAreas = getFireAreas(regionVal, prevDate, currentDate, numForecastDays)

    return render_template('dashboard.html', 
                            region = regionVal, 
                            currentDate = dateVal, 
                            forecastDays = forecastDaysVal,
                            days = numForecastDays,
                            dateList = dates,
                            fireAreasList = fireAreas)

if __name__ == '__main__':
    app.run()

