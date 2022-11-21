# Normalizer class 
class Normalizer():
    def __init__(self, mean_std):
        self.mean = mean_std['mean'].to_numpy()
        self.std = mean_std['std'].to_numpy()
        
    def normalize(self, sample):
        return (sample - self.mean) / self.std
    
    def denormalize(self, sample):
        return (sample * self.std) + self.mean




