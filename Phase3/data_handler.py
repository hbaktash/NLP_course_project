from Phase2 import prep_tools
from Phase1 import dictionary
import numpy as np
import pandas as pd

LANGUAGE = 1  # "english"


def prepare_data_as_list():
    filename = "Data.csv"
    trie_dict, _ = dictionary.build_dictionary(english_or_persian=LANGUAGE, filename=filename)
    trie_list = trie_dict.to_list()
    trie_list.sort(key=lambda x: x.term)
    term_and_posting_list = [(a.term, a.posting_list) for a in trie_list]
    return term_and_posting_list


def term_pl_list_to_matrix(term_pl_list: list, docs_count: int = 5000):
    term_arr = [a[0] for a in term_pl_list]
    doc_id_tfs_list = [a[1].to_list() for a in term_pl_list]
    doc_term_matrix = np.zeros((docs_count, len(term_arr)))
    for i in range(len(doc_id_tfs_list)):
        doc_id_tfs = doc_id_tfs_list[i]
        for doc_id_tf in doc_id_tfs:
            doc_id = doc_id_tf[0]
            tf = doc_id_tf[1]
            doc_term_matrix[doc_id - 1][i] = tf
    return doc_term_matrix, term_arr


# def get_labels_np():
#     "phase2_train.csv"
#     train_y = pd.read_csv("phase2_train.csv").to_numpy()[:, 0]
#     test_y = pd.read_csv("phase2_test.csv").to_numpy()[:, 0]
#     train_y = train_y.astype(int)
#     test_y = test_y.astype(int)
#     return train_y, test_y


def get_data_np():
    doc_term_data = np.load("doc_term_data3.npy")
    term_list = np.load("term_list.npy")
    return doc_term_data, term_list


def save_data_np():
    term_and_posting_list = prepare_data_as_list()
    doc_term_data, term_arr = term_pl_list_to_matrix(term_and_posting_list)
    np.save("doc_term_data3.npy", doc_term_data)
    np.save("term_list.npy", term_arr)


def get_data():
    term_and_posting_list = prepare_data_as_list()
    doc_term_data, term_arr = term_pl_list_to_matrix(term_and_posting_list)
