from Phase3 import data_handler
from Phase3 import k_means


def prepare_data_and_cluster():
    doc_term_matrix, terms = data_handler.get_data_np()
    vectors_list = data_handler.doc_term_mat_to_tf_idf(doc_term_matrix, terms)
    # vectors_list = data_handler.doc_term_mat_to_w2vec()
    labels = k_means.k_means_clustering(vectors_list)
