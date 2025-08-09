import numpy as np 

def revolve_curve(curve_pts, n_ang): 

    n_theta = curve_pts.shape[0] 
    n_phi = 2*n_ang 

    phi = np.linspace(0, 2*np.pi, n_phi, endpoint=False) 

    z = curve_pts[:, 0] 
    r = curve_pts[:, 1]

    R, PHI = np.meshgrid(r, phi, indexing='ij') 
    Z, _ = np.meshgrid(z, phi, indexing='ij') 

    X = R*np.cos(PHI) 
    Y = R*np.sin(PHI) 


    vertices = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    faces = generate_mesh_from_vertices(vertices, n_theta, n_phi) 

    return vertices, faces 


def generate_mesh_from_vertices(verts, n_theta, n_phi): 
    
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

    return faces 


def generate_mesh_from_vertices_numpy(n_theta, n_phi): 

    n_cells = (n_theta - 1)*n_phi 
    k = np.arange(n_cells) 
    i = k // n_phi 
    j = k % n_phi
    j2 = (j + 1) % n_phi 

    base = i*n_phi 
    nxt = base + n_phi 

    faces = np.empty((2 * n_cells, 3), dtype=int)
    # Triángulos pares (v0, v1, v2)
    faces[0::2, 0] = base + j
    faces[0::2, 1] = nxt  + j
    faces[0::2, 2] = nxt  + j2
    # Triángulos impares (v0, v2, v3)
    faces[1::2, 0] = base + j
    faces[1::2, 1] = nxt  + j2
    faces[1::2, 2] = base + j2    

    return faces


def compute_normal(p1, p2, p3):
    v1 = p2 - p1
    v2 = p3 - p1
    n  = np.cross(v1, v2)
    norm = np.linalg.norm(n)
    return n / norm if norm else n


# ===============
#   EXPORT TO STL 
# ===============

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


def export_to_stl_trimesh(filename, vertices, faces, solid_name="surface"):
    """
    Exporta la malla a un archivo STL usando trimesh para máxima velocidad.
    """
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.export(filename)
    print(f"Archivo STL generado con trimesh: {filename}")

