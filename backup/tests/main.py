#!/usr/bin/env python3
import json
import argparse

from singlet import SigmaCurve, OmegaLens
from surface_generation import revolve_curve
from surface_generation import export_to_stl_trimesh as export_to_stl

from plotting import create_2d_curve_canvas
from vispy import app

def main():
    parser = argparse.ArgumentParser(
        description="Genera la lente Ω y, opcionalmente, muestra la curva 2D y exporta la superficie en STL"
    )
    parser.add_argument(
        "--params", "-p",
        default="params.json",
        help="Ruta al archivo JSON con los parámetros"
    )
    parser.add_argument(
        "--plot2d",
        action="store_true",
        help="Si se indica, abre una ventana VisPy con la curva 2D (r vs. z)"
    )

    parser.add_argument(
        '--rho-points', '-rho',
        type=int,
        default=64,
        help= 'El número de elementos que se toma para discretizar la variable rho (distancia del origen a la superficie)'
    )

    parser.add_argument(
        "--angular-points", "-ang",
        type=int,
        default=None,
        help="Resolución angular para la generación de la superficie (n_phi = 2·angular_points)"
    )
    parser.add_argument(
        "--stl-file", "-o",
        default="surface.stl",
        help="Nombre del archivo STL de salida"
    )
    args = parser.parse_args()

    # 1) Leer parámetros
    with open(args.params, "r") as f:
        params = json.load(f)

    z0 = params["z0"]
    z1 = params["z1"]
    z2 = params["z2"]
    n0 = params["n0"]
    n1 = params["n1"]
    t  = params.get("t", 0.0)

    
    rho_points = args.rho_points
    angular_points = args.angular_points

    # 2) Generar las dos curvas Sigma
    sigma1 = SigmaCurve(z0, z1, n0, n1, rho_points=rho_points)
    sigma2 = SigmaCurve(z1, z2, n1, n0, rho_points=rho_points, t_shift=t)

    # 3) Construir el lente Ω
    omega = OmegaLens(sigma1, sigma2)
    curve = omega.get_points()  # array (N×2) con columnas [z, r]

    # 4) Mostrar la curva 2D si se pidió
    if args.plot2d:
        r = curve[:,1]
        z = curve[:,0]
        _ = create_2d_curve_canvas(r, z)
        app.run()

    # 5) Revolver la curva para generar la malla 3D y exportar STL
    vertices, faces = revolve_curve(curve, args.angular_points)
    export_to_stl('output/' + args.stl_file, vertices, faces)

if __name__ == "__main__":
    main()

