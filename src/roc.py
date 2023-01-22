'''
Here is a good source: https://towardsdatascience.com/intuition-behind-roc-auc-score-1456439d1f30
Also seen in CS165B Lecture 4

TLDR: 
- ROC graph plots FPR (false postiive rate) against TPR (true positive rate)
- The thresholds are different probability cutoffs that separate the two classes in binary classification. It uses probability to tell us how well a model separates the classes.
- The area under the curve (AUC) represents the ranking accuracy
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve

"""
    Parameters: 
    y_true: true binary labels of fire/no fire
    y_pred: probability estimate of the 
"""

def plot_roc_curve(y_true, y_pred):
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    print(f'AUC score: {roc_auc_score(y_true, y_pred)}')