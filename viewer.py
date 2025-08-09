
# viewer.py
import numpy as np
from vispy import scene, app
from vispy.visuals.filters import ShadingFilter, WireframeFilter
import matplotlib.pyplot as plt


def show_vispy(vertices, faces, TITLE_NAME='3D SCENE',
               SHADING='flat', COLOR=[0.7, 0.7, 0.7, 1],
               SHOW_WIREFRAME=False):

    canvas = scene.SceneCanvas(keys='interactive', show=True, title=TITLE_NAME)
    view = canvas.central_widget.add_view()
    view.camera = 'turntable'

    mesh = scene.visuals.Mesh(vertices=vertices,
                              faces=faces,
                              color=COLOR,
                              shading=SHADING)
    view.add(mesh)

    if SHOW_WIREFRAME:
        wireframe_filter = WireframeFilter(color=COLOR)
        mesh.attach(wireframe_filter)

    view.camera.set_range()

    # Manejar cierre seguro para evitar que se quede bloqueado
    def on_close(event):
        app.quit()

    canvas.events.close.connect(on_close)

    app.run()
    return canvas
def info_view(sigma1_points, sigma2_points, inner_curve_points,
              intersection_point, width, diameter):
    """
    Genera la vista 2D con información del diámetro y espesor.
    Las curvas sigma se dibujan punteadas y la interna en negro continuo.
    """
    fig, ax = plt.subplots()

    z1, r1 = sigma1_points.T
    z2, r2 = sigma2_points.T
    zc, rc = inner_curve_points.T

    # Curvas Sigma
    ax.plot(z1, r1, 'k--', label='Σ₁')
    ax.plot(z2, r2, 'r--', label='Σ₂')

    # Curva interna
    ax.plot(zc, rc, 'k-', label='Inner curve')

    # Punto de intersección
    ax.scatter(*intersection_point, color='blue', zorder=5)

    # Texto informativo
    text_x = min(z1.min(), z2.min())
    text_y = max(r1.max(), r2.max()) * 1.05
    ax.text(text_x, text_y,
            f"Diameter = {diameter:.2f} cm\nWidth = {width:.2f} cm",
            fontsize=10, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    ax.axis('equal')
    plt.legend()
    plt.show()
