from Phase3 import data_handler
from Phase3 import k_means, GMM, hierarchichal
import numpy as np


def prepare_data_and_cluster():
    print("getting data")
    doc_term_matrix, terms = data_handler.get_data_np()
    print("occurance to vectors")
    vectors_list = data_handler.doc_term_mat_to_tf_idf(doc_term_matrix)
    # vectors_list = data_handler.doc_term_mat_to_w2vec()
    # print("running gmm:")
    # gmm_labels = GMM.fit_gaussian_model(vectors_list)
    # np.save("GMM labels.npy", gmm_labels)
    # print("\ngmm labels\n", gmm_labels)
    # print("running hr clustering:")
    # hr_labels = hierarchichal.cluster_hierarchical(vectors_list)
    # np.save("GMM labels.npy", hr_labels)
    # print("\nhr_labels:\n", hr_labels)
    print("running k means:")
    km_labels = k_means.sikit_k_means(vectors_list)
    np.save("k_means labels.npy", km_labels)
    print("\nk means:\n", km_labels)


prepare_data_and_cluster()
