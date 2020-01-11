from Phase3 import data_handler
import numpy as np
import math
from sklearn.cluster import AgglomerativeClustering
import pickle

NUMBER_OF_CLUSTERS = 5


def cluster_hierarchical(vectors_list: list, number_of_clusters=NUMBER_OF_CLUSTERS):
    hr_clustering = AgglomerativeClustering(n_clusters=number_of_clusters,linkage='single')
    vecs_matrix = np.array(vectors_list)
    print(vecs_matrix.shape)
    hr_clustering.fit(vecs_matrix)
    labels = hr_clustering.labels_
    return labels
