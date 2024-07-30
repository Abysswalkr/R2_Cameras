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
                vert = list(map(float, value.split(" ")))
                self.vertices.append(vert)
            elif prefix == "vt":
                vts = list(map(float, value.split(" ")))
                self.textcoord.append(vts)
            elif prefix == "vn":
                norm = list(map(float, value.split(" ")))
                self.normals.append(norm)
            elif prefix == "f":
                face = []
                verts = value.split(" ")
                for vert in verts:
                    vert = list(map(int, vert.split("/")))
                    face.append(vert)
                self.faces.append(face)
