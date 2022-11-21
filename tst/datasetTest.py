import unittest
import sys
import pandas as pd

sys.path.append('/data/capstone22/src')

from dataset import IBMFireDS
from normalizer import Normalizer

class TestIBMDataset(unittest.TestCase):
    def setUp(self):
        df_train = pd.read_csv('/data/capstone22/IBM/spot-challenge-wildfires/Nov_10/Fire_Weather_train.csv')
        
        mean = df_train.mean()
        std = df_train.std()
        mean_std = pd.concat([mean, std], axis=1)
        mean_std.columns = ['mean', 'std']
        
        selected_features = ['Estimated_fire_area',
       'Mean_estimated_fire_brightness', 'Mean_estimated_fire_radiative_power',
       'Mean_confidence', 'Std_confidence', 'Var_confidence', 'Count', 'Precipitation_min()', 'Precipitation_max()',
       'Precipitation_mean()', 'Precipitation_variance()',
       'RelativeHumidity_min()', 'RelativeHumidity_max()',
       'RelativeHumidity_mean()', 'RelativeHumidity_variance()',
       'SoilWaterContent_min()', 'SoilWaterContent_max()',
       'SoilWaterContent_mean()', 'SoilWaterContent_variance()',
       'SolarRadiation_min()', 'SolarRadiation_max()', 'SolarRadiation_mean()',
       'SolarRadiation_variance()', 'Temperature_min()', 'Temperature_max()',
       'Temperature_mean()', 'Temperature_variance()', 'WindSpeed_min()',
       'WindSpeed_max()', 'WindSpeed_mean()', 'WindSpeed_variance()',
       'Region_int']
        selected_mean_std = mean_std.loc[selected_features]
        self.NUM_FEATURES = len(selected_features)
        self.REGION_INT_INDX = selected_features.index('Region_int')
        
        # dataset parameters
        self.normalizer = Normalizer(selected_mean_std)
        self.TIME_RANGE_IN = 25
        self.TIME_RANGE_OUT = 10
        self.SPLIT_PERC = 0.2
        
        self.train_ds = IBMFireDS(df_train, True, selected_features, self.TIME_RANGE_IN, self.TIME_RANGE_OUT, self.SPLIT_PERC , self.normalizer)
        self.valid_ds = IBMFireDS(df_train, False, selected_features, self.TIME_RANGE_IN, self.TIME_RANGE_OUT, self.SPLIT_PERC, self.normalizer)
        
    def tearDown(self):
        pass
    
    # Test that the train dataset __getitem__() function returns the correct shape
    def test_train_getitem(self):
        X_train, y_train = self.train_ds.__getitem__(0)
    
        self.assertEqual(self.TIME_RANGE_IN, X_train.shape[0])
        self.assertEqual(self.NUM_FEATURES, X_train.shape[1])
        self.assertEqual(self.TIME_RANGE_OUT, y_train.shape[0])
        self.assertEqual(self.NUM_FEATURES, y_train.shape[1])
        
    # Test that the validation dataset __getitem__() function returns the correct shape
    def test_valid_getitem(self):
        X_valid, y_valid = self.train_ds.__getitem__(0)
    
        self.assertEqual(self.TIME_RANGE_IN, X_valid.shape[0])
        self.assertEqual(self.NUM_FEATURES, X_valid.shape[1])
        self.assertEqual(self.TIME_RANGE_OUT, y_valid.shape[0])
        self.assertEqual(self.NUM_FEATURES, y_valid.shape[1])
        
    # Test that all elements for a sample are for the same region
    def test_sample_region(self):
        indx = [3, 5, 19, 20]
        X_trains, y_trains = list(), list()
        
        for i in indx:
            X, y = self.train_ds.__getitem__(i)
            X_trains.append(X)
            y_trains.append(y)
            
        for X, y in zip(X_trains, y_trains):
            self.assertEqual(X[0][self.REGION_INT_INDX], X[-1][self.REGION_INT_INDX])
            self.assertEqual(y[0][self.REGION_INT_INDX], y[-1][self.REGION_INT_INDX])
            self.assertEqual(X[0][self.REGION_INT_INDX], y[-1][self.REGION_INT_INDX])
       
    # Test that the validation dataset is smaller than the train dataset 
    def test_length_ds(self):
        self.assertLess(self.valid_ds.__len__(), self.train_ds.__len__())
    

if __name__ == '__main__':
    unittest.main()