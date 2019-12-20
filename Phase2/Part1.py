from Phase2.prep_tools import *
from Phase2.utils import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
np.set_printoptions(threshold=np.inf)


train_y,test_y = get_labels_np()
train_y = train_y.astype(int)
test_y  = test_y.astype(int)
train_x,test_x = get_data_np()
print(train_x.shape,train_y.shape,test_x.shape,test_y.shape)

train_x = get_tf_idf(train_x)
test_x = get_tf_idf(test_x)

clf = SVC(gamma='auto')
clf.fit(train_x, train_y.astype(int))
prediction = clf.predict(train_x)
print(1-np.count_nonzero(prediction-train_y)/train_y.shape[0])

##############
#
#
# clf = RandomForestClassifier(n_estimators=100)
# clf.fit(train_x, train_y)
# prediction = clf.predict(test_x)
# print(1-np.count_nonzero(prediction-test_y)/test_y.shape[0])
#
