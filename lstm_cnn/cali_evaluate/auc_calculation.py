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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pred_pickle', dest='pred_pickle')
args = parser.parse_args()

##########################
# USER SET PARAMETERS
##########################
prediction_filename = args.pred_pickle
output_log_file = '../results/auc_prediction_label_cali.txt'
##########################


prediction_list, label_list = pickle.load(open(prediction_filename, 'rb'))

label_list = [x[0] for x in label_list]
label_array = np.array(label_list)

# threshold the labels to 1 and 0, 1 fore fire and 0 for no fire
label_array[label_array > 0.0] = 1

prediction_array = np.array(prediction_list)

fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_true=label_array, y_score=prediction_array, drop_intermediate=True)

roc_auc = sklearn.metrics.auc(x=fpr, y=tpr)

pred_name = prediction_filename.split('/')[-1].split('.')[0]
result = 'Area under ROC curve for ' + pred_name + ' : ' + str(roc_auc)

with open(output_log_file, 'a') as file:
    file.write(f'\n{result}')





# log_file = open(output_log_file, 'a+')
# log_file.write('Area under ROC curve for ' + prediction_filename + ' : ' + str(roc_auc))
# log_file.close()
