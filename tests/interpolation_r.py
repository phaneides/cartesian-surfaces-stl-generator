import numpy as np 
import matplotlib.pyplot as plt 

def biseccion(f, a, b, tol=1e-9, max_iter=100):
    """Método de bisección"""
    fa, fb = f(a), f(b)
    
    while fa * fb > 0:
        b *= 1.5
        fb = f(b)
    
    for i in range(max_iter):
        c = 0.5 * (a + b)
        fc = f(c)
        
        if abs(fc) < tol or (b - a) < tol:
            return c
            
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c

def sigma(z0, zi, rho, n0, ni):
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

# Parámetros 
z0, zi, n0, ni = -10.0, -20.0, 1.0, 1.5
num_rho = 90

# Funciones
z_rho = lambda rho: sigma(z0, zi, rho, n0, ni)[0]
rho_sq_minus_z_sq = lambda rho: rho**2 - z_rho(rho)**2

# Encontrar límite y generar curva
rho_max = biseccion(rho_sq_minus_z_sq, 1e-9, 30, tol=1e-10) - 1e-10
rho_vals = np.linspace(0.01, rho_max, num_rho)
z_vals = [z_rho(r) for r in rho_vals]
r_vals = [sigma(z0, zi, r, n0, ni)[1] for r in rho_vals]

# Graficar
fig, ax = plt.subplots()
ax.plot(z_vals, r_vals, 'b-', label='Curva paramétrica')
ax.scatter(z_vals, r_vals, color="black", s=10) 
ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
ax.set_xlabel('$z(\\rho)$')
ax.set_ylabel('$r(\\rho)$')
ax.set_title('Curva paramétrica z(ρ) vs r(ρ)')
ax.grid(True, alpha=0.3)
ax.axis("equal")
ax.legend()
plt.show()

print(f"ρ_max = {rho_max + 1e-10:.10f}")
print(f"Puntos generados: {len(z_vals)}")
