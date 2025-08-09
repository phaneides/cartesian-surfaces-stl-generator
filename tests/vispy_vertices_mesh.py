# Canvas Setup. 

import numpy as np 
from vispy import scene, app 


def gen_sphere(R=1, n_ang=30):

    theta = np.linspace(0, np.pi, n_ang)     # de 0 a pi para cubrir de polo a polo
    phi = np.linspace(0, 2*np.pi, n_ang)     # de 0 a 2pi para una vuelta completa

    THETA, PHI = np.meshgrid(theta, phi, indexing='ij')

    X = R * np.sin(THETA) * np.cos(PHI)
    Y = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)

    vertices = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

    faces = []
    rows, cols = THETA.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Índices de los 4 vértices de la celda actual
            a = i * cols + j
            b = a + 1
            c = a + cols
            d = c + 1

            # Dos triángulos por cuadrado
            faces.append([a, b, d])
            faces.append([a, d, c])

    return vertices, np.array(faces)

# Ejemplo de uso

TITLE_NAME = "No-name 2D"
COLOR = [0.5, 0.5, 0.5, 1]
PPRINT = False 
N_ANG = 9
RADIUS = 1

vertices, faces = gen_sphere(R=RADIUS, n_ang=N_ANG)
print("Num. Vértices:", vertices.shape)
print("Num. Faces:", len(faces))

if PPRINT == True: 
    print(f'vertex_array: \n {vertices}') 
    print(f'\n faces_array: \n {faces}') 


from vispy.visuals.filters import ShadingFilter, WireframeFilter, FacePickingFilter


wireframe_filter = WireframeFilter()
shading_filter = ShadingFilter()
face_picking_filter = FacePickingFilter()


canvas = scene.SceneCanvas(keys='interactive', show=True, title=TITLE_NAME)
view = canvas.central_widget.add_view() 
view.camera = "turntable"
mesh = scene.visuals.Mesh(vertices=vertices, faces = faces, color = COLOR, shading = 'flat')

view.add(mesh)

# Use filters 

mesh.attach(wireframe_filter)



app.run()


