from MathLib import *

def vertex_shader(vertex, model_matrix, view_matrix, projection_matrix, viewport_matrix):
    vt = vertex + [1] if len(vertex) + 1 == len(model_matrix) else vertex

    vp_matrix_project_matrix = matrix_multiply(viewport_matrix, projection_matrix)
    vp_matrix_project_matrix_view_matrix = matrix_multiply(vp_matrix_project_matrix, view_matrix)
    vp_matrix_project_matrix_view_matrix_model = matrix_multiply(vp_matrix_project_matrix_view_matrix, model_matrix)

    vt = vector_matrix_multiply(vt, vp_matrix_project_matrix_view_matrix_model)
    return [vt[0]/vt[3], vt[1]/vt[3], vt[2]/vt[3]] if len(vt) > 3 else vt
