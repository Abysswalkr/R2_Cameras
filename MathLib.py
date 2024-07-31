import numpy as np
from math import pi, sin, cos

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
    pitch *= pi/180
    yaw *= pi/180
    roll *= pi/180

    pitchMat = [[1,0,0,0],
                [0,cos(pitch),-sin(pitch),0],
                [0,sin(pitch),cos(pitch),0],
                [0,0,0,1]]

    yawMat = [[cos(yaw),0,sin(yaw),0],
              [0,1,0,0],
              [-sin(yaw),0,cos(yaw),0],
              [0,0,0,1]]

    rollMat = [[cos(roll),-sin(roll),0,0],
               [sin(roll),cos(roll),0,0],
               [0,0,1,0],
               [0,0,0,1]]

    return matrix_multiply(matrix_multiply(pitchMat, yawMat), rollMat)

def matrix_multiply(A, B):
    return np.dot(A, B).tolist()

def vector_matrix_multiply(vector, matrix):
    return np.dot(matrix, vector).tolist()
