
import numpy as np


def NaiveBayes_train(occurence_matrix, label_vector, normalization_factor):

    class_num = label_vector.max()
    word_num = occurence_matrix.shape[1]
    docs_num = occurence_matrix.shape[0]

    prior = np.zeros(class_num+1)
    likelihood = np.zeros((class_num+1,word_num))

    for class_int in range(1,class_num+1):

        prior[class_int] = np.argwhere(label_vector == class_int).shape[0]

    prior/=docs_num


    for class_int in range(1,class_num+1):

        class_arg = np.argwhere(label_vector == class_int).reshape(-1)
        terms_of_a_class = occurence_matrix[class_arg,:].sum(axis=0).reshape(1,-1) + normalization_factor *  np.ones((1,word_num))
        likelihood[class_int,:] =  terms_of_a_class /terms_of_a_class.sum()


    return likelihood,prior

def NaiveBayes(likelihood,prior,test_vector):

    prob =  np.power(likelihood,test_vector.reshape(1,-1))
    prob = np.prod(prob,axis=1)

    prob = (prob.reshape(-1,1) * prior.reshape(-1,1)).reshape(-1)
    return np.argmax(prob)


#def KNN_train(tf_idf,label_matrix):

def get_tf_idf(occurence_matrix):
    exist_matrix = np.copy(occurence_matrix)
    exist_matrix[exist_matrix>1]=1
    idf = exist_matrix.sum(axis=0)
    idf +=1
    doc_num = occurence_matrix.shape[0]
    idf = np.log(doc_num/idf).reshape(1,-1)
    tf_idf = occurence_matrix*idf
    return tf_idf

def KNN(K,tf_idf,label_vector,test_vector):
    scores = tf_idf * (test_vector.reshape(1,-1))
    scores = scores.sum(axis=1).reshape(-1)
    neighbors_arg = scores.argsort()[::-1][0:K]
    neighbors_label = label_vector[neighbors_arg]
    neighbors_bin = np.bincount(neighbors_label)
    predict_label = neighbors_bin.argmax().reshape(-1)[0]
    return predict_label


