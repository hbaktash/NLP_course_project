import numpy as np

KK=10 ## number of top scored words in jacard selected for edit distance

def edit_distance(word1,word2):
    dp = -1 * np.ones((len(word1)+1,len(word2)+1))
    for i in range(len(word1)+1):
        dp[i,0]=i
    for i in range(len(word2)+1):
        dp[0,i]=i

    def memoiz(i,j):
        if dp[i,j] == -1:
            dp[i,j]=min(memoiz(i-1,j)+1,memoiz(i,j-1)+1,memoiz(i-1,j-1)+1-int(word1[i-1]==word2[j-1]))
        return dp[i,j]
    memoiz(len(word1),len(word2))
    print(dp)
    return dp[len(word1),len(word2)]

def word_correction(wrong_word,trie):


    bigram_list = wrong_word.bigram_list

    union_map = {}
    intersection_map = {}

    for bigram in bigram_list:
        term_list = bigram.term_list
        for term in term_list:
            if not(term in union_map):
                union_map[term]= set()
            if not(term in intersection_map):
                intersection_map[term]=set()
            intersection_map[term].add(bigram)
            union_map[term].add(bigram)

    for term in list(union_map.keys()):
        for bigram in term.bigram_list:
            union_map[term].add(bigram)

    jaccard_score_list=[]

    for term in list(union_map.keys()):
        jaccard_score_list.append((term,1.0*len(intersection_map[term])/len(union_map[term])))

    jaccard_score_list.sort(key=lambda tup: tup[1],reverse=True)[0:KK]
    editDistance_score_list = []
    for i in range(KK):
        term = jaccard_score_list[i][0]
        editDistance_score_list[i]=(term,edit_distance(wrong_word,term))

    editDistance_score_list.sort(key=lambda tup: tup[1],reverse=False)
    return editDistance_score_list[0][0]



