from Phase3 import data_handler
import numpy as np
import math
from sklearn import mixture
import pickle

NUMBER_OF_CLUSTERS = 5


def fit_gaussian_model(vectors_list: list, number_of_clusters=NUMBER_OF_CLUSTERS):
    g_model = mixture.GaussianMixture(n_components=number_of_clusters)
    g_model.fit(np.array([v.reshape(1, len(v)) for v in vectors_list]))
    print("centers: \n", g_model.means_)
    return g_model
