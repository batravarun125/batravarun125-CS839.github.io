import pandas as pd
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
import nltk.data
from nltk import tokenize
from os import listdir
import os.path
import re
import argparse

from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score


output_dir_path = os.path.dirname(os.path.abspath(__file__))+'/results/'

parser = argparse.ArgumentParser(description = 'removing not relevant labels')
parser.add_argument('--trainData', action='train file')
parser.add_argument('--testData', type=str, help="test file")
parser.add_argument('--model', type=int, help="Model number to be tested 1. DecisionTreeClassifier")

if __name__ == '__main__':


    args = parser.parse_args()

    train_df = pd.read_csv(output_dir_path+args.trainData)
    test_df = pd.read_csv(output_dir_path + args.testData)
    df = pd.DataFrame(np.random.randn(100, 2))
    msk = np.random.rand(len(df)) < 0.8
    train_split = train_df[msk]
    val_split = train_df[msk]
    features = ['n-gram', 'POST_DIST_VERB', 'PrecedingTitle', 'PRE_DIST_FROM_POSITION', 'NEGATIVE_FEATURE',
                'POSITIVE_FEATURE']
    input_data = train_split[features].as_matrix()
    target = train_split['classtype'].as_matrix()

    model = DecisionTreeClassifier()
    model.fit(input_data, target)
    # print(model)

    expected = val_split['classtype'].as_matrix()

    predicted = model.predict(val_split[features].as_matrix())

    n = len(expected)

    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    




