import hazm
import nltk
import file_handler

ALPHA = 0.008


def get_all_english_docs_tf_tokens():
    titles_and_text = file_handler.load_english_file()
    total_combined_tf_pairs = []
    for doc_pair in titles_and_text:
        current_tf_pairs = pre_process_text(doc_pair[1]+" "+doc_pair[0], with_tf=True)
        # print(total_combined_tf_pairs)
        # print(current_tf_pairs)
        total_combined_tf_pairs = combine_tf_tokens(total_combined_tf_pairs,
                                                    current_tf_pairs)
    total_combined_tf_pairs.sort(key=lambda x: x[1], reverse=True)
    total_words = sum([tf_pair[1] for tf_pair in total_combined_tf_pairs])
    print(total_words)
    ans = [tf_pair for tf_pair in total_combined_tf_pairs if tf_pair[1] <= ALPHA*total_words]
    return ans


def combine_tf_tokens(tft1: list, tft2: list):
    positions_dict = {}
    term_frequency_pairs = []
    i = 0
    for tf_pair in tft1:
        positions_dict[tf_pair[0]] = i
        i += 1
        term_frequency_pairs.append(tf_pair)
    for tf_pair in tft2:
        if tf_pair[0] in positions_dict:
            pair = term_frequency_pairs[positions_dict[tf_pair[0]]]
            term_frequency_pairs[positions_dict[tf_pair[0]]] = (pair[0], pair[1] + tf_pair[1])
        else:
            positions_dict[tf_pair[0]] = i
            i += 1
            term_frequency_pairs.append(tf_pair)
    return term_frequency_pairs


def pre_process_text(text: str, with_tf=False):
    normal_text = normalize(text)
    simple_tokens = simple_tokenize_and_remove_junk(normal_text)
    simple_stemmed_tokens = [stem(token) for token in simple_tokens]
    tf_tokens_no_stopwords = remove_stopwords(simple_stemmed_tokens, alpha=1)
    final_words = [pair[0] for pair in tf_tokens_no_stopwords]
    if with_tf:
        ans = tf_tokens_no_stopwords
    else:
        ans = final_words
    return ans


def normalize(text: str):
    return text.lower()


def simple_tokenize_and_remove_junk(text: str):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens


def tokens_with_tf(tokens: list):
    positions_dict = {}
    term_frequencies = []
    i = 0
    for token in tokens:
        if token in positions_dict:
            tf_pair = term_frequencies[positions_dict[token]]
            term_frequencies[positions_dict[token]] = (tf_pair[0], tf_pair[1] + 1)
        else:
            positions_dict[token] = i
            i += 1
            term_frequencies.append((token, 1))
    return term_frequencies


def remove_stopwords(simple_tokens: list, alpha: float):
    tf_list = tokens_with_tf(simple_tokens)
    tf_list.sort(key=lambda x: x[1])
    tf_threshold = int(len(simple_tokens) * alpha)
    return [tf_pair for tf_pair in tf_list if tf_pair[1] <= tf_threshold]


def stem(word: str):
    return nltk.stem.PorterStemmer().stem(word)


# print(get_all_english_docs_tf_tokens())
