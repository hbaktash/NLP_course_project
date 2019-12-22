import numpy as np
from Phase2.utils import get_sho
predict = np.array([1,2,2,3,2,4])
trueLabel = np.array([1,1,1,3,3,3])
class_num=4

predict_onehot = np.zeros((predict.shape[0],class_num))
trueLabel_onehot = np.zeros((trueLabel.shape[0],class_num))

predict_onehot[np.arange(predict.shape[0]),predict-1]=1
trueLabel_onehot[np.arange(trueLabel.shape[0]), trueLabel - 1] = 1

confusion_matrix = predict_onehot.transpose()@predict_onehot
print(confusion_matrix)
print("@@@")
print(np.diag(confusion_matrix))