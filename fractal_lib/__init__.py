"""
Inicializační soubor pro knihovnu fraktálů.
Zpřístupňuje hlavní funkce pro generování fraktálů.
"""

from .generation import generate_mandelbrot, generate_julia

__all__ = ["generate_mandelbrot", "generate_julia"]
