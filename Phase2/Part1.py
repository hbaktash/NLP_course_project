from Phase2.prep_tools import *



term_and_posting_list = prepare_data_as_list(train_not_test=True)
train_x = term_pl_list_to_matrix(term_and_posting_list)
prepare_data_as_list(train_x.shape)
