class OrderedSet:
    """A set (doesn't have the same functionality) that supports adding and popping. All data can be accessed with an
    index. """
    def __init__(self, collection=()):
        self.data = list(set(collection))

    def add(self, value):
        if value not in self.data:
            self.data.append(value)
            return True
        return False

    def pop(self, index: int):
        if not isinstance(index, int):
            raise ValueError("Please enter an integer")
        return self.data.pop(index)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        if not isinstance(index, int):
            raise ValueError("Please enter an integer")
        return self.data[index]

    def __repr__(self):
        return str(self.data)
