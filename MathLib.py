from math import pi, sin, cos
import numpy as np

def TranslationMatrix(x, y, z):
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def ScaleMatrix(x, y, z):
    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]

def RotationMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180

    pitchMat = [[1, 0, 0, 0],
                [0, cos(pitch), -sin(pitch), 0],
                [0, sin(pitch), cos(pitch), 0],
                [0, 0, 0, 1]]

    yawMat = [[cos(yaw), 0, sin(yaw), 0],
              [0, 1, 0, 0],
              [-sin(yaw), 0, cos(yaw), 0],
              [0, 0, 0, 1]]

    rollMat = [[cos(roll), -sin(roll), 0, 0],
               [sin(roll), cos(roll), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]

    return matrix_multiply(matrix_multiply(pitchMat, yawMat), rollMat)

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError(
            "Number of columns in the first matrix must be equal to the number of rows in the second matrix.")

    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result

def vector_matrix_multiply(vector, matrix):
    if len(matrix[0]) != len(vector):
        raise ValueError("The number of columns in the matrix must match the size of the vector.")

    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]

    return result

def inversed_matrix(matrix):
    inverse_matrix = np.linalg.inv(matrix)

    return inverse_matrix

def magnitud_vector(A):
    return []

matrix = [
    [2, 5, 7, 6],
    [1, 3, 4, 5],
    [3, 4, 5, 6],
    [5, 7, 8, 9]
]

inverse = inversed_matrix(matrix)
for row in inverse:
    print(row)