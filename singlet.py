# singlet.py 

# Curves of the cartesian Ovoids in the parametric formulation z(ρ).  

from math_utils import * 

import numpy as np 
import math_utils as mu


# Cartesian Ovioids in the form z = z(ρ), r = r(ρ).
def sigma(z0, zi, rho, n0, ni): 
    
    z0 = -z0 #Absolutiza los z

    G = ((ni**2*zi - n0**2*z0)**2) / (ni*n0*(ni*zi - n0*z0)*(ni*z0 - n0*zi))
    O = (ni*z0 - n0*zi) / (zi*z0*(ni - n0)) 
    T = (ni - n0)*(ni + n0)**2 / (4*ni*n0*zi*z0*(ni*zi - n0*z0))
    S = ((ni + n0)*(ni**2*zi - n0**2*z0))/(2*ni*n0*zi*z0*(ni*zi - n0*z0)) 

    num = (O + T*rho**2)*rho**2
    rad = np.sqrt(1 + (2*S - O**2 * G)*rho**2) 
    den = 1 + S*rho**2 + rad

    z = num/den 
    r = np.sqrt(rho**2 - z**2) 


    return z, r


class SigmaCurve: 
    def __init__(self, z0, zi, n0, ni, rho_points, t_shift=0):
        self.z0 = z0
        self.zi = zi 
        self.n0 = n0 
        self.ni = ni 
        self.rho_points = rho_points 
        self.t_shift = t_shift 
        self.points = self.get_points() 
        
    def get_points(self, rhof=None): 
        z0, zi = self.z0 - self.t_shift, self.zi - self.t_shift 
        n0, ni = self.n0, self.ni 
        
        z_rho = lambda rho: sigma(z0, zi, rho, n0, ni)[0] 
        r_rho_2 = lambda rho: rho**2 - z_rho(rho)**2
        tol = 1e-6

        if rhof is None: 
            rho_max = mu.biseccion_mod(r_rho_2, tol, 50)
            rho_max -= tol  
            rhof = rho_max

        rho = np.linspace(tol, rhof, self.rho_points) 
        z, r = sigma(z0, zi, rho, n0, ni) 
        z = z + self.t_shift 
        return np.column_stack((z, r)) 

    def lambdify(self): 
        """Devuelve funciones z(rho), r(rho) listas para Newton–Raphson."""

        z0, zi = self.z0 - self.t_shift, self.zi - self.t_shift 
        n0, ni = self.n0, self.ni 
        z_rho = lambda rho: sigma(z0, zi, rho, n0, ni)[0] + self.t_shift
        r_rho = lambda rho: sigma(z0, zi, rho, n0, ni)[1]
        return z_rho, r_rho


class OmegaLens: 

    def __init__(self, sigma1: SigmaCurve, sigma2: SigmaCurve): 
        self.s1 = sigma1
        self.s2 = sigma2 
       
        z1_func, r1_func = self.s1.lambdify() 
        z2_func, r2_func = self.s2.lambdify()

        # 1) Calcular intersección en parámetros (rho1, rho2)
        rho_i1, rho_i2 = intersection_between_curves(z1_func, r1_func,
                                                     z2_func, r2_func,
                                                     s1_0=1.0, s2_0=1.0)

        self.rho_intersection = (rho_i1, rho_i2)

        # 2) Calcular punto físico de intersección
        z_int = z1_func(rho_i1) + self.s1.t_shift
        r_int = r1_func(rho_i1)
        self.intersection_point = (z_int, r_int)

        # 3) Generar la curva interna
        self.curve = self._generate_inner_curve(rho_i1, rho_i2)
        
    def _generate_inner_curve(self, rho_i1, rho_i2): 
        part1 = self.s1.get_points(rho_i1)
        part2 = self.s2.get_points(rho_i2)
        return np.vstack((part1, part2[::-1]))

    def get_points(self): 
        return self.curve

