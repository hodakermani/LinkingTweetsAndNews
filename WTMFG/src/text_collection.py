import numpy as np

from src.matrix import TFIDF, SparseAdjacencyMatrix


class TextCollection:
    def __init__(self):
        self.num_of_text = 0
        self.num_of_words = 0
        self.tf_idf_matrix = TFIDF()

    def load_text(self, text_file_path, vocab_file_path, tf_idf_file_path):
        with open(text_file_path) as fp:
            self.num_of_text = len(fp.readlines())
        with open(vocab_file_path) as fp:
            self.num_of_words = len(fp.readlines()) - 1
        self.tf_idf_matrix.set_size(self.num_of_text, self.num_of_words)
        tf_idf_matrix_file = np.loadtxt(tf_idf_file_path, usecols=range(3))
        row = {}
        last_text_index = 0
        i = 1
        for line in tf_idf_matrix_file:
            word_index = int(line[0])
            text_index = int(line[1])
            tf_idf_value = line[2]
            if last_text_index != 0 and text_index != last_text_index:
                i = i + 1
                self.tf_idf_matrix.add_row(row)
                row = {}
                while i < text_index:
                    i = i + 1
                    self.tf_idf_matrix.add_row({})
            row[word_index-1] = tf_idf_value
            last_text_index = text_index
        self.tf_idf_matrix.add_row(row)

    def save_tf_idf_matrix(self, path):
        self.tf_idf_matrix.store_in_file(path)

    def save_weight_matrix(self, path):
        self.tf_idf_matrix.store_weights_in_file(path)

    def save_adjacency_matrix(self, path):
        adjacency_matrix = SparseAdjacencyMatrix(self.num_of_text, self.num_of_words)
        adjacency_matrix.store_in_file(path)
