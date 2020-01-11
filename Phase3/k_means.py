from Phase3 import data_handler
import numpy as np
import math
from sklearn import cluster

MAX_ITERS = 5
NUMBER_OF_CLUSTERS = 5


def sikit_k_means(docs_as_vecs_list: list, number_of_clusters: int = NUMBER_OF_CLUSTERS, max_iters=MAX_ITERS):
    vecs_matrix = np.array(docs_as_vecs_list)
    print(vecs_matrix.shape)
    _, labels, _ = cluster.k_means(vecs_matrix, n_clusters=5, verbose=1)
    print(labels)
    return labels



def k_means_clustering(docs_as_vecs_list: list, number_of_clusters: int = NUMBER_OF_CLUSTERS, max_iters=MAX_ITERS):
    init_points = get_initial_centers(docs_as_vecs_list, number_of_clusters)
    current_centers = init_points
    for i in range(max_iters):
        print("-", i)
        print("    -labeling")
        labels = label_vecs(docs_as_vecs_list, current_centers)
        print("    -re centering")
        new_centers_and_counts = recenter(docs_as_vecs_list, labels, number_of_clusters)
        current_centers = [p[0] for p in new_centers_and_counts]
    print("k means clustering done after {} iterations".format(max_iters))
    return labels


def get_initial_centers(vecs_list: list, number_of_clusters: int):  # take k distinct points
    vecs_count = len(vecs_list)
    init_points = np.random.randint(0, vecs_count, number_of_clusters)
    init_points = list(set(init_points))
    while len(init_points) < number_of_clusters:
        new_points = np.random.randint(0, vecs_count, number_of_clusters - len(init_points))
        init_points = list(set(init_points + new_points))
    return [vecs_list[i] for i in init_points]


def distance(v1: np.ndarray, v2: np.ndarray):
    d = v2.shape[0]
    return math.sqrt(np.sum([(v1[i] - v2[i]) ** 2 for i in range(d)]))


def label_vecs(vecs_list: list, centers: list):
    labels = []
    print("len", len(vecs_list))
    i = 0
    for vec in vecs_list:
        i += 1
        print(" ..", i)
        distances = [distance(vec, center) for center in centers]
        labels.append(np.argmin(distances))
    return labels


def recenter(vecs_list: list, labels: list, number_of_clusters: int):
    sum_count_pairs = [(0, 0) for _ in range(number_of_clusters)]
    for i in range(len(vecs_list)):
        vec = vecs_list[i]
        label = labels[i]
        sum_count_pair = sum_count_pairs[label]
        sum_count_pairs[label] = (sum_count_pair[0] + vec, sum_count_pair[1] + 1)
    new_centers_and_counts = [(p[0] / p[1], p[1]) for p in sum_count_pairs]
    return new_centers_and_counts
