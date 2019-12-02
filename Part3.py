
import bitstring
import dictionary
import pickle
from pympler import asizeof


def get_varible_byte(int_num):

    fliped_byte_array = bytearray()
    quotient = int_num

    while(quotient>0):
        remainder = quotient%128
        quotient = int(quotient/128)
        fliped_byte_array.append(remainder)
    if int_num==0:
        fliped_byte_array.append(0)

    fliped_byte_array[0] = fliped_byte_array[0] + 128
    res_byte_array = bytearray()

    while(len(fliped_byte_array)>0):
        res_byte_array.append(fliped_byte_array.pop())


    return bytes(res_byte_array)

def get_gamma_bit(int_num):
    int_num = int_num+1
    offset_len=0
    while(int_num>=2**offset_len):
        offset_len=offset_len+1
    ofset_part = bitstring.BitArray(int=int_num,length=offset_len+1)
    ofset_part = ofset_part[2:]
    length_part = bitstring.BitArray(int=2**(offset_len-1)-1,length=offset_len)[1:]
    length_part._append(bitstring.BitArray(bin='0b0'))
    res = length_part+ofset_part
    return res

def decipher_pos_bits(bits:bitstring.BitArray):
    print(bits.bin)

    position_list = []
    position_acm = 0
    i=0
    while(i<bits.len):
        offset_length=0
        while (bits[i]):
            offset_length = offset_length + 1
            i = i + 1
        i = i + 1
        position_gap_int = (bitstring.BitArray(bin='0b01') + bits[i:i + offset_length]).int-1
        i = i + offset_length
        position_acm += position_gap_int
        position_list.append(position_acm)
    return position_list


def compress_VB(trie:dictionary.Trie):

    term_list = trie.get_all_terms()

    level_0_byte_array = {}
    level_1_byte_array = bytearray()
    level_2_byte_array = bytearray()

    level2_gap_byte_counter=0

    for term in term_list:

        level_0_byte_array[term]=len(level_1_byte_array)

        previous_doc_id=0
        posting_list = trie.search_term(term)
        doc_data = posting_list.first_doc_data
        while doc_data is not None:
            doc_id = doc_data.doc_id
            doc_id_gap = doc_id - previous_doc_id
            previous_doc_id=doc_id
            bytes_of_doc_id = get_varible_byte(doc_id_gap)
            level_1_byte_array.extend(bytes_of_doc_id)
            level_1_byte_array.extend(get_varible_byte(level2_gap_byte_counter))


            level2_gap_byte_counter = 0
            previous_position = 0

            pos_data = doc_data.first_pos_data
            while pos_data is not None:
                position = pos_data.position
                gap_position = position-previous_position
                previous_position=position
                bytes_of_position = get_varible_byte(gap_position)
                level_2_byte_array.extend(bytes_of_position)
                level2_gap_byte_counter+=len(bytes_of_position)
                pos_data=pos_data.next_pos
            doc_data=doc_data.next

    return level_0_byte_array,level_1_byte_array,level_2_byte_array

def compress_gamma(trie:dictionary.Trie):

    term_list = trie.get_all_terms()
    level_0_bit_array = {}
    level_1_bit_array = bitstring.BitArray()
    level_2_bit_array = bitstring.BitArray()

    level2_gap_bit_counter=0

    for term in term_list:

        level_0_bit_array[term]=level_1_bit_array.len
        previous_doc_id=0

        posting_list = trie.search_term(term)
        doc_data = posting_list.first_doc_data

        while doc_data is not None:
            doc_id = doc_data.doc_id

            doc_id_gap = doc_id - previous_doc_id
            previous_doc_id=doc_id
            level_1_bit_array += get_gamma_bit(doc_id_gap)
            level_1_bit_array += get_gamma_bit(level2_gap_bit_counter)

            level2_gap_bit_counter = 0
            previous_position = 0
            position_data = doc_data.first_pos_data
            while position_data is not None:
                position = position_data.position
                gap_position = position-previous_position
                previous_position=position
                bits_of_position = get_gamma_bit(gap_position)
                level_2_bit_array += bits_of_position
                level2_gap_bit_counter+=bits_of_position.len
                position_data=position_data.next_pos

            doc_data=doc_data.next

    return level_0_bit_array,level_1_bit_array,level_2_bit_array

def decompress_gamma(level_0_bit_array,level_1_bit_array:bitstring.BitArray,level_2_bit_array:bitstring.BitArray):


    word_list = list(level_0_bit_array.keys())
    word_list.sort()


    word_counter = 0

    dic_of_word_to_docIdList={}
    dic_of_word_to_ptrList = {}

    docId_list=[]
    ptr_list=[]
    docId_counter=0
    ptr_counter=0
    i=0

    while i < level_1_bit_array.len:

        if word_counter+1<len(word_list) and i>= level_0_bit_array[word_list[word_counter+1]]:
            dic_of_word_to_docIdList[word_list[word_counter]] = docId_list
            dic_of_word_to_ptrList[word_list[word_counter]] = ptr_list
            docId_list=[]
            ptr_list = []
            word_counter=word_counter+1
            docId_counter=0


        offset_length = 0
        while(level_1_bit_array[i]):
            offset_length = offset_length + 1
            i=i+1
        i=i+1
        doc_id_gap_int = (bitstring.BitArray(bin='0b01') + level_1_bit_array[i:i+offset_length]).int-1
        i=i+offset_length
        docId_counter+=doc_id_gap_int
        docId_list.append(docId_counter)

        offset_length = 0
        while (level_1_bit_array[i]):
            offset_length = offset_length + 1
            i = i + 1
        i = i + 1
        leve2_ptr_gap_int = (bitstring.BitArray(bin='0b01') + level_1_bit_array[i:i + offset_length]).int-1
        i = i + offset_length
        ptr_counter+=leve2_ptr_gap_int
        ptr_list.append(ptr_counter)

    dic_of_word_to_docIdList[word_list[word_counter]] = docId_list
    dic_of_word_to_ptrList[word_list[word_counter]] = ptr_list
    word_counter=word_counter+1


    result_trie =  dictionary.Trie()

    for word_itr in range(word_counter):

        word = word_list[word_itr]
        docId_list = dic_of_word_to_docIdList[word]
        ptr_list   = dic_of_word_to_ptrList[word]

        for doc_itr in range(len(docId_list)):

            begin_indx = ptr_list[doc_itr]
            if doc_itr < len(docId_list)-1:
                end_indx = ptr_list[doc_itr+1]

            elif word_itr<word_counter-1:
                end_indx = dic_of_word_to_ptrList[word_list[word_itr+1]][0]
            else:
                end_indx = level_2_bit_array.len



            pos_bits = level_2_bit_array[begin_indx:end_indx]

            position_list = decipher_pos_bits(pos_bits)
            #
            for position_int in  position_list:
                result_trie.add_term(word,docId_list[doc_itr],position_int)

    #return dic_of_word_to_docIdList
    return result_trie

def check_equality_tri(orginal_trie:dictionary.Trie,recovered_trie:dictionary.Trie):

    term_list = orginal_trie.get_all_terms()

    for term in term_list:

        recovered_posting_list =  recovered_trie.search_term(term)
        original_posting_list = orginal_trie.search_term(term)

        orginal_doc_data = original_posting_list.first_doc_data
        recovered_doc_data = recovered_posting_list.first_doc_data

        while orginal_doc_data:
            orginal_pos_data = orginal_doc_data.first_pos_data
            recovered_pos_data = recovered_doc_data.first_pos_data

            while orginal_pos_data:
                if orginal_pos_data.position != recovered_pos_data.position:
                    print("positions are not identical")
                    return False
                orginal_pos_data=orginal_pos_data.next_pos
                recovered_pos_data = recovered_pos_data.next_pos

            if recovered_pos_data is not None:
                print("recovered position list is longer")
                return False
            orginal_doc_data=orginal_doc_data.next
            recovered_doc_data=recovered_doc_data.next

        if recovered_doc_data is not None:
            print("recovered doc list is longer")
            return False

    return True


def save_bitstring(bits:bitstring.BitArray,file_name):
    margin  = 8-(bits.len % 8)
    margin_bits = bitstring.BitArray(int=margin,length=8)+bitstring.BitArray(int=0,length=margin)
    margined_bits = margin_bits+bits
    f = open(file_name, 'wb')
    f.write(margined_bits.tobytes())
    #print("!!",margined_bits.tobytes())
    f.close()

def load_bitsring(file_name):
    f = open(file_name, 'rb')
    margined_bytes = f.read()
    f.close()
    #print("!!!",margined_bytes)
    bits = bitstring.BitArray(bytes=margined_bytes)
    print()
    margin =  bits[0:8].int
    unmargined_bits = bits[8+margin:]
    return unmargined_bits



def part3_1and2():
    english_trie = dictionary.build_english_dictionary()
    a0,a1,a2 = compress_VB(english_trie)
    ByteSize_VB = len(a1)+len(a2)

    a0, a1, a2 = compress_gamma(english_trie)
    ByteSize_gamma = int((a1.len + a2.len)/8)
    ByteSize_initial = asizeof.asizeof(english_trie)
    print("Engilish Corpus:","        Whole Initial ByteSize=  ",ByteSize_initial,"     VB ByteSize=  ",ByteSize_VB,"     gamma ByteSize=  ",ByteSize_gamma,"     term_to_ptr ByteSize =  ",asizeof.asizeof(a0))

def part3_3():
    orginal_trie = dictionary.build_english_dictionary()

    ### compress and save part
    a0, a1, a2 = compress_gamma(orginal_trie)
    save_bitstring(a1, "a1.txt")
    save_bitstring(a2, "a2.txt")
    f = open("a0.pkl", "wb")
    pickle.dump(a0, f)
    f.close()
    print("Posting Lists Compressed and Saved in a0.pkl, a1.txt, a2.txt")

    ### load and decompress part
    a1 = load_bitsring("a1.txt")
    a2 = load_bitsring("a2.txt")
    f = open("a0.pkl", "rb")
    a0 = pickle.load(f)
    f.close()
    recovered_trie =  decompress_gamma(a0, a1,a2)
    print("Posting Lists Compressed and Loaded and Decompressed")

    if check_equality_tri(orginal_trie, recovered_trie):
        print("Orginal Version and Recovered Version Are Identical")
    else:
        print("Orginal Version and Recovered Version Are Not Identical!!!")











