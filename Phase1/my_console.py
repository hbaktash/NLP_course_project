from Phase1 import dictionary, Part3, part5, persian_preproccessing, english_preprocessing, file_handler, Part4


def main():
    global term_to_num, idf_query, doc_space, bigram_ds, trie_dict
    input("press any button!")
    dic_is_built = False
    while True:
        lang = int(input("choose language:\n"
                         "1- english\n"
                         "2- persian"))
        if lang == 1:
            PREPROCESSOR = english_preprocessing
            all_docs_and_titles = file_handler.load_english_file()
        else:
            PREPROCESSOR = persian_preproccessing
            all_docs_and_titles = file_handler.load_persian_file()
        command: int = int(input("choose:\n"
                                 "1- pre process my text\n"
                                 "2- show frequent words\n"
                                 "3- go to dict\n"))
        if command == 1:
            text = (input("enter your text:\n"))
            print("**pre processed:", PREPROCESSOR.pre_process_text(text))
        elif command == 2:
            rank = int(input("how many?"))
            tf_token_pairs = PREPROCESSOR.get_all_docs_tf_tokens()
            for pair in tf_token_pairs[:rank]:
                print(pair[0], ": ", pair[1])
        elif command == 3:
            if not dic_is_built:
                print("building dict...")
                trie_dict, bigram_ds = dictionary.build_dictionary(lang)
                doc_space, idf_query, term_to_num = part5.vector_space_preprocess(trie_dict)
                dic_is_built = True
            command2 = int(input("1- show posting for my word\n"
                                 "2- show positions of word in all docs\n"
                                 "3- remove the doc\n"
                                 "4- correct query\n"
                                 "5- test compression \n"
                                 "6- test compression recoverability\n"
                                 "7- search query\n"
                                 "8- search query (proximity)"))
            if command2 == 1:
                word = input("enter the word:\n")
                dictionary.show_posting_list(word, trie_dict)
            elif command2 == 2:
                word = input("enter the word:\n")
                dictionary.show_positions_in_all_docs(word, trie_dict)
            elif command2 == 3:
                doc_id = int(input("enter doc id:"))
                dictionary.remove_doc(all_docs_and_titles, doc_id, trie_dict)
            elif command2 == 4:
                query = input("enter [bad] query:")
                corrected = ""
                for term in PREPROCESSOR.simple_tokenize_and_remove_junk(query):
                    corrected = corrected + " " + Part4.word_correction(term, trie_dict, bigram_ds)
                print("corrected: ", corrected)
            elif command2 == 5:
                Part3.part3_1and2(trie_dict)
            elif command2 == 6:
                Part3.part3_3(trie_dict)
            elif command2 == 7:
                query = input("inout your query: ")
                corrected = ""
                for term in PREPROCESSOR.simple_tokenize_and_remove_junk(query):
                    corrected = corrected + " " + Part4.word_correction(term, trie_dict, bigram_ds)
                query_tokens = PREPROCESSOR.simple_tokenize_and_remove_junk(corrected)
                relev_docs = part5.get_related_docId_list(query_tokens, idf_query, term_to_num, doc_space)
                print("results: ", relev_docs)
            elif command2 == 8:
                query = input("inout your query: ")
                corrected = ""
                for term in PREPROCESSOR.simple_tokenize_and_remove_junk(query):
                    corrected = corrected + " " + Part4.word_correction(term, trie_dict, bigram_ds)
                query_tokens = PREPROCESSOR.simple_tokenize_and_remove_junk(corrected)
                relev_docs = part5.get_related_docId_list_proximity_version(query_tokens, idf_query, term_to_num, doc_space, trie_dict)
                print("results: ", relev_docs)


main()
