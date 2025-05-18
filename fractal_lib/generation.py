import numpy as np
from numba import njit

@njit
def generate_mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter):
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
    # Vytvoření mřížky komplexních čísel pokrývající zadaný rozsah
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    c = real[:, np.newaxis] + 1j * imag[np.newaxis, :]

    # Inicializace pole pro výsledky
    z = np.zeros_like(c)
    div_time = np.zeros(c.shape, dtype=int)

    # Iterativní výpočet Mandelbrotovy množiny
    for i in range(max_iter):
        z = z**2 + c
        diverged = np.abs(z) > 2
        div_now = diverged & (div_time == 0)
        div_time[div_now] = i
        z[diverged] = 2

    return div_time


@njit
def generate_julia(x_min, x_max, y_min, y_max, width, height, c, max_iter):
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
    # Vytvoření mřížky komplexních čísel pokrývající zadaný rozsah
    real = np.linspace(x_min, x_max, width)
    imag = np.linspace(y_min, y_max, height)
    z = real[:, np.newaxis] + 1j * imag[np.newaxis, :]

    # Inicializace pole pro výsledky
    div_time = np.zeros(z.shape, dtype=int)

    # Iterativní výpočet Juliovy množiny
    for i in range(max_iter):
        z = z**2 + c
        diverged = np.abs(z) > 2
        div_now = diverged & (div_time == 0)
        div_time[div_now] = i
        z[diverged] = 2

    return div_time
