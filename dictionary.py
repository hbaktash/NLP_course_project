from indexing import Posting_list, Doc_data, Pos_data
import english_preprocessing
import file_handler
import pickle


class Trie:
    def __init__(self):
        self.root = Trie_node("")

    def add_term(self, term: str, doc_id: int, pos: int):
        new_posting_list = Posting_list(term)
        new_posting_list.add_new_doc_data(doc_id, pos)
        current_trie_node = self.root
        for i in range(len(term)):
            if i < len(term) - 1:
                # print("     not there yet***")
                if term[i] in current_trie_node.children:
                    current_trie_node = current_trie_node.children[term[i]]
                else:
                    current_trie_node.children[term[i]] = Trie_node(term[i])
                    current_trie_node = current_trie_node.children[term[i]]
            else:
                # print("     got there###")
                if term[i] in current_trie_node.children:
                    # print("     existed**")
                    current_trie_node = current_trie_node.children[term[i]]
                    if current_trie_node.posting_list is None:
                        current_trie_node.posting_list = new_posting_list
                    else:
                        current_trie_node.posting_list.add_new_doc_data(doc_id, pos)
                else:
                    # print("     existedn't#")
                    current_trie_node.children[term[i]] = Trie_node(term[i])
                    current_trie_node = current_trie_node.children[term[i]]
                    current_trie_node.posting_list = new_posting_list
                break

    def search_term(self, term: str):
        current_trie_node = self.root
        while True:
            for i in range(len(term)):
                if not(term[i] in current_trie_node.children):
                    print("{} not found!!".format(term))
                    return None
                else:
                    if i < len(term) - 1:
                        current_trie_node = current_trie_node.children[term[i]]
                    else:
                        print("found the term: {}".format(term))
                        return current_trie_node.children[term[i]].posting_list

    def delete_term_doc(self, term: str, doc_id: int):
        current_trie_node = self.root
        while True:
            for i in range(len(term)):
                if not(term[i] in current_trie_node.children):
                    print("{} not found!!".format(term))
                    return None
                else:
                    if i < len(term) - 1:
                        current_trie_node = current_trie_node.children[term[i]]
                    else:
                        print("found the term: {}".format(term))
                        return current_trie_node.children[term[i]].posting_list


class Trie_node:
    def __init__(self, char: str):
        self.posting_list = None
        self.char: str = char
        self.children = {}


def add_doc_data(title_and_body: tuple, doc_id: int, trie: Trie):
    title = title_and_body[0]
    body = title_and_body[1]
    stemmed_non_junky_terms = [english_preprocessing.stem(term) for term in
                               english_preprocessing.simple_tokenize_and_remove_junk(body + "" + title)]
    i = 0
    for term in stemmed_non_junky_terms:
        # print("     pos:", i, " ", term)
        trie.add_term(term, doc_id, pos=i)
        i += 1


def remove_doc(title_and_body: tuple, doc_id: int, trie: Trie):
    title = title_and_body[0]
    body = title_and_body[1]
    stemmed_non_junky_terms = [english_preprocessing.stem(term) for term in
                               english_preprocessing.simple_tokenize_and_remove_junk(body + "" + title)]
    all_tf_tokens = english_preprocessing.get_all_english_docs_tf_tokens(alpha=1)
    all_tokens = [tf_pair[0] for tf_pair in all_tf_tokens]
    for term in stemmed_non_junky_terms:
        trie.delete_term_doc(term, doc_id)


def build_english_dictionary():
    trie_dict = Trie()
    titles_and_bodies = file_handler.load_english_file()
    i = 1
    for doc_pair in titles_and_bodies:
        # print(" doc:", i)
        add_doc_data(doc_pair, i, trie_dict)
        i += 1
    return trie_dict


def show_posting_list(term: str, trie_dic: Trie):
    posting_list: Posting_list = trie_dic.search_term(term)
    if not(posting_list is None):
        print(term + ":\n"+posting_list.__str__())


def show_positions_in_all_docs(term: str, trie_dic: Trie):
    posting_list: Posting_list = trie_dic.search_term(term)
    if posting_list is None:
        print("{} not found!".format(term))
    else:
        current_doc_data:Doc_data = posting_list.first_doc_data
        print(current_doc_data.__str__())
        while not(current_doc_data.next is None):
            current_doc_data = current_doc_data.next
            print(current_doc_data.__str__())


#TODO add the remove file handler

# print("building dict")
# trie_dictionary = build_english_dictionary()
# show_posting_list("saturday", trie_dictionary)
# show_positions_in_all_docs("sharon", trie_dictionary)
#
# print("saving dict to file")
# file_handler.save_object_to_file(trie_dictionary, "my_dic.pkl")
