class Posting_list:
    def __init__(self, term: str):
        self.term = term
        self.first_doc_data = None

    def __str__(self):
        if self.first_doc_data is None:
            return "[empty]"
        else:
            current_doc_data = self.first_doc_data
            ans = ""
            while not(current_doc_data is None):
                ans += str(current_doc_data.doc_id) + ", "
                current_doc_data = current_doc_data.next
        return ans

    def to_list(self):
        if self.first_doc_data is None:
            return []
        else:
            current_doc_data = self.first_doc_data
            ans = []
            while not(current_doc_data is None):
                ans.append((current_doc_data.doc_id, current_doc_data.tf))
                current_doc_data = current_doc_data.next
        return ans

    def add_new_doc_data(self, doc_id, pos):
        if self.first_doc_data is None:
            self.first_doc_data = Doc_data(doc_id, pos)
        else:
            current_doc_data = self.first_doc_data
            while True:
                # print("         :", current_doc_data.doc_id)
                if current_doc_data.doc_id == doc_id:
                    # print("         1")
                    current_doc_data.add_pos(pos)
                    break
                elif doc_id < current_doc_data.doc_id:
                    # print("         2")
                    new_doc_data = Doc_data(doc_id, pos)
                    new_doc_data.next = current_doc_data
                    self.first_doc_data = new_doc_data
                    break
                elif current_doc_data.next is None:
                    # print("         3")
                    new_doc_data = Doc_data(doc_id, pos)
                    current_doc_data.next = new_doc_data
                    break
                elif current_doc_data.doc_id < doc_id < current_doc_data.next.doc_id:
                    # print("         4")
                    new_doc_data = Doc_data(doc_id, pos)
                    new_doc_data.next = current_doc_data.next
                    current_doc_data.next = new_doc_data
                    break
                else:
                    current_doc_data = current_doc_data.next

    def remove_doc_data(self, doc_id:int):
        current_doc_data = self.first_doc_data
        prev_doc_data = None
        first = True
        found = False
        while True:
            if current_doc_data.doc_id == doc_id:
                found = True
                if first:
                    self.first_doc_data = current_doc_data.next
                    break
                else:
                    prev_doc_data.next = current_doc_data.next
                    break
            first = False
            prev_doc_data = current_doc_data
        if not found:
            print("term {} indexing did not contain doc {}".format(self.term, doc_id))


class Doc_data:
    def __init__(self, doc_id: int, position: int):
        self.doc_id: int = doc_id
        self.first_pos_data: Pos_data = Pos_data(position)
        self.tf = 1
        self.next = None

    def add_pos(self, pos: int):
        self.tf += 1
        new_pos_data = Pos_data(pos)
        if self.first_pos_data is None:
            self.first_pos_data = new_pos_data
        elif pos < self.first_pos_data.position:
            new_pos_data.next_pos = self.first_pos_data
            self.first_pos_data = new_pos_data
        else:
            current_pos_data = self.first_pos_data
            while True:
                if current_pos_data.next_pos is None:
                    current_pos_data.next_pos = new_pos_data
                    break
                elif current_pos_data.position < pos < current_pos_data.next_pos.position:
                    new_pos_data.next_pos = current_pos_data.next_pos
                    current_pos_data.next_pos = new_pos_data
                    break
                else:
                    current_pos_data = current_pos_data.next_pos

    def __str__(self):
        if self.first_pos_data is None:
            ans = "[empty]"
        else:
            current_pos_data = self.first_pos_data
            ans = "doc ID " + str(self.doc_id) + ":\n"
            while not(current_pos_data is None):
                ans += str(current_pos_data.position) + ", "
                current_pos_data = current_pos_data.next_pos
        ans += "\n"
        return ans


class Pos_data:
    def __init__(self, position: int):
        self.position: int = position
        self.next_pos = None


