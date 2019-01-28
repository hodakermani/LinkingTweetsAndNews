class Text:
    lastIndex = -1

    def __init__(self, text):
        Text.lastIndex += 1
        self.index = Text.lastIndex
        self.text = text
        self.neighbours = set()

    def add_neighbour_with_index(self, index):
        self.neighbours.add(index)

    def add_neighbour(self, neighbour):
        if neighbour.index != self.index:
            self.neighbours.add(neighbour.index)

    def add_neighbours(self, neighbours):
        for neighbour in neighbours:
            self.add_neighbour(neighbour)

    def __str__(self):
        return self.text
