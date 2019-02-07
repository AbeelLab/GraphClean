import pickle
import numpy as np
import pandas as pd
import subprocess

outputoverlappath = "/tudelft.net/staff-umbrella/haplotype/2018/data/potato/Solanum_tuberosum.SolTub_3.0.dna_sm.chromosome.4.fa-chr-4-ploidy1-cov-30-72208621-"
base_name = "results/4-features-30-72208621-"
features_name = ['Centrality', 'Degree', 'Node2Vec', 'ShortestPath', 'SLL']


def classifyoverlaps(base_name, modelpath, threshold):
    threshold = 1 - threshold
    X_test = list()
    for feature in features_name:
        if feature == 'Node2Vec':
            n2v = pd.read_csv(base_name + '-' + feature, delimiter=',', header=None)
            n2v = n2v.values
            for i in range(len(n2v[0])):
                X_test.append(n2v[:, i])
        else:
            X_test.append(pd.read_csv(base_name + '-' + feature, delimiter=',', header=None).values.flatten())

    X_test = np.asarray(X_test).T
    print(np.shape(X_test))
    clf = pickle.load(open(modelpath, 'rb'))
    scaler = pickle.load(open('models/scaler-potato', 'rb'))
    X_test = scaler.transform(X_test)
    Y_test_pred_prob = clf.predict_proba(X_test)
    Y_test_pred_prob = np.asarray(Y_test_pred_prob)[:, 1]
    Y_test_pred_prob[Y_test_pred_prob > threshold] = 1
    Y_test_pred_prob[Y_test_pred_prob < threshold] = 0

    return Y_test_pred_prob

