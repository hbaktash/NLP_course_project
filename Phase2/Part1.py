from Phase1 import english_preprocessing,part5,Part4
from Phase2.prep_tools import *
from Phase2.utils import *
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
np.set_printoptions(threshold=np.inf)



#train_x = get_tf_idf(train_x)
#test_x = get_tf_idf(test_x)

prepare_np_flg =  input("Welcome To Phase 2 of MIR project. For the first run, it is required to load the dataset as a numpy array and save it. Do you wish to run this preprocessing? Y/N")
if prepare_np_flg=='Y':
    save_data_np()

while(True):

    train_Y, test_y = get_labels_np()
    train_X, test_x, big_term_arr = get_data_np()

    prm = np.arange(train_Y.shape[0])
    np.random.shuffle(prm)

    train_indx = prm[0:int(0.9*prm.shape[0])]
    val_indx   = prm[int(0.9 * prm.shape[0]):]

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
            print("Accuracy on Validation = ",get_accuracy(predict,val_y))

        if model_int==2:

            K = int(input("Type the value of K: "))
            predict = np.zeros_like(val_y)
            for i in range(val_y.shape[0]):
                predict[i]  = KNN(K,train_x,train_y,val_x[i,:])
                print(i)
            print("Accuracy on Validation = ",get_accuracy(predict,val_y))

        if model_int==3:

            C = int(input("Type the value of C: "))
            clf = SVC(gamma='auto',C=C)
            clf.fit(train_x, train_y)
            prediction = clf.predict(val_x)
            print("Accuracy on Validation = ",get_accuracy(predict,val_y))

        if model_int==4:

            clf = RandomForestClassifier(n_estimators=100)
            clf.fit(train_x, train_y)
            prediction = clf.predict(val_x)
            print("Accuracy on Validation = ",get_accuracy(predict,val_y))

    if section_int==2:


        try:
            predict =  np.load("prediction_for_phas1Data.npy")

        except:
            print(" As it is the first query, please be patient while we train a model to classify the Phase1 Dataset")
            PREPROCESSOR = english_preprocessing
            all_docs_and_titles = file_handler.load_english_file()

            trie_dict, bigram_ds = dictionary.build_dictionary(english_or_persian=1)
            doc_space, idf_query, term_to_num = part5.vector_space_preprocess(trie_dict)
            occurence_matrix = get_occurence_matrix(trie_dict)

            small_term_list = [None] * len(list(term_to_num.keys()))
            for term in list(term_to_num.keys()):
                small_term_list[term_to_num[term]] = term

            big_term_list = big_term_arr.tolist()
            big_indx = []
            small_indx = []
            term_cnt = 0
            for term in small_term_list:
                # indx.append(big_term_list.index(term))
                if term in big_term_list:
                    big_indx.append(big_term_list.index(term))
                    small_indx.append(term_cnt)
                term_cnt += 1

            ###############
            # big_occurence_matrix = np.zeros((occurence_matrix.shape[0],len(big_term_arr)))

            # big_occurence_matrix[:,indx] = occurence_matrix
            ###############
            # reduced_train_X = train_X[:,big_indx]
            # reduced_train_X = train_X

            consistant_occurence_matrix = np.zeros((occurence_matrix.shape[0], train_X.shape[1]))
            consistant_occurence_matrix[:, big_indx] = occurence_matrix[:, small_indx]

            likelihood, prior = NaiveBayes_train(train_X, train_Y, 1)
            predict = np.zeros(occurence_matrix.shape[0])

            for i in range(predict.shape[0]):
                predict[i] = NaiveBayes(likelihood, prior, consistant_occurence_matrix[i, :])
            np.save("prediction_for_phas1Data.npy", predict)


        predict = np.load("prediction_for_phas1Data.npy")
        category_query = int(input("input the category of your query: 1,2,3,4"))
        query = input("inout your query: ")
        corrected = ""
        for term in PREPROCESSOR.simple_tokenize_and_remove_junk(query):
            corrected = corrected + " " + Part4.word_correction(term, trie_dict, bigram_ds)
        query_tokens = PREPROCESSOR.simple_tokenize_and_remove_junk(corrected)
        relev_docs = get_related_docId_list_classified(query_tokens, idf_query, term_to_num, doc_space,predict,category_query)
        print("results: ", relev_docs)

    if section_int==3:

        model_int = int(input("Please indicate the model number. 1-Naive Bayes, 2-KNN, 3-SVM, 4-Random Forest"))

        if model_int == 1:

            likelihood, prior = NaiveBayes_train(train_X, train_Y, 1)
            predict = np.zeros_like(test_y)
            for i in range(predict.shape[0]):
                predict[i] = NaiveBayes(likelihood, prior, test_x[i, :])
                print(i)

            print_criterias(predict, test_y)

        if model_int == 2:
            tf_idf = get_tf_idf(train_X)
            K = int(input("Type the value of K: "))
            test_y = test_y
            predict = np.zeros_like(test_y)
            for i in range(predict.shape[0]):
                predict[i] = KNN(K, tf_idf, train_Y, test_x[i, :])
                print(i)

            print_criterias(predict, test_y)

        if model_int == 3:
            C = int(input("Type the value of C: "))
            clf = SVC(gamma='auto', C=C)
            clf.fit(train_X, train_Y)
            predict = clf.predict(test_x)
            print_criterias(predict, test_y)

        if model_int == 4:
            clf = RandomForestClassifier(n_estimators=100)
            clf.fit(train_X, train_Y)
            predict = clf.predict(test_x)
            print_criterias(predict, test_y)

    if section_int==4:
        exit()



