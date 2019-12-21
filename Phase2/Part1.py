from Phase2.prep_tools import *
from Phase2.utils import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
np.set_printoptions(threshold=np.inf)



#train_x = get_tf_idf(train_x)
#test_x = get_tf_idf(test_x)

prepare_np_flg =  input("Welcome To Phase 2 of MIR project. For the first run, it is required to load the dataset as a numpy array and save it. Do you wish to run this preprocessing? Y/N")
print(prepare_np_flg)
if prepare_np_flg=='Y':
    save_data_np()

while(True):

    train_Y, test_y = get_labels_np()
    train_X, test_x = get_data_np()

    prm = np.range(train_Y.shape[0])
    np.random.shuffle(prm)

    train_indx = prm[0:0.9*prm.shape[0]]
    val_indx   = prm[0.9 * prm.shape[0]:]

    train_x = train_X[train_indx,:]
    train_y = train_Y[train_indx]
    val_x   = train_X[val_indx,:]
    val_y   = train_Y[val_indx]


    section_int = int( input("Please indicate the section number. 1,2,3,4=Quit"))

    if section_int == 1:

        model_int = int(input("Please indicate the model number. 1-Naive Bayes, 2-KNN, 3-SVM, 4-Random Forest"))

        if model_int==1:

            likelihood,prior = NaiveBayes_train(train_x,train_y,1)
            predict = np.zeros_like(val_y)
            for i in range(val_y.shape[0]):
                predict[i] = NaiveBayes(likelihood,prior,val_x[i,:])
                print(i)
            print("Accuracy on Validation = ",1-np.count_nonzero(predict-val_y)/val_y.shape[0])

        if model_int==2:

            K = int(input("Type the value of K: "))
            predict = np.zeros_like(val_y)
            for i in range(val_y.shape[0]):
                predict[i]  = KNN(K,train_x,train_y,val_x[i,:])
                print(i)
            print("Accuracy on Validation = ",1-np.count_nonzero(predict-val_y)/val_y.shape[0])

        if model_int==3:

            C = int(input("Type the value of C: "))
            clf = SVC(gamma='auto',C=C)
            clf.fit(train_x, train_y)
            prediction = clf.predict(val_x)
            print("Accuracy on Validation = ",1-np.count_nonzero(prediction-val_y)/val_y.shape[0])

        if model_int==4:

            clf = RandomForestClassifier(n_estimators=100)
            clf.fit(train_x, train_y)
            prediction = clf.predict(val_x)
            print("Accuracy on Validation = ",1-np.count_nonzero(prediction-val_y)/val_y.shape[0])

    if section_int==2:

        prp_flg = input("If it is the first time, please say yes to preprocess Y/N")
        if prp_flg == "Y":
            #TODO posting list and preprocess should be done
            #TODO Classifier should be trained on train data and classify the english dataset

        if prp_flg == "N":
            query = input("inout your query: ")
            corrected = ""
            for term in PREPROCESSOR.simple_tokenize_and_remove_junk(query):
                corrected = corrected + " " + Part4.word_correction(term, trie_dict, bigram_ds)
            query_tokens = PREPROCESSOR.simple_tokenize_and_remove_junk(corrected)
            relev_docs = part5.get_related_docId_list_proximity_version(query_tokens, idf_query, term_to_num, doc_space,
                                                                        trie_dict)
            print("results: ", relev_docs)

    if section_int==3:
        pass

    if section_int==4:
        exit()



