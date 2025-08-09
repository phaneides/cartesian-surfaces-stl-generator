
import trimesh
import numpy as np
from vispy import scene
from vispy.scene import visuals

# Cargar el STL con trimesh
mesh = trimesh.load("thin.stl")

# Obtener vértices y caras
vertices = mesh.vertices
faces = mesh.faces

# Crear una escena de VisPy
canvas = scene.SceneCanvas(keys='interactive', bgcolor='black', show=True)
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='z', fov=45)

# Crear la malla
mesh_visual = visuals.Mesh(vertices=vertices, faces=faces, color=(0.5, 0.6, 0.9, 1.0), shading='smooth')
view.add(mesh_visual)

# Añadir un eje para referencia
axis = scene.visuals.XYZAxis(parent=view.scene)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1:
        canvas.app.run()
