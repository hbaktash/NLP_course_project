
import numpy as np
from Phase1 import dictionary

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

    # scores = tf_idf - (test_vector.reshape(1, -1))
    # scores = scores**2
    # scores = scores.sum(axis=1).reshape(-1)
    # neighbors_arg = scores.argsort()[0:K]
    # neighbors_label = label_vector[neighbors_arg]
    # neighbors_bin = np.bincount(neighbors_label)
    # predict_label = neighbors_bin.argmax().reshape(-1)[0]
    # return predict_label


def get_related_docId_list_classified(query_tokens_array, idf_query, term_to_num, doc_space, predict, category_query):

    query_vector = np.zeros_like(idf_query)
    for token in query_tokens_array:
        query_vector[0, term_to_num[token]] += 1

    #####
    nonzero_indx = np.nonzero(query_vector)
    query_vector[nonzero_indx] -= 1
    query_vector += 1
    query_vector = np.log(query_vector)
    query_vector[nonzero_indx] += 1
    #####

    query_vector = query_vector * idf_query
    query_vector = query_vector / (np.sqrt((query_vector ** 2).sum())+1e-20)
    query_vector = query_vector.reshape(1, -1)
    score_arr = (query_vector * doc_space).sum(1)

    sorted_docId_list = (-score_arr).argsort()
    res = []
    for i in range(1,sorted_docId_list.shape[0]):
        if predict[i] == category_query:
            res.append(i)

    return res[0:10]


def get_occurence_matrix(trie: dictionary.Trie):
    trie.set_termNum_docNum()
    num_of_terms = trie.term_num
    num_of_docs = trie.doc_num

    term_to_num = {}
    term_list = trie.get_all_terms()
    for i in range(len(term_list)):
        term_to_num[term_list[i]] = i

    term_list = trie.get_all_terms()
    doc_term = np.zeros((num_of_docs + 1, num_of_terms))

    for term in term_list:
        posting_list = trie.search_term(term).posting_list
        doc_data = posting_list.first_doc_data

        while doc_data:
            doc_id = doc_data.doc_id
            pos_data = doc_data.first_pos_data
            while pos_data:
                doc_term[doc_id, term_to_num[term]] += 1
                pos_data = pos_data.next_pos

            doc_data = doc_data.next

    return doc_term

def get_accuracy(predict,true_labels):
    return 1 - np.count_nonzero(predict - true_labels) / true_labels.shape[0]

def get_precision_recall_f1(predict,trueLabel,class_num):
    predict_onehot = np.zeros((predict.shape[0],class_num))
    trueLabel_onehot = np.zeros((trueLabel.shape[0],class_num))

    predict_onehot[np.arange(predict.shape[0]),predict-1]=1
    trueLabel_onehot[np.arange(trueLabel.shape[0]), trueLabel - 1] = 1

    confusion_matrix = trueLabel_onehot.transpose() @ predict_onehot
    precision = np.diag(confusion_matrix).reshape(-1,1) / (confusion_matrix.sum(axis=0).reshape(-1,1))
    recal     = np.diag(confusion_matrix).reshape(-1,1) / (confusion_matrix.sum(axis=1).reshape(-1,1))

    f1 = (2 * precision * recal)/(precision+recal)
    f1_avg = np.mean(f1)
    return precision.reshape(-1),recal.reshape(-1),f1_avg


def print_criterias(predict,trueLabel):
    accuracy = get_accuracy(predict,trueLabel)
    precision,recall,f1_avg = get_precision_recall_f1(predict,trueLabel,4)
    print("On Test data: ")
    print("Accuracy                = ",accuracy)
    print("f1_avg                  = ",f1_avg)
    print("Precision of each class = ",precision.tolist())
    print("Recall    of each class = ",recall.tolist())