import codecs

import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cosine

def read_dense_matrix(file_path):
    file = codecs.open(file_path, mode='r', encoding='utf-8')
    content = file.readlines()
    content = [x.strip() for x in content]
    num_of_rows = int(content[0].split(' ')[0])
    num_of_cols = int(content[0].split(' ')[1])
    matrix = np.ndarray((num_of_rows, num_of_cols), dtype=float)
    for i in range(1, len(content)):
        values = content[i].split(" ")
        for j in range(0, len(values)):
            matrix[i - 1][j] = float(values[j])
    return matrix


m1 = read_dense_matrix('/Users/amir/hodaProject/acl2013/data/model/model.p')
m2 = read_dense_matrix('/Users/amir/hodaProject/acl2013/data/model/smodel.p')

s = 0.0
for i in range(m1.shape[1]):
    s += cosine(m1[:, i].transpose(), m2[:, i].transpose())
print(s)