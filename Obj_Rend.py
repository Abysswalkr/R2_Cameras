import os
import numpy as np
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from PIL import Image, ImageDraw
from Gl import Render
from Model import Model
from Shaders import vertexShader
from MathLib import TranslationMatrix, ScaleMatrix, RotationMatrix

def load_obj(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append([float(x) for x in line.strip().split()[1:]])
            elif line.startswith('f '):
                face = [int(x.split('/')[0]) - 1 for x in line.strip().split()[1:]]
                faces.append(face)

    return np.array(vertices), faces

def translate(vertices, tx, ty, tz):
    translation_matrix = TranslationMatrix(tx, ty, tz)
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ np.array(translation_matrix).T)[:, :3]

def scale(vertices, sx, sy, sz):
    scaling_matrix = ScaleMatrix(sx, sy, sz)
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ np.array(scaling_matrix).T)[:, :3]

def rotate(vertices, angle, axis):
    if axis == 'x':
        rotation_matrix = RotationMatrix(angle, 0, 0)
    elif axis == 'y':
        rotation_matrix = RotationMatrix(0, angle, 0)
    elif axis == 'z':
        rotation_matrix = RotationMatrix(0, 0, angle)
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ np.array(rotation_matrix).T)[:, :3]

def draw_model(vertices, faces, image_size=500):
    img = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(img)

    vertices_2d = vertices[:, :2]
    vertices_2d = (vertices_2d - np.min(vertices_2d)) / (np.max(vertices_2d) - np.min(vertices_2d)) * (image_size - 1)

    for face in faces:
        for i in range(len(face)):
            v0 = vertices_2d[face[i]]
            v1 = vertices_2d[face[(i + 1) % len(face)]]
            draw.line([tuple(v0), tuple(v1)], fill='black')

    img.save('output.bmp')

# Inicializar Pygame y la ventana de renderizado
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
clock = pygame.time.Clock()

rend = Render(screen)
rend.vertexShader = vertexShader

# Cargar modelos y aplicar transformaciones
file_path = 'modelo.obj'
if not os.path.isfile(file_path):
    print(f"Error: El archivo {file_path} no se encuentra.")
else:
    vertices, faces = load_obj(file_path)
    centroid = np.mean(vertices, axis=0)
    vertices = translate(vertices, -centroid[0], -centroid[1], -centroid[2])
    vertices = scale(vertices, 200, 200, 200)
    vertices = translate(vertices, 250, 250, 0)
    vertices = rotate(vertices, 30, 'x')
    vertices = rotate(vertices, 30, 'y')
    draw_model(vertices, faces)

# Cargar el modelo en el renderizador
modelo = Model(file_path)
modelo.translate = [0, 0, -5]
modelo.scale = [0.1, 0.1, 0.1]
rend.models.append(modelo)

# Bucle principal de Pygame
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 1
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 1
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 1
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_3:
                modelo.scale = [x + 0.1 for x in modelo.scale]
            elif event.key == pygame.K_0:
                modelo.scale = [x - 0.1 for x in modelo.scale]

    rend.glClear()
    rend.glRender()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
