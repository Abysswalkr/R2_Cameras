import struct
from Camera import Camera
from math import tan, pi

def char(c):
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    return struct.pack("=h", w)

def dword(d):
    return struct.pack("=l", d)

POINTS, LINES, TRIANGLES = 0, 1, 2

class Render:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()
        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()
        self.vertexShader = None
        self.primitiveType = POINTS
        self.models = []

    def glViewport(self, x, y, width, height):
        self.vpX, self.vpY, self.vpWidth, self.vpHeight = x, y, width, height
        self.viewportMatrix = [
            [width / 2, 0, 0, x + width / 2],
            [0, height / 2, 0, y + height / 2],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
        ]

    def glProjection(self, n=0.1, f=1000, fov=60):
        aspectRatio = self.vpWidth / self.vpHeight
        fov = fov * pi / 180
        t = tan(fov / 2) * n
        r = t * aspectRatio
        self.projectionMatrix = [
            [n / r, 0, 0, 0],
            [0, n / t, 0, 0],
            [0, 0, -(f + n) / (f - n), -(2 * f * n) / (f - n)],
            [0, 0, -1, 0]
        ]

    def glColor(self, r, g, b):
        self.currentColor = [min(1, max(0, c)) for c in (r, g, b)]

    def glClearColor(self, r, g, b):
        self.clearColor = [min(1, max(0, c)) for c in (r, g, b)]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)
        self.frameBuffer = [[self.clearColor for _ in range(self.height)] for _ in range(self.width)]

    def glPoint(self, x, y, color=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            color = [int(i * 255) for i in (color or self.currentColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    def glLine(self, v0, v1, color=None):
        x0, y0, x1, y1 = int(v0[0]), int(v0[1]), int(v1[0]), int(v1[1])
        dy, dx = abs(y1 - y0), abs(x1 - x0)
        steep = dy > dx

        if steep:
            x0, y0, x1, y1 = y0, x0, y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy, dx = abs(y1 - y0), abs(x1 - x0)
        offset, limit, m = 0, 0.75, dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)
            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    file.write(bytes([color[2], color[1], color[0]]))

    def glRender(self):
        for model in self.models:
            mMat = model.get_model_matrix()
            vertexBuffer = []

            for face in model.faces:
                vertCount = len(face)
                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]

                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix=mMat, viewMatrix=self.camera.get_view_matrix(),
                                           projectionMatrix=self.projectionMatrix, viewportMatrix=self.viewportMatrix)
                    v1 = self.vertexShader(v1, modelMatrix=mMat, viewMatrix=self.camera.get_view_matrix(),
                                           projectionMatrix=self.projectionMatrix, viewportMatrix=self.viewportMatrix)
                    v2 = self.vertexShader(v2, modelMatrix=mMat, viewMatrix=self.camera.get_view_matrix(),
                                           projectionMatrix=self.projectionMatrix, viewportMatrix=self.viewportMatrix)

                    if vertCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix=mMat, viewMatrix=self.camera.get_view_matrix(),
                                               projectionMatrix=self.projectionMatrix, viewportMatrix=self.viewportMatrix)

                vertexBuffer.append(v0)
                vertexBuffer.append(v1)
                vertexBuffer.append(v2)
                if vertCount == 4:
                    vertexBuffer.append(v0)
                    vertexBuffer.append(v2)
                    vertexBuffer.append(v3)

        self.glDrawPrimitives(vertexBuffer)

    def glDrawPrimitives(self, buffer):
        if self.primitiveType == POINTS:
            for point in buffer:
                self.glPoint(int(point[0]), int(point[1]))
        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), 3):
                p0, p1, p2 = buffer[i], buffer[i + 1], buffer[i + 2]
                self.glLine((p0[0], p0[1]), (p1[0], p1[1]))
                self.glLine((p1[0], p1[1]), (p2[0], p2[1]))
                self.glLine((p2[0], p2[1]), (p0[0], p0[1]))
