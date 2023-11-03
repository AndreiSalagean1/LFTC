class SortedST:
    def __init__(self):
        self.table = []

    def insert(self, key, value):
        # Add the key-value pair to the table ALWAYS in alphabetical order
        self.table.append((key, value))
        self.table.sort(key=lambda item: item[0])

    def searchKey(self, key):
        for k, v in self.table:
            if k == key:
                return v
        return None

    def delete(self, key):
        for i, (k, v) in enumerate(self.table):
            if k == key:
                del self.table[i]
                return

    def size(self):
        return len(self.table)

    def keys(self):
        return [key for key, _ in self.table]

if __name__ == '__main__':
    # Example
    st = SortedST()

    st.insert('id1', 5)
    st.insert('id2', 3)
    st.insert('id3', 8)

    print(st.searchKey('id2'))  # Output: 3
    print(st.searchKey('sadasdasd'))    # Output: None

    st.delete('id2')

    print(st.keys())  # Output: ['id1', 'id3']
    print(st.size())  # Output: 2
