"""
Inicializační soubor pro knihovnu fraktálů (fractal_lib).
Zpřístupňuje hlavní funkce pro generování fraktálů.
"""

from .generation import generate_mandelbrot, generate_julia
from .visualization import interactive_fractal_viewer

__all__ = ["generate_mandelbrot", "generate_julia", "interactive_fractal_viewer"]
