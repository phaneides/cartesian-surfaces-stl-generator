from singlet import * 
# Parámetros
params = {
    "z0": 100000.0,
    "z1": 60.0,
    "z2": 30.0,
    "n0": 1.0,
    "n1": 1.5,
    "t": 4.0,
}

# Crear curvas
c1 = SigmaCurve(z0=params["z0"], zi=params["z1"], 
                n0=params["n0"], ni=params["n1"], 
                rho_points=400, t_shift=0)

c2 = SigmaCurve(z0=-params["z1"], zi=params["z2"], 
                n0=params["n1"], ni=params["n0"], 
                rho_points=400, t_shift=params["t"])

# Crear lente Omega
lens = OmegaLens(c1, c2)

# Imprimir resultados
print("ρ intersección:", lens.rho_intersection)
print("Punto intersección (z, r):", lens.intersection_point)

# Graficar
import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.plot(c1.points[:,0], c1.points[:,1], label="Curva 1")
plt.plot(c2.points[:,0], c2.points[:,1], label="Curva 2")
plt.plot(*lens.intersection_point, 'ro', label="Intersección")
plt.plot(lens.curve[:,0], lens.curve[:,1], 'k--', label="Curva interna")
plt.axis("equal")
plt.xlabel("z")
plt.ylabel("r")
plt.legend()
plt.grid(True)
plt.title("Omega Lens")
plt.show()
