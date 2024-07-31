from Obj import Obj
from MathLib import *

class Model:
    def __init__(self, filename):
        objFile = Obj(filename)
        self.vertices = objFile.vertices
        self.faces = objFile.faces
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [1, 1, 1]

    def get_model_matrix(self):
        translateMat = TranslationMatrix(*self.translate)
        rotateMat = RotationMatrix(*self.rotate)
        scaleMat = ScaleMatrix(*self.scale)
        return matrix_multiply(matrix_multiply(translateMat, rotateMat), scaleMat)
