from dictionary import Trie_node
import english_preprocessing


class Bigram:
    def __init__(self):
        self.bis_dict: dict = {}

    def add_bi_data(self, bi: str, trie_node: Trie_node):
        if bi in self.bis_dict:
            if trie_node.term in self.bis_dict[bi]:
                pass
            else:
                self.bis_dict[bi].append(trie_node)
        else:
            self.bis_dict[bi] = [trie_node]

    def add_bis_in_term(self, term: str, trie_node: Trie_node):
        if len(term) > 1:
            for i in range(len(term)-1):
                self.add_bi_data(term[i:i+2], trie_node)