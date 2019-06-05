import numpy as np
import random
import pandas as pd
from random import randint
from sklearn import svm
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import precision_recall_fscore_support
import subprocess
import FilterOverlaps
import pickle
import re

random.seed(2)

c = 0.01
outputoverlappath = "/tudelft.net/staff-umbrella/haplotype/2018/data/potato/Solanum_tuberosum.SolTub_3.0.dna_sm.chromosome.4.fa-chr-4-ploidy4-cov-30-72208621-"
base_name = "results/Solanum_tuberosum.SolTub_3.0.dna_sm.chromosome.4.fa-features-30-72208621-"
organism = 'potato'
features_name = ['Centrality', 'Degree', 'Node2Vec', 'ShortestPath', 'SLL', 'SL']



samplescount = list()
samplesnumber = random.sample(range(0, 15), 15)
print(samplesnumber)
samplesnumber = samplesnumber[0:5]
samplescount = list()
X = list()
Y = list()
for i in samplesnumber:
    temp_list = list()
    temp_name = base_name + str(i)
    for feature in features_name:
        if feature == 'Node2Vec':
            n2v = pd.read_csv(temp_name + '-' + feature, delimiter=',', header=None)
            n2v = n2v.values
            samplescount.append(len(n2v))
            for i in range(len(n2v[0])):
                temp_list.append(n2v[:, i])
        else:
            temp_list.append(pd.read_csv(temp_name + '-' + feature, delimiter=',', header=None).values.flatten())

    X.append(np.array(temp_list))
    Y.append(pd.read_csv(temp_name + '-label.csv', delimiter=',', header=None).values)

X = np.hstack(X)
X = X.T
Y = np.asarray([item for sublist in Y for item in sublist]).flatten()
Y[Y == 2] = 0
Y[Y == 3] = 1


print(X.shape)
print(Y.shape)
print(Y)

X_neg = X[Y == 1]
X_pos = X[Y == 0]
Y_pos = Y[Y == 0]
Y_neg = Y[Y == 1]

print(X_pos.shape[0])
print(len(Y_neg))

index = np.random.choice(X_pos.shape[0], len(Y_neg), replace=False)
X_pos = X_pos[index]
Y_pos = Y_pos[index]
X = np.vstack((X_pos, X_neg))
Y = np.concatenate((Y_pos, Y_neg))
print('data done')

Y[Y == 1] = 1
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

clf = LogisticRegression(random_state=2324, solver='saga', C=c)
#clf = RandomForestClassifier(n_estimators=500, random_state=2324, n_jobs=20)
clf.fit(X, Y)
pickle.dump(scaler, open('models/scalerpoly', 'wb'))
pickle.dump(clf, open('models/modelpoly' + organism + '-' + str(c), 'wb'))

#ids = np.argsort((-np.abs(clf.coef_)))
#print(ids)
#for i in ids:
#    print(clf.coef_[0][i])

