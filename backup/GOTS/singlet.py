# singlet.py
import numpy as np

# Parámetros de la curva sigma definidos directamente: sigma_params

def sigma_params(rho, G, O, T, S):
    """
    Curva sigma dada por parámetros G, O, T, S:
      z = ((O + T·ρ²)·ρ²) / (1 + S·ρ² + √(1 + (2S − O²G)·ρ²))
      r = √(max(ρ² − z², 0))
    """
    num = (O + T * rho**2) * rho**2
    rad = np.sqrt(1 + (2 * S - O**2 * G) * rho**2)
    den = 1 + S * rho**2 + rad
    z = num / den
    r = np.sqrt(np.maximum(rho**2 - z**2, 0))
    return z, r


def find_rho_max_params(G, O, T, S, rmin=1e-6, rmax=50.0, tol=1e-6):
    """
    Busca ρ máximo donde r(ρ) = 0 usando búsqueda binaria.
    """
    def r_val(rho):
        z, r = sigma_params(np.array([rho]), G, O, T, S)
        return r[0]

    a, b = rmin, rmax
    if r_val(b) > 0:
        while r_val(b) > 0 and b < 1e3:
            b *= 1.5
        if b >= 1e3:
            raise RuntimeError("No se encontró cruce con el eje en el rango dado.")

    while b - a > tol:
        mid = (a + b) / 2.0
        if r_val(mid) < tol:
            b = mid
        else:
            a = mid
    return (a + b) / 2.0


class SigmaCurveParams:
    """
    Genera la curva sigma a partir de parámetros G, O, T, S.
    """
    def __init__(self, G, O, T, S, rho_points=1000, t_shift=0.0):
        self.G = G
        self.O = O
        self.T = T
        self.S = S
        self.rho_points = rho_points
        self.t_shift = t_shift
        self.curve = self._generate_curve()

    def _generate_curve(self):
        # Encuentra ρ máximo
        rho_max = find_rho_max_params(self.G, self.O, self.T, self.S)
        rho = np.linspace(0.001, rho_max, self.rho_points)
        z, r = sigma_params(rho, self.G, self.O, self.T, self.S)
        if self.t_shift != 0.0:
            z += self.t_shift
        return np.column_stack((z, r))

    def get_points(self):
        return self.curve


# Reutilizamos intersection y OmegaLens de la versión anterior

def intersection(curve1, curve2):
    diff = np.sqrt((curve1[:,0][:,None] - curve2[:,0][None,:])**2 +
                   (curve1[:,1][:,None] - curve2[:,1][None,:])**2)
    i1, i2 = np.unravel_index(np.argmin(diff), diff.shape)
    pt = (curve1[i1] + curve2[i2]) / 2.0
    return i1, i2, pt


class OmegaLens:
    """
    Construye la lente interior uniendo dos curvas Sigma.
    """
    def __init__(self, sigma1: SigmaCurveParams, sigma2: SigmaCurveParams):
        self.s1 = sigma1
        self.s2 = sigma2
        self.i1, self.i2, self.intersection_point = intersection(
            self.s1.get_points(), self.s2.get_points()
        )
        self.curve = self._generate_inner_curve()

    def _generate_inner_curve(self):
        part1 = self.s1.get_points()[:self.i1+1]
        part2 = self.s2.get_points()[:self.i2+1]
        return np.vstack((part1, part2[::-1]))

    def get_points(self):
        return self.curve

