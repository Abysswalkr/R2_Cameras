from MathLib import *
import numpy as np

class Camera:
    def __init__(self):
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def get_view_matrix(self):
        translateMat = TranslationMatrix(*self.translate)
        rotateMat = RotationMatrix(*self.rotate)
        camMatrix = matrix_multiply(translateMat, rotateMat)
        return np.linalg.inv(camMatrix).tolist()
