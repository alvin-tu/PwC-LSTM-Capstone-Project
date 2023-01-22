import pandas as pd
import numpy as np
import os

import torch
from torch.utils.data import Dataset


class IsaacDS(Dataset):
    def __init__(self, split, features, data_dir):
        self.split = split
        self.features = features
        self.data_dir = data_dir
        self.df = self.getdf()
      

    def getdf(self):
        path = os.path.join(self.data_dir, f'isaac_{self.split}.csv')
        df = pd.read_csv(path)
        df = df[self.features]
        
        return df
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        X = self.df.drop(columns=['value']).iloc[idx].values
        y = self.df['value'].iloc[idx]
        return torch.from_numpy(X).float(), torch.from_numpy(np.array([y])).float()