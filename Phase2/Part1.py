from Phase2.prep_tools import *

import numpy as np
np.set_printoptions(threshold=np.inf)


term_and_posting_list = prepare_data_as_list(train_not_test=True)
train_x = term_pl_list_to_matrix(term_and_posting_list)
print(train_x.sum(axis=1))
