# surface_generation.py

import numpy as np

def revolve_curve(curve_pts, angular_points):
    """
    Genera la superficie de revolución a partir de una curva 2D (z, r).
    
    Parámetros:
      curve_pts: array Nx2 con columnas [z, r]
      angular_points: resolución angular; n_phi = 2*angular_points
    
    Retorna:
      vertices: arreglo (M x 3) con coordenadas 3D
      faces:    arreglo (K x 3) con índices de triángulos
    """
    
    n_theta = curve_pts.shape[0]
    n_phi = 2 * angular_points
    phi = np.linspace(0, 2*np.pi, n_phi, endpoint=False)

    z = curve_pts[:, 0]
    r = curve_pts[:, 1]

    # Rejillas para revolución
    r_grid, phi_grid = np.meshgrid(r, phi, indexing='ij')
    z_grid, _      = np.meshgrid(z, phi, indexing='ij')

    x = r_grid * np.cos(phi_grid)
    y = r_grid * np.sin(phi_grid)

    # Vértices: (n_theta * n_phi) x 3
    vertices = np.column_stack((x.ravel(), y.ravel(), z_grid.ravel()))

    # Caras: dos triángulos por celda
    faces = []
    for i in range(n_theta - 1):
        for j in range(n_phi):
            j2 = (j + 1) % n_phi
            v0 = i     * n_phi + j
            v1 = (i+1) * n_phi + j
            v2 = (i+1) * n_phi + j2
            v3 = i     * n_phi + j2
            faces.append([v0, v1, v2])
            faces.append([v0, v2, v3])
    faces = np.array(faces, dtype=int)
    return vertices, faces


def compute_normal(p1, p2, p3):
    v1 = p2 - p1
    v2 = p3 - p1
    n  = np.cross(v1, v2)
    norm = np.linalg.norm(n)
    return n / norm if norm else n


def export_to_stl(filename, vertices, faces, solid_name="surface"):
    with open(filename, "w") as f:
        f.write(f"solid {solid_name}\n")
        for tri in faces:
            p1, p2, p3 = vertices[tri]
            n = compute_normal(p1, p2, p3)
            f.write(f"  facet normal {n[0]} {n[1]} {n[2]}\n")
            f.write("    outer loop\n")
            for p in (p1, p2, p3):
                f.write(f"      vertex {p[0]} {p[1]} {p[2]}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {solid_name}\n")
    print(f"Archivo STL generado: {filename}")

