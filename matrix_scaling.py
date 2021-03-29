import numpy as np


# Набор функций для построения матрицы алгебраических дополнений

def minor_of_element(a, i, j):
    sub_a = np.delete(a, i - 1, 0)
    sub_a = np.delete(sub_a, j - 1, 1)
    M_ij = np.linalg.det(sub_a)
    return np.around(M_ij, decimals=3)


def minor_matrix(a):
    m = np.shape(a)[0]
    M_a = np.zeros([m, m])
    for i in range(1, m + 1):
        for j in range(1, m + 1):
            M_a[i - 1, j - 1] = minor_of_element(a, i, j)
    return M_a


def cofactor_matrix(a):
    m = np.shape(a)[0]  # Order of the matrix
    C_a = np.zeros([m, m])  # Initializing the cofactor matrix with zeros
    for i in range(1, m + 1):
        for j in range(1, m + 1):
            C_a[i - 1, j - 1] = pow(-1, i + j) * minor_of_element(a, i, j)
    return C_a
