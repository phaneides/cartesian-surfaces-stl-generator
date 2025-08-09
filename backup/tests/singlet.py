
import numpy as np

# Número de puntos por defecto para muestreo de rho
default_rho_points = 1000

# Función sigma: genera las coordenadas (z, r) de la curva para un dioptrio

def sigma(z0, zi, rho, n0, n1):
    G = ((n1**2 * zi - n0**2 * z0)**2) / (n1 * n0 * (n1*zi - n0*z0) * (n1*z0 - n0*zi))
    O = (n1*z0 - n0*zi) / (zi*z0*(n1 - n0))
    T = ((n1 - n0)*(n1 + n0)**2) / (4*n1*n0*zi*z0*(n1*zi - n0*z0))
    S = ((n1 + n0)*(n1**2*zi - n0**2*z0)) / (2*n1*n0*zi*z0*(n1*zi - n0*z0))

    num = (O + T*rho**2) * rho**2
    rad = np.sqrt(1 + (2*S - O**2 * G) * rho**2)
    den = 1 + S * rho**2 + rad

    z_curve = num / den
    r_curve = np.sqrt(np.maximum(rho**2 - z_curve**2, 0))
    return z_curve, r_curve


def find_rho_max(z0, zi, n0, n1, rmin=1e-6, rmax=50, tol=1e-6):
    def r_val(rho):
        z, r = sigma(z0, zi, np.array([rho]), n0, n1)
        return r[0]

    a, b = rmin, rmax
    if r_val(b) > 0:
        while r_val(b) > 0 and b < 1e3:
            b *= 1.5
        if b >= 1e3:
            raise RuntimeError("No se encontró cruce con el eje en el rango dado.")

    while b - a > tol:
        mid = (a + b) / 2
        if r_val(mid) < tol:
            b = mid
        else:
            a = mid
    return (a + b) / 2



# Busca rho máximo donde r(rho) = 0 (segundo cruce con el eje r) def find_rho_max(z0, zi, n0, n1, rmin=1e-6, rmax=50, tol=1e-6):
    def r_val(rho):
        _, r = sigma(z0, zi, np.array([rho]), n0, n1)
        return r[0]

    a, b = rmin, rmax
    if r_val(b) > 0:
        while r_val(b) > 0 and b < 1e3:
            b *= 1.5
        if b >= 1e3:
            raise RuntimeError("No se encontró cruce con el eje en el rango dado.")

    while b - a > tol:
        mid = (a + b) / 2
        if r_val(mid) < tol:
            b = mid
        else:
            a = mid
    return (a + b) / 2


# Clase que encapsula la generación de una curva sigma completa
class SigmaCurve:
    def __init__(self, z0, zi, n0, n1, rho_points=default_rho_points, t_shift=0):
        self.z0 = z0
        self.zi = zi
        self.n0 = n0
        self.n1 = n1
        self.rho_points = rho_points
        self.t_shift = t_shift
        self.curve = self._generate_curve()

    def _generate_curve(self):
        z0, zi = self.z0, self.zi
        if self.t_shift != 0:
            z0 -= self.t_shift
            zi -= self.t_shift

        rho_max = find_rho_max(z0, zi, self.n0, self.n1)
        rho = np.linspace(0.001, rho_max, self.rho_points)
        z, r = sigma(z0, zi, rho, self.n0, self.n1)

        if self.t_shift != 0:
            z = z + self.t_shift
        return np.column_stack((z, r))

    def get_points(self):
        return self.curve


# Encuentra el punto de intersección más cercano entre dos curvas
def intersection(curve1, curve2):
    diff = np.sqrt((curve1[:,0][:,None] - curve2[:,0][None,:])**2 +
                   (curve1[:,1][:,None] - curve2[:,1][None,:])**2)
    i1, i2 = np.unravel_index(np.argmin(diff), diff.shape)
    pt = (curve1[i1] + curve2[i2]) / 2.0
    return i1, i2, pt


# Clase que modela la lente Omega a partir de dos SigmaCurve
class OmegaLens:
    def __init__(self, sigma1: SigmaCurve, sigma2: SigmaCurve):
        self.s1 = sigma1
        self.s2 = sigma2
        self.i1, self.i2, self.intersection_point = intersection(self.s1.get_points(),
                                                                  self.s2.get_points())
        self.curve = self._generate_inner_curve()

    def _generate_inner_curve(self):
        part1 = self.s1.get_points()[:self.i1+1]
        part2 = self.s2.get_points()[:self.i2+1]
        return np.vstack((part1, part2[::-1]))

    def get_points(self):
        return self.curve

