
import pyvista as pv

# Cargar el archivo STL
mesh = pv.read("surface.stl")

# Mostrar el modelo 3D 

mesh.plot()
