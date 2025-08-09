import numpy as np

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """Bisection Method for find roots of the function f in the interval [a, b]"""
    fa, fb = f(a), f(b)

    if fa * fb > 0:
        raise ValueError("La función debe cambiar de signo en el intervalo.")

    for _ in range(max_iter):
        c = 0.5 * (a + b)
        fc = f(c)

        if abs(fc) < tol or (b - a) / 2 < tol:
            return c

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    raise RuntimeError(f"El método de bisección no convergió en {max_iter} steps.")



def biseccion_mod(f, a, b, tol=1e-9, max_iter=100):
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


def newton_raphson_2d(F, x0, tol=1e-10, max_iter=50):
    """
    Multivariable Newton–Raphson for solving F(x) = 0 in R^2.

    Parameters:
        F        : function R^2 -> R^2, returns (f1, f2)
        x0       : tuple (s1, s2) initial guess
        tol      : convergence tolerance
        max_iter : maximum number of iterations

    Returns:
        (s1, s2) solution
    """
    x = np.array(x0, dtype=float)
    
    def jacobian(F, x, h=1e-8):
        """Numerical Jacobian via finite differences."""
        J = np.zeros((2, 2))
        f0 = np.array(F(*x))
        for i in range(2):
            x_step = x.copy()
            x_step[i] += h
            fi = np.array(F(*x_step))
            J[:, i] = (fi - f0) / h
        return J

    for _ in range(max_iter):
        f_val = np.array(F(*x))
        if np.linalg.norm(f_val, ord=2) < tol:
            return tuple(x)
        J = jacobian(F, x)
        try:
            delta = np.linalg.solve(J, -f_val)
        except np.linalg.LinAlgError:
            raise ValueError(f"Jacobian is singular at {x}")
        x += delta
        if np.linalg.norm(delta, ord=2) < tol:
            return tuple(x)

    raise RuntimeError("Newton–Raphson did not converge.")

def intersection_between_curves(x1, y1, x2, y2, s1_0, s2_0):
    """
    Finds intersection between two parametric curves:
    Curve 1: (x1(s1), y1(s1))
    Curve 2: (x2(s2), y2(s2))

    Parameters:
        x1, y1 : functions of s1 for curve 1
        x2, y2 : functions of s2 for curve 2
        s1_0, s2_0 : initial guesses

    Returns:
        (s1, s2) intersection parameters
    """
    def F(s1, s2):
        return (
            x1(s1) - x2(s2),
            y1(s1) - y2(s2)
        )
    
    return newton_raphson_2d(F, (s1_0, s2_0))


