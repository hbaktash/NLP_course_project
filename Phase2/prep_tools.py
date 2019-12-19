from Phase1 import dictionary, file_handler
import numpy as np
LANGUAGE = 1  # English


def prepare_data_as_list(train_not_test=True):
    if train_not_test:
        filename = "phase2_train.csv"
    else:
        filename = "phase2_test.csv"
    trie_dict, _ = dictionary.build_dictionary(english_or_persian=LANGUAGE, filename=filename)
    trie_list = trie_dict.to_list()
    trie_list.sort(key=lambda x: x.term)
    term_and_posting_list = [(a.term, a.posting_list) for a in trie_list]
    return term_and_posting_list


def term_pl_list_to_matrix(term_pl_list: list, docs_count: int = 9000):
    term_arr = [a[0] for a in term_pl_list]
    doc_id_tfs_list = [a[1].to_list() for a in term_pl_list]
    doc_term_matrix = np.zeros((docs_count, len(term_arr)))
    for i in range(len(doc_id_tfs_list)):
        doc_id_tfs = doc_id_tfs_list[i]
        for doc_id_tf in doc_id_tfs:
            doc_id = doc_id_tf[0]
            tf = doc_id_tf[1]
            doc_term_matrix[doc_id-1][i] = tf
    return doc_term_matrix
