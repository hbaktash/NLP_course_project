import dictionary
import numpy as np

window_size=1000
np.set_printoptions(threshold=np.inf)


###########################

def get_doc_term(trie:dictionary.Trie):

    trie.set_termNum_docNum()
    num_of_terms = trie.term_num
    num_of_docs = trie.doc_num

    term_to_num = {}
    term_list = trie.get_all_terms()
    for i in range(len(term_list)):
        term_to_num[term_list[i]] = i

    term_list = trie.get_all_terms()
    doc_term = np.zeros((num_of_docs+1,num_of_terms))

    for term in term_list:
        posting_list = trie.search_term(term)
        doc_data = posting_list.first_doc_data

        while doc_data:
            doc_id = doc_data.doc_id
            pos_data = doc_data.first_pos_data
            while pos_data:
                doc_term[doc_id,term_to_num[term]]+=1
                pos_data=pos_data.next_pos

            doc_data=doc_data.next


    return doc_term


def vector_space_preprocess(trie:dictionary.Trie):

    trie.set_termNum_docNum()
    num_of_terms = trie.term_num
    num_of_docs = trie.doc_num

    term_to_num = {}
    term_list = trie.get_all_terms()
    for i in range(len(term_list)):
        term_to_num[term_list[i]] = i

    term_list = trie.get_all_terms()
    doc_term = np.zeros((num_of_docs+1,num_of_terms))

    for term in term_list:
        posting_list = trie.search_term(term)
        doc_data = posting_list.first_doc_data

        while doc_data:
            doc_id = doc_data.doc_id
            pos_data = doc_data.first_pos_data
            while pos_data:
                doc_term[doc_id,term_to_num[term]]+=1
                pos_data=pos_data.next_pos

            doc_data=doc_data.next



    ###########
    tf_doc = np.copy(doc_term)
    nonzero_indx = np.nonzero(tf_doc)
    tf_doc[nonzero_indx] -= 1
    tf_doc += 1
    tf_doc = np.log(tf_doc)
    tf_doc[nonzero_indx] += 1

    #tf_doc = np.log(doc_term+1)+1
    idf_doc = np.ones((1,num_of_terms))
    doc_space = tf_doc*idf_doc
    doc_space=doc_space/(np.sqrt((doc_space**2).sum(axis=1).reshape(-1,1))+1e-20)

    idf_query = np.zeros_like(doc_term)
    idf_query[np.nonzero(doc_term)]=1
    idf_query = idf_query.sum(0).reshape(1,-1)
    idf_query = np.log(num_of_docs/idf_query)

    return doc_space,idf_query,term_to_num

def check_window_proximity(query_tokens_array,doc_id,trie):

    occurrence_list = []

    for term in query_tokens_array:
        posting_list = trie.search_term(term)
        doc_data=posting_list.first_doc_data
        while doc_data:
            if doc_data.doc_id == doc_id:
                pos_data = doc_data.first_pos_data
                while pos_data:
                    occurrence_list.append((term,pos_data.position))
                    pos_data = pos_data.next_pos
            doc_data=doc_data.next

    occurrence_list.sort(key=lambda tup: tup[1], reverse=False)

    begin_itr=0

    while begin_itr< len(occurrence_list):

        InWindow_Term_Set = set()
        end_itr=begin_itr

        while end_itr< len(occurrence_list) and occurrence_list[end_itr][1]-occurrence_list[begin_itr][1] < window_size:
            term = occurrence_list[end_itr][0]
            InWindow_Term_Set.add(term)
            end_itr+=1

        if len(InWindow_Term_Set)==len(query_tokens_array):
            return True
        begin_itr+=1

    return False

def get_related_docId_list(query_tokens_array,idf_query,term_to_num,doc_space):
    query_vector = np.zeros_like(idf_query)
    for token in query_tokens_array:
        query_vector[0,term_to_num[token]]+=1

    #####
    nonzero_indx = np.nonzero(query_vector)
    query_vector[nonzero_indx] -= 1
    query_vector += 1
    query_vector = np.log(query_vector)
    query_vector[nonzero_indx] += 1

    #####
    query_vector = query_vector*idf_query
    query_vector = query_vector/ np.sqrt((query_vector**2).sum())
    query_vector = query_vector.reshape(1,-1)
    #print(query_vector)
    #exit()
    score_arr = (query_vector * doc_space).sum(1)
    related_docId_list = (-score_arr).argsort()[1:11]
    return related_docId_list

def get_related_docId_list_proximity_version(query_tokens_array,idf_query,term_to_num,doc_space,trie):


    query_vector = np.zeros_like(idf_query)
    for token in query_tokens_array:
        query_vector[0,term_to_num[token]]+=1

    #####
    nonzero_indx = np.nonzero(query_vector)
    query_vector[nonzero_indx] -= 1
    query_vector += 1
    query_vector = np.log(query_vector)
    query_vector[nonzero_indx] += 1
    #####

    query_vector=query_vector*idf_query
    query_vector = query_vector/ (np.sqrt((query_vector**2).sum()))
    query_vector =  query_vector.reshape(1,-1)
    score_arr = (query_vector * doc_space).sum(1)
    #####
    for doc_id in range(1,doc_space.shape[0]):
       if not check_window_proximity(query_tokens_array,doc_id,trie):
           score_arr[doc_id]=0

    #####
    related_docId_list = (-score_arr).argsort()[1:11]

    return related_docId_list






trie = dictionary.build_english_dictionary()
doc_space,idf_query,term_to_num = vector_space_preprocess(trie)

#print(doc_space[1])
query_tokens_array=['writer']

related_doc_id = get_related_docId_list_proximity_version(query_tokens_array,idf_query,term_to_num,doc_space,trie)
doc_term = get_doc_term(trie)
most_related_doc = related_doc_id[0]
term_index = term_to_num['writer']
print(related_doc_id)
# for docId in related_doc_id:
#     print(doc_term[docId,term_index],doc_term[:,term_index].max())




