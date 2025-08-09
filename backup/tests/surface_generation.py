import numpy as np
import trimesh


def revolve_curve(curve_pts, angular_points):
    """
    Genera la superficie de revolución a partir de una curva 2D (z, r) de manera totalmente vectorizada.

    Parámetros:
      curve_pts: array Nx2 con columnas [z, r]
      angular_points: resolución angular; n_phi = 2*angular_points

    Retorna:
      vertices: arreglo (M x 3) con coordenadas 3D
      faces:    arreglo (K x 3) con índices de triángulos
    """
    n_theta = curve_pts.shape[0]
    n_phi = 2 * angular_points

    # Generar vértices
    z = curve_pts[:, 0]
    r = curve_pts[:, 1]
    phi = np.linspace(0, 2 * np.pi, n_phi, endpoint=False)
    r_grid, phi_grid = np.meshgrid(r, phi, indexing='ij')
    z_grid, _      = np.meshgrid(z, phi, indexing='ij')
    x = r_grid * np.cos(phi_grid)
    y = r_grid * np.sin(phi_grid)
    vertices = np.column_stack((x.ravel(), y.ravel(), z_grid.ravel()))

    # Generar caras vectorizadas
    n_cells = (n_theta - 1) * n_phi
    k = np.arange(n_cells)
    i = k // n_phi
    j = k % n_phi
    j2 = (j + 1) % n_phi
    base = i * n_phi
    nxt  = base + n_phi

    faces = np.empty((2 * n_cells, 3), dtype=int)
    # Triángulos pares (v0, v1, v2)
    faces[0::2, 0] = base + j
    faces[0::2, 1] = nxt  + j
    faces[0::2, 2] = nxt  + j2
    # Triángulos impares (v0, v2, v3)
    faces[1::2, 0] = base + j
    faces[1::2, 1] = nxt  + j2
    faces[1::2, 2] = base + j2

    return vertices, faces


def export_to_stl_trimesh(filename, vertices, faces, solid_name="surface"):
    """
    Exporta la malla a un archivo STL usando trimesh para máxima velocidad.
    """
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.export(filename)
    print(f"Archivo STL generado con trimesh: {filename}")

