import numpy as np

from src.matrix import DenseMatrix
from sklearn.metrics.pairwise import cosine_similarity


class LatentModel:
    def __init__(self, path):
        self.matrix = DenseMatrix()
        self.matrix.load_from_file(path)
        self.cosine_similarity_matrix = []
        self.mat = []

    def calculate_cosine_matrix(self, num_of_texts, num_of_tweets, num_of_news):
        mat = np.array(self.matrix.data)
        mat = mat[:(num_of_tweets + num_of_news), ]
        self.cosine_similarity_matrix = cosine_similarity(mat, mat)

    def cosine_similarity(self, text_a_index, text_b_index):
        return self.cosine_similarity_matrix[text_a_index, text_b_index]
