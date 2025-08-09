# main.py
#!/usr/bin/env python3
import json
import argparse
from singlet import SigmaCurveParams, OmegaLens
from surface_generation import revolve_curve, export_to_stl
from plotting import create_2d_curve_canvas
from vispy import app

def main():
    parser = argparse.ArgumentParser(
        description="Genera la lente Ω usando parámetros G,O,T,S y exporta STL"
    )
    parser.add_argument(
        "--params", "-p",
        default="params.json",
        help="Ruta al archivo JSON con los parámetros de sigma1 y sigma2"
    )
    parser.add_argument(
        "--rho-points", "-r",
        type=int,
        default=1000,
        help="Número de puntos de muestreo de ρ para las curvas sigma"
    )
    parser.add_argument(
        "--plot2d",
        action="store_true",
        help="Si se indica, abre una ventana VisPy con la curva 2D"
    )
    parser.add_argument(
        "--angular-points", "-a",
        type=int,
        default=64,
        help="Resolución angular para la generación de la superficie (n_phi = 2·angular_points)"
    )
    parser.add_argument(
        "--stl-file", "-o",
        default="surface.stl",
        help="Nombre del archivo STL de salida"
    )
    args = parser.parse_args()

    # Carga de parámetros JSON (solo G,O,T,S para sigma1 y sigma2, y t)
    with open(args.params, "r") as f:
        cfg = json.load(f)

    p1 = cfg["sigma1"]
    p2 = cfg["sigma2"]
    t_shift = cfg.get("t", 0.0)

    # Crear curvas Sigma a partir de parámetros G,O,T,S
    sigma1 = SigmaCurveParams(**p1, rho_points=args.rho_points, t_shift=0.0)
    sigma2 = SigmaCurveParams(**p2, rho_points=args.rho_points, t_shift=t_shift)

    # Construir lente Omega y obtener contorno
    omega = OmegaLens(sigma1, sigma2)
    curve = omega.get_points()  # array (N x 2) [z, r]

    # Mostrar curva 2D si se solicitó
    if args.plot2d:
        r = curve[:,1]
        z = curve[:,0]
        _ = create_2d_curve_canvas(r, z)
        app.run()

    # Generar superficie 3D y exportar STL
    vertices, faces = revolve_curve(curve, args.angular_points)
    export_to_stl(args.stl_file, vertices, faces)

if __name__ == "__main__":
    main()
