import numpy as np
from vispy import scene, app

def create_2d_curve_canvas(r, z):
    """
    Crea un canvas para visualizar el perfil 2D en el plano (r, z).
    """
    canvas = scene.SceneCanvas(keys='interactive', show=True, title="Curva 2D")
    view = canvas.central_widget.add_view()
    view.camera = scene.PanZoomCamera(aspect=1)
    pts = np.column_stack((r, z))
    line = scene.visuals.Line(pos=pts, color='red', width=2, method='gl')
    view.add(line)
    view.camera.set_range()
    return canvas

def create_3d_surface_canvas(vertices, faces):
    """
    Crea un canvas para visualizar la superficie 3D (mallado) con vispy.
    """
    canvas = scene.SceneCanvas(keys='interactive', show=True, title="Superficie 3D")
    view = canvas.central_widget.add_view()
    view.camera = 'turntable'
    mesh = scene.visuals.Mesh(vertices=vertices, faces=faces, color=(0.5, 0.5, 1, 1), shading='smooth')
    view.add(mesh)
    view.camera.set_range()
    return canvas

