# Dataset Class

from torch.utils.data import Dataset
import pandas as pd
import numpy as np

import torch

class IBMFireDS(Dataset):
    def __init__(self, df, train, features, time_range_in, time_range_out, split_perc, normalizer):
        self.train = train
        self.features = features
        self.time_range_in = time_range_in
        self.time_range_out = time_range_out
        self.split_perc = split_perc
        self.df = self.getdf(df)
        self.map_idx = self.getValidIdx()
        self.normalizer = normalizer
      
    # Depending on whether the class is initialized as a train ds or validation ds, filter and store the df
    def getdf(self, df):
        df = df[self.features]
        df = df.fillna(0)
        df_new = pd.DataFrame(columns=df.columns)
        
        for region, count in zip(*np.unique(df.Region_int, return_counts=True)):
            region_rows = df.loc[df.Region_int == region]
#             region_rows = region_rows.sort_values(by='Date_int', ascending=True)
            
            if self.train:
                rows = region_rows.iloc[:-int(count*self.split_perc)]
            else:
                rows = region_rows.iloc[-int(count*self.split_perc):]
                
            df_new = pd.concat([df_new, rows], ignore_index=True)
                
        return df_new 
    
    # Valid indexes
    def getValidIdx(self):
        validIndx = []
#         for i in range(self.df.shape[0] - self.time_range*2 + 1):
        total_time_range = self.time_range_in + self.time_range_out
        for i in range(self.df.shape[0] - total_time_range + 1):
#             y_end = i + 2*self.time_range - 1
            y_end = total_time_range
            if (y_end < self.df.shape[0]) and (self.df.iloc[i]['Region_int'] == self.df.iloc[y_end]['Region_int']):
                validIndx.append(i)
        return validIndx
        
    def __len__(self):
        return len(self.map_idx)
    
    # Returns training sample X and y
    # X contains 'time_range' samples, each w/ 'features' number of features; same w/ y
    def __getitem__(self, idx):
        X_start = self.map_idx[idx]
        X_end = X_start + self.time_range_in # exclusive 
        y_start = X_end 
        y_end = y_start + self.time_range_out # exclusive
        
        X = self.df.iloc[X_start:X_end].to_numpy(dtype=float)
        y = self.df.iloc[y_start:y_end].to_numpy(dtype=float)
        
        # Perform Z-score Normalization 
        X = self.normalizer.normalize(X)
        y = self.normalizer.normalize(y)
        
        # To torch
        X = torch.from_numpy(X).float()
        y = torch.from_numpy(y).float()
        
        return X, y
    