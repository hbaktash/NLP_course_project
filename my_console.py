import file_handler
import dictionary
import indexing
import english_preprocessing


def main():
    input("press any button!")
    dic_is_built = False
    while True:
        command: int = int(input("choose:\n"
                                 "1- pre process my text\n"
                                 "2- show frequent words\n"
                                 "3- go to dict\n"))
        if command == 1:
            text = (input("enter your text:\n"))
            print("**pre processed:", english_preprocessing.pre_process_text(text))
        elif command == 2:
            rank = int(input("how many?"))
            tf_token_pairs = english_preprocessing.get_all_english_docs_tf_tokens()
            for pair in tf_token_pairs[:rank]:
                print(pair[0], ": ", pair[1])
        elif command == 3:
            all_docs_and_titles = file_handler.load_english_file()
            if not dic_is_built:
                print("building dict...")
                trie_dict,_ = dictionary.build_english_dictionary()
                dic_is_built = True
            command2 = int(input("1- show posting for my word\n"
                                 "2- show positions of word in all docs\n"
                                 "3- remove the doc"))
            if command2 == 1:
                word = input("enter the word:\n")
                dictionary.show_posting_list(word, trie_dict)
            elif command2 == 2:
                word = input("enter the word:\n")
                dictionary.show_positions_in_all_docs(word, trie_dict)
            elif command2 == 3:
                doc_id = int(input("enter doc id:"))
                dictionary.remove_doc(all_docs_and_titles, doc_id, dictionary)

main()
