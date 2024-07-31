import numpy as np
from PIL import Image, ImageDraw

def load_obj(file_path):
    vertices, faces = [], []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append([float(x) for x in line.strip().split()[1:]])
            elif line.startswith('f '):
                face = [int(x.split('/')[0]) - 1 for x in line.strip().split()[1:]]
                faces.append(face)
    return np.array(vertices), faces

def translate(vertices, tx, ty, tz):
    translation_matrix = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ translation_matrix.T)[:, :3]

def scale(vertices, sx, sy, sz):
    scaling_matrix = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ scaling_matrix.T)[:, :3]

def rotate_x(vertices, angle):
    rad = np.radians(angle)
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rad), -np.sin(rad), 0],
        [0, np.sin(rad), np.cos(rad), 0],
        [0, 0, 0, 1]
    ])
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ rotation_matrix.T)[:, :3]

def rotate_y(vertices, angle):
    rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(rad), 0, np.sin(rad), 0],
        [0, 1, 0, 0],
        [-np.sin(rad), 0, np.cos(rad), 0],
        [0, 0, 0, 1]
    ])
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ rotation_matrix.T)[:, :3]

def rotate_z(vertices, angle):
    rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(rad), -np.sin(rad), 0, 0],
        [np.sin(rad), np.cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    vertices_homogeneous = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    return (vertices_homogeneous @ rotation_matrix.T)[:, :3]

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
