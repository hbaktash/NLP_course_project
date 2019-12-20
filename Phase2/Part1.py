from Phase2.prep_tools import *


import numpy as np
np.set_printoptions(threshold=np.inf)

train_y,test_y = get_labels_np()
train_x,test_x = get_data_np()
print(train_x.shape,train_y.shape,test_x.shape,test_y.shape)


