import pandas as pd
import numpy as np
import unittest
import sys

sys.path.append('/data/capstone22/src')
from normalizer import Normalizer

class TestNormalizer(unittest.TestCase):
    def test_normalize(self):
        # create mean_std dataframe to initialize Normalizer
        mean = pd.DataFrame(np.array((1,1)))
        std = pd.DataFrame(np.array((1,1)))
        mean_std = pd.concat([mean, std], axis=1)
        mean_std.columns = ['mean', 'std']

        # create testing dataframe to run normalizer function
        test_mean = pd.DataFrame(np.array((2,2)))
        test_std = pd.DataFrame(np.array((2,2)))
        test_mean_std = pd.concat([test_mean, test_std], axis=1)
        test_mean_std.columns = ['mean', 'std']

        # known answer calculated by hand
        ans_mean = pd.DataFrame(np.array((1,1)))
        ans_std = pd.DataFrame(np.array((1,1)))
        ans_mean_std = pd.concat([mean, std], axis=1)
        ans_mean_std.columns = ['mean', 'std']

        normalizer = Normalizer(mean_std)

        # assert every element is equal to each other
        for ind in ans_mean_std.index:
            self.assertEqual(int(normalizer.normalize(test_mean_std)['mean'][ind]), ans_mean_std['mean'][ind])
            self.assertEqual(int(normalizer.normalize(test_mean_std)['std'][ind]), ans_mean_std['std'][ind])
    
    def test_denormalize(self):
        # create mean_std dataframe to initialize Normalizer
        mean = pd.DataFrame(np.array((2,2)))
        std = pd.DataFrame(np.array((2,2)))
        mean_std = pd.concat([mean, std], axis=1)
        mean_std.columns = ['mean', 'std']

        # create testing dataframe to run denormalize function
        test_mean = pd.DataFrame(np.array((1,1)))
        test_std = pd.DataFrame(np.array((1,1)))
        test_mean_std = pd.concat([test_mean, test_std], axis=1)
        test_mean_std.columns = ['mean', 'std']

        # known answer calculated by hand
        ans_mean = pd.DataFrame(np.array((4,4)))
        ans_std = pd.DataFrame(np.array((4,4)))
        ans_mean_std = pd.concat([ans_mean, ans_std], axis=1)
        ans_mean_std.columns = ['mean', 'std']

        normalizer = Normalizer(mean_std)

        # assert every element is equal to each other
        for ind in ans_mean_std.index:
            self.assertEqual(int(normalizer.denormalize(test_mean_std)['mean'][ind]), ans_mean_std['mean'][ind])
            self.assertEqual(int(normalizer.denormalize(test_mean_std)['std'][ind]), ans_mean_std['std'][ind])
    
    def test_bad_type(self):
        data = "oogabooga"
        with self.assertRaises(TypeError):
            normalizer = Normalizer(data)

if __name__ == '__main__':
    unittest.main()