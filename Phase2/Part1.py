from Phase2.prep_tools import *

import numpy as np
np.set_printoptions(threshold=np.inf)


train_term_and_posting_list = prepare_data_as_list(train_not_test=True)
train_x, train_terms = term_pl_list_to_matrix(train_term_and_posting_list)
test_term_and_posting_list = prepare_data_as_list(train_not_test=False)
test_x, _ = term_pl_list_to_matrix_for_test_given_train(test_term_and_posting_list, train_terms)
print(train_x.sum(axis=1))
print(test_x.sum(axis=1))
