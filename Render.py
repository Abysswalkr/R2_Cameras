import pygame
from pygame.locals import *
from Gl import *
from Model import Model
from Shaders import vertex_shader

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
rend = Render(screen)
rend.vertexShader = vertex_shader

model = Model('face.obj')
model.translate[2], model.translate[0], model.scale[0], model.scale[1], model.scale[2] = -10, -2, 0.1, 0.1, 0.1

rend.models.append(model)

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
                model.scale[0] += 1
                model.scale[1] += 1
                model.scale[2] += 1
            elif event.key == pygame.K_0:
                model.scale[0] -= 1
                model.scale[1] -= 1
                model.scale[2] -= 1

    rend.glClear()
    rend.glRender()
    rend.glGenerateFrameBuffer("output.bmp")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
