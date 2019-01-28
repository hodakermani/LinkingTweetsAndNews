class SparseMatrix:
    def __init__(self, rows=None, columns=None):
        self.data = []
        self.rows = rows
        self.columns = columns

    def load_from_array(self, array):
        matrix = []
        self.rows = len(array)
        self.columns = len(array[0])
        for i in range(0, len(array)):
            row = {}
            for j in range(0, len(array[i])):
                if array[i][j] != 0:
                    row[j] = array[i][j]
            matrix.append(row)
        self.data = matrix

    def load_from_file(self, path):
        matrix = []
        with open(path) as fp:
            self.rows, self.columns = (int(x) for x in fp.readline().split(' '))
            for line in fp:
                words = line.split(' ')
                row = {}
                if int(words[0]) != 0:
                    pass
                for i in range(1, int(words[0])):
                    row[int(words[i])] = float(words[i + 1])
                matrix.append(row)
        self.data = matrix

    def store_in_file(self, path):
        fp = open(path, '+w')
        fp.write('%d %d\n' % (self.rows, self.columns))
        for i in range(0, self.rows):
            fp.write('%d ' % len(self.data[i]))
            for column in self.data[i]:
                fp.write('%d %f ' % (column, self.data[i][column]))
            fp.write('\n')

    def get_data(self, row, column):
        r = self.data[row]
        if column in r:
            return self.data[row][column]
        return 0

    def add_row(self, indexes_in_row):
        row = {}
        for index in indexes_in_row:
            row[index] = int(1)
        self.data.append(row)


class TFIDF(SparseMatrix):
    def __init__(self):
        super().__init__()

    def set_size(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def store_weights_in_file(self, path):
        fp = open(path, '+w')
        fp.write('%d %d\n' % (self.rows, self.columns))
        for i in range(0, self.rows):
            fp.write('%d ' % len(self.data[i]))
            for column in self.data[i]:
                if self.data[i][column] != 0:
                    fp.write('%d %d ' % (column, 1))
            fp.write('\n')

    def add_row(self, indexes_in_row):
        row = {}
        sorted_indexes = sorted(indexes_in_row.keys())
        for index in sorted_indexes:
            row[index] = indexes_in_row[index]
        self.data.append(row)


class DenseMatrix:
    def load_from_file(self, path):
        matrix = []
        with open(path) as fp:
            self.rows, self.columns = (int(x) for x in fp.readline().split(' '))
            for line in fp:
                words = line.split(' ')
                row = []
                for i in range(0, self.columns):
                    row.append(float(words[i]))
                matrix.append(row)
        self.data = matrix

    def store_in_file(self, path):
        fp = open(path, '+w')
        fp.write('%d %d\n' % (self.rows, self.columns))
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                fp.write('%d ' % self.data[i][j])
            fp.write('\n')

    def __getitem__(self, item):
        return self.data[item]


class SparseAdjacencyMatrix(SparseMatrix):
    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns

    def store_in_file(self, path):
        fp = open(path, '+w')
        fp.write('%d %d\n' % (self.rows, self.columns))
        for i in range(0, self.rows):
            fp.write('%d ' % len(self.data[i]))
            for column in self.data[i]:
                fp.write('%d %d ' % (column, self.data[i][column]))
            fp.write('\n')

    def add_row(self, indexes_in_row):
        row = {}
        for index in indexes_in_row:
            row[index] = int(1)
        self.data.append(row)
