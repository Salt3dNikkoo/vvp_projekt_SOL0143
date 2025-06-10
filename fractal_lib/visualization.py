"""
Modul pro vizualizaci Mandelbrotovy a Juliovy množiny pomocí Matplotlibu.
Zahrnuje interaktivní GUI s ovládacími prvky.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.backend_bases import MouseEvent
from .generation import generate_mandelbrot, generate_julia
from typing import Optional, Any
matplotlib.use('TkAgg')

def interactive_fractal_viewer() -> None:
    """
    Spouští interaktivní vizualizaci Mandelbrotovy a Juliovy množiny pomocí knihovny Matplotlib.
    Umožňuje uživateli měnit parametry (počet iterací, parametr c), barevná schémata,
    a typ fraktálu pomocí ovládacích prvků a také přibližovat/oddalovat zobrazení kolečkem myši.
    """
    width, height = 800, 600
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    initial_max_iter = 100
    initial_c = complex(-0.4, 0.6)

     # Inicializace figure a subplotu
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.4)

    current_limits = [x_min, x_max, y_min, y_max]

    # Generování počátečních dat Mandelbrotovy množiny
    data = generate_mandelbrot(x_min, x_max, y_min, y_max, width, height, initial_max_iter)
    image = ax.imshow(data, cmap='inferno', extent=[x_min, x_max, y_min, y_max])
    ax.set_title("Mandelbrotova množina")

    # UI prvky
    # Slider pro počet iterací
    ax_iter = plt.axes([0.25, 0.3, 0.65, 0.03])
    iter_slider = Slider(ax_iter, 'Iterace', 10, 1000, valinit=initial_max_iter, valstep=10)

    # Slidery pro reálnou a imaginární část parametru c
    ax_c_real = plt.axes([0.25, 0.25, 0.3, 0.03])
    c_real_slider = Slider(ax_c_real, 'Re(c)', -1.0, 1.0, valinit=initial_c.real, valstep=0.01)

    ax_c_imag = plt.axes([0.6, 0.25, 0.3, 0.03])
    c_imag_slider = Slider(ax_c_imag, 'Im(c)', -1.0, 1.0, valinit=initial_c.imag, valstep=0.01)

    # RadioButtons pro výběr barevného schématu a typu fraktálu
    ax_colormap = plt.axes([0.025, 0.4, 0.15, 0.15])
    cmap_radio = RadioButtons(ax_colormap, ['inferno', 'plasma', 'viridis'])

    # Radiobuttony pro výběr typu fraktálu
    ax_type = plt.axes([0.025, 0.6, 0.15, 0.1])
    fractal_radio = RadioButtons(ax_type, ['Mandelbrot', 'Julia'])

     # Tlačítko pro vykreslení
    ax_button = plt.axes([0.4, 0.15, 0.2, 0.05])
    update_button = Button(ax_button, 'Vykreslit')

    # Tlačítko pro reset zoomu
    ax_reset = plt.axes([0.65, 0.15, 0.2, 0.05])
    reset_button = Button(ax_reset, 'Reset zoom')

    def update(val: Optional[Any] = None) -> None:
        nonlocal image, current_limits
        max_iter = int(iter_slider.val)
        c = complex(c_real_slider.val, c_imag_slider.val)
        cmap = cmap_radio.value_selected
        selected_type = fractal_radio.value_selected
        x0, x1, y0, y1 = current_limits

        # Set axis limits first
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)

        if selected_type == "Mandelbrot":
            data = generate_mandelbrot(x0, x1, y0, y1, width, height, max_iter)
            ax.set_title("Mandelbrotova množina")
        else:
            data = generate_julia(x0, x1, y0, y1, width, height, c, max_iter)
            ax.set_title(f"Juliova množina (c={c.real:.2f}+{c.imag:.2f}i)")

        image.set_data(data)
        image.set_extent([x0, x1, y0, y1])
        image.set_cmap(cmap)
        fig.canvas.draw_idle()

    def on_scroll(event: MouseEvent) -> None:
        nonlocal current_limits
        base_scale = 0.9
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None:
            return

        x0, x1, y0, y1 = current_limits
        scale = base_scale if event.button == 'up' else 1 / base_scale

        new_width = (x1 - x0) * scale
        new_height = (y1 - y0) * scale
        new_xmin = xdata - (xdata - x0) * scale
        new_ymin = ydata - (ydata - y0) * scale

        current_limits = [new_xmin, new_xmin + new_width, new_ymin, new_ymin + new_height]
        update()

    def reset_zoom(event: MouseEvent) -> None:
        nonlocal current_limits
        current_limits = [-2.0, 1.0, -1.5, 1.5]
        ax.set_xlim(current_limits[0], current_limits[1])
        ax.set_ylim(current_limits[2], current_limits[3])
        ax.figure.canvas.draw()  # Force immediate redraw of the axes
        update()

    # Připojení funkcí k událostem tlačítek a kolečka myši
    update_button.on_clicked(update)
    reset_button.on_clicked(reset_zoom)
    fig.canvas.mpl_connect('scroll_event', on_scroll)

    # Zobrazení interaktivního okna
    plt.show()

