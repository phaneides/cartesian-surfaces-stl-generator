
from scipy.optimize import root_scalar
import numpy as np

def sigma_z_curve(rho, z0, zi, n0, ni):
    G = ((ni**2 * zi - n0**2 * z0)**2) / (ni * n0 * (ni*zi - n0*z0) * (ni*z0 - n0*zi))
    O = (ni*z0 - n0*zi) / (zi*z0*(ni - n0))
    T = ((ni - n0)*(ni + n0)**2) / (4*ni*n0*zi*z0*(ni*zi - n0*z0))
    S = ((ni + n0)*(ni**2*zi - n0**2*z0)) / (2*ni*n0*zi*z0*(ni*zi - n0*z0))

    num = (O + T*rho**2) * rho**2
    rad = np.sqrt(1 + (2*S - O**2 * G) * rho**2)
    den = 1 + S * rho**2 + rad

    return num / den

def f(rho, z0, zi, n0, ni):
    z = sigma_z_curve(rho, z0, zi, n0, ni)
    return rho**2 - z**2

# Parámetros de ejemplo
z0 = 1.0
zi = 2.0
n0 = 1.0
ni = 1.5

# Resolver numéricamente
sol = root_scalar(f, args=(z0, zi, n0, ni), method='brentq', bracket=[0.0001, 100.0])
print("Rho donde r(rho) = 0:", sol.root)
print("r(ρ) = ", f(sol.root, z0, zi, n0, ni))  
