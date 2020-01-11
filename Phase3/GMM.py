from Phase3 import data_handler
import numpy as np
import math
from sklearn import mixture
import pickle

NUMBER_OF_CLUSTERS = 50


def fit_gaussian_model(vectors_list: list, number_of_clusters=NUMBER_OF_CLUSTERS):
    g_model = mixture.GaussianMixture(n_components=number_of_clusters, verbose=1, covariance_type='diag')
    vecs_matrix = np.array(vectors_list)
    print(vecs_matrix.shape)
    g_model.fit(vecs_matrix)
    print("centers: \n", g_model.means_)
    labels = g_model.predict(vecs_matrix)
    return labels
