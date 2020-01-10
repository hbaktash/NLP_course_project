from Phase3 import data_handler
import numpy as np
import math

MAX_ITERS = 400
NUMBER_OF_CLUSTERS = 5


def k_means_clustering(docs_as_vecs_list: list, number_of_clusters: int = NUMBER_OF_CLUSTERS, max_iters=MAX_ITERS):
    init_points = get_initial_centers(docs_as_vecs_list, number_of_clusters)
    current_centers = init_points
    for _ in range(max_iters):
        labels = label_vecs(docs_as_vecs_list, current_centers)
        new_centers_and_counts = recenter(docs_as_vecs_list, labels, number_of_clusters)
        current_centers = [p[0] for p in new_centers_and_counts]
    print("clustering done after {} iterations".format(max_iters))
    print(labels)
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
    return math.sqrt(np.sum([(v1[i]-v2[i])**2 for i in range(d)]))


def label_vecs(vecs_list: list, centers: list):
    labels = []
    for vec in vecs_list:
        distances = [distance(vec, center) for center in centers]
        labels.append(np.argmin(distances))
    return labels

def recenter(vecs_list: list, labels: list, number_of_clusters: int):
    sum_count_pairs = [(0,0) for _ in range(number_of_clusters)]
    for i in range(len(vecs_list)):
        vec = vecs_list[i]
        label = labels[i]
        sum_count_pair = sum_count_pairs[i]
        sum_count_pairs[i] = (sum_count_pair[0] + vec, sum_count_pair[1] + 1)
    new_centers_and_counts = [(p[0]/p[1], p[1]) for p in sum_count_pairs]
    return new_centers_and_counts