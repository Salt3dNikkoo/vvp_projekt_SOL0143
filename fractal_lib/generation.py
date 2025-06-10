"""
Modul pro generování fraktálů – Mandelbrotovy a Juliovy množiny.
Používá Numba pro paralelní výpočet.
"""

from numba import njit, prange
import numpy as np

@njit(parallel=True)
def generate_mandelbrot(x_min: float,
                        x_max: float,
                        y_min: float,
                        y_max: float,
                        width: int,
                        height: int,
                        max_iter: int) -> np.ndarray:
    """
    Generuje obraz Mandelbrotovy množiny.

    Parametry:
    x_min, x_max: float
        Rozsah reálné části komplexní roviny.
    y_min, y_max: float
        Rozsah imaginární části komplexní roviny.
    width, height: int
        Rozměry výstupního obrázku v pixelech.
    max_iter: int
        Maximální počet iterací pro výpočet divergence.

    Návratová hodnota:
    numpy.ndarray
        2D pole s počtem iterací pro každý bod; slouží k vizualizaci fraktálu.
    """
    result = np.zeros((height, width), dtype=np.int32)
    for i in prange(height):
        for j in prange(width):
            x0 = x_min + j * (x_max - x_min) / width
            y0 = y_min + i * (y_max - y_min) / height
            x, y = 0.0, 0.0
            iteration = 0
            while x*x + y*y <= 4.0 and iteration < max_iter:
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
                iteration += 1
            result[i, j] = iteration
    return result

@njit(parallel=True)
def generate_julia(x_min: float,
                   x_max: float,
                   y_min: float,
                   y_max: float,
                   width: int,
                   height: int,
                   c: complex,
                   max_iter: int) -> np.ndarray:
    """
    Generuje obraz Juliovy množiny pro daný parametr c.

    Parametry:
    x_min, x_max: float
        Rozsah reálné části komplexní roviny.
    y_min, y_max: float
        Rozsah imaginární části komplexní roviny.
    width, height: int
        Rozměry výstupního obrázku v pixelech.
    c: complex
        Komplexní konstanta určující tvar Juliovy množiny.
    max_iter: int
        Maximální počet iterací pro výpočet divergence.

    Návratová hodnota:
    numpy.ndarray
        2D pole s počtem iterací pro každý bod; slouží k vizualizaci fraktálu.
    """
    result = np.zeros((height, width), dtype=np.int32)
    for i in prange(height):
        for j in prange(width):
            x = x_min + j * (x_max - x_min) / width
            y = y_min + i * (y_max - y_min) / height
            z_real, z_imag = x, y
            iteration = 0
            while z_real*z_real + z_imag*z_imag <= 4.0 and iteration < max_iter:
                temp = z_real*z_real - z_imag*z_imag + c.real
                z_imag = 2.0 * z_real * z_imag + c.imag
                z_real = temp
                iteration += 1
            result[i, j] = iteration
    return result
