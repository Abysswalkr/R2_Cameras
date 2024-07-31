class Obj:
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        self.vertices = []
        self.textcoord = []
        self.normals = []
        self.faces = []

        for line in lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue

            if prefix == "v":
                self.vertices.append(list(map(float, value.split())))
            elif prefix == "vt":
                self.textcoord.append(list(map(float, value.split())))
            elif prefix == "vn":
                self.normals.append(list(map(float, value.split())))
            elif prefix == "f":
                face = [list(map(int, vert.split('/'))) for vert in value.split()]
                self.faces.append(face)
