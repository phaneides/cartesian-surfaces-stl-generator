
# main.py
import numpy as np
import matplotlib.pyplot as plt
from newton_rhapson import *  # imports newton_raphson_2d, intersection_between_curves

def sigma(z0, zi, rho, n0, ni):
    """Returns z(rho), r(rho) for given parameters."""
    G = ((ni**2 * zi - n0**2 * z0)**2) / (ni * n0 * (ni*zi - n0*z0) * (ni*z0 - n0*zi))
    O = (ni*z0 - n0*zi) / (zi*z0*(ni - n0))
    T = ((ni - n0)*(ni + n0)**2) / (4*ni*n0*zi*z0*(ni*zi - n0*z0))
    S = ((ni + n0)*(ni**2*zi - n0**2*z0)) / (2*ni*n0*zi*z0*(ni*zi - n0*z0))
    num = (O + T*rho**2) * rho**2
    rad = np.sqrt(1 + (2*S - O**2 * G) * rho**2)
    den = 1 + S * rho**2 + rad
    z_curve = num / den
    r_curve = np.sqrt(rho**2 - z_curve**2)
    return z_curve, r_curve

class ParametricCurve:
    """Generates callable functions z(rho) and r(rho) for given optical parameters."""
    def __init__(self, z0, zi, n0, ni):
        self.z0 = z0
        self.zi = zi
        self.n0 = n0
        self.ni = ni
        self.z = lambda rho: sigma(self.z0, self.zi, rho, self.n0, self.ni)[0]
        self.r = lambda rho: sigma(self.z0, self.zi, rho, self.n0, self.ni)[1]

# Ejemplo de parámetros distintos para cada curva
curve1 = ParametricCurve(z0=10.0, zi=2.0, n0=1.0, ni=1.5)
curve2 = ParametricCurve(z0=1.5, zi=2.5, n0=1.5, ni=1.0)

# Calcular intersección en parámetros (s1, s2)
s1_int, s2_int = intersection_between_curves(curve1.z, curve1.r,
                                              curve2.z, curve2.r,
                                              s1_0=1.0, s2_0=1.0)

# Punto de intersección en coordenadas (z, r)
z_int, r_int = curve1.z(s1_int), curve1.r(s1_int)

print(f"Parámetros de intersección: s1 = {s1_int}, s2 = {s2_int}")
print(f"Punto de intersección: z = {z_int}, r = {r_int}")

# Graficar ambas curvas y el punto de intersección
rho_vals = np.linspace(0.1, 3.0, 400)
z1_vals, r1_vals = curve1.z(rho_vals), curve1.r(rho_vals)
z2_vals, r2_vals = curve2.z(rho_vals), curve2.r(rho_vals)

plt.figure(figsize=(6, 6))
plt.plot(z1_vals, r1_vals, label="Curva 1")
plt.plot(z2_vals, r2_vals, label="Curva 2")
plt.plot(z_int, r_int, 'ro', label="Intersección")
plt.xlabel("z")
plt.ylabel("r")
plt.title("Intersección entre dos curvas paramétricas")
plt.legend()
plt.axis("equal")
plt.grid(True)
plt.show()
