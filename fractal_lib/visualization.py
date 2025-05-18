import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from fractal_lib.generation import generate_mandelbrot, generate_julia

def interactive_fractal_viewer():
    """
    Spouští interaktivní vizualizaci Mandelbrotovy a Juliovy množiny pomocí knihovny Matplotlib.
    Umožňuje uživateli měnit parametry (počet iterací, parametr c), barevná schémata,
    a typ fraktálu pomocí ovládacích prvků a také přibližovat/oddalovat zobrazení kolečkem myši.
    """
    
    # Rozměry výstupního obrázku
    width, height = 600, 400

    # Výchozí hodnoty iterací a parametru c
    initial_max_iter = 100
    initial_c = complex(-0.4, 0.6)

    # Možnosti colormap a typů fraktálů
    cmap_options = ['inferno', 'plasma', 'viridis', 'twilight', 'magma']
    fractal_type = ['Mandelbrot', 'Julia']

    # Výchozí rozsah souřadnic
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5

    # Inicializace figure a subplotu
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.4)

    # Generování počátečních dat Mandelbrotovy množiny
    data = generate_mandelbrot(x_min, x_max, y_min, y_max, width, height, initial_max_iter)
    image = ax.imshow(data, cmap='inferno', extent=[x_min, x_max, y_min, y_max])
    ax.set_title("Mandelbrotova množina")

    # Slider pro počet iterací
    ax_iter = plt.axes([0.25, 0.3, 0.65, 0.03])
    iter_slider = Slider(ax_iter, 'Iterace', 10, 500, valinit=initial_max_iter, valstep=10)

    # Slidery pro reálnou a imaginární část parametru c
    ax_c_real = plt.axes([0.25, 0.25, 0.3, 0.03])
    c_real_slider = Slider(ax_c_real, 'Re(c)', -1.0, 1.0, valinit=initial_c.real, valstep=0.01)

    ax_c_imag = plt.axes([0.6, 0.25, 0.3, 0.03])
    c_imag_slider = Slider(ax_c_imag, 'Im(c)', -1.0, 1.0, valinit=initial_c.imag, valstep=0.01)

    # Radiobuttony pro výběr colormapy
    ax_colormap = plt.axes([0.025, 0.4, 0.15, 0.15])
    cmap_radio = RadioButtons(ax_colormap, cmap_options, active=0)

    # Radiobuttony pro výběr typu fraktálu
    ax_type = plt.axes([0.025, 0.6, 0.15, 0.1])
    fractal_radio = RadioButtons(ax_type, fractal_type, active=0)

    # Tlačítko pro vykreslení
    ax_button = plt.axes([0.4, 0.15, 0.2, 0.05])
    update_button = Button(ax_button, 'Vykreslit')

    # Tlačítko pro reset zoomu
    ax_reset = plt.axes([0.65, 0.15, 0.2, 0.05])
    reset_button = Button(ax_reset, 'Reset zoom')

    # Uložení aktuálního rozsahu souřadnic
    current_limits = [x_min, x_max, y_min, y_max]

    def update(val=None):
        """
        Překresluje fraktál na základě aktuálních hodnot získaných ze všech ovládacích prvků:
        sliderů (počet iterací, parametr c), radiobuttonů (výběr typu fraktálu a barevného schématu),
        a aktuálního zoomu (výřez oblasti).
        """
        nonlocal image
        max_iter = int(iter_slider.val)
        c = complex(c_real_slider.val, c_imag_slider.val)
        cmap = cmap_radio.value_selected
        selected_type = fractal_radio.value_selected
        x0, x1, y0, y1 = current_limits

        if selected_type == "Mandelbrot":
            new_data = generate_mandelbrot(x0, x1, y0, y1, width, height, max_iter)
            ax.set_title("Mandelbrotova množina")
        else:
            new_data = generate_julia(x0, x1, y0, y1, width, height, c, max_iter)
            ax.set_title(f"Juliova množina (c={c.real:.2f}+{c.imag:.2f}i)")

        image.set_data(new_data)
        image.set_cmap(cmap)
        image.set_extent([x0, x1, y0, y1])
        fig.canvas.draw_idle()

    def on_scroll(event):
        """
        Reaguje na události kolečka myši. Přibližuje nebo oddaluje výřez zobrazení fraktálu
        podle směru kolečka a pozice kurzoru.
        """
        nonlocal current_limits
        base_scale = 0.8

        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None:
            return

        x0, x1, y0, y1 = current_limits
        x_range = (x1 - x0)
        y_range = (y1 - y0)

        scale = base_scale if event.button == 'up' else 1 / base_scale

        new_width = x_range * scale
        new_height = y_range * scale

        new_xmin = xdata - (xdata - x0) * scale
        new_xmax = new_xmin + new_width
        new_ymin = ydata - (ydata - y0) * scale
        new_ymax = new_ymin + new_height

        current_limits = [new_xmin, new_xmax, new_ymin, new_ymax]
        update()

    def reset_zoom(event):
        """
        Nastaví zpět výchozí rozsah souřadnic a překreslí obrázek.
        """
        nonlocal current_limits
        current_limits = [-2.0, 1.0, -1.5, 1.5]
        update()

    # Připojení funkcí k událostem tlačítek a kolečka myši
    update_button.on_clicked(update)
    reset_button.on_clicked(reset_zoom)
    fig.canvas.mpl_connect('scroll_event', on_scroll)

    # Zobrazení interaktivního okna
    plt.show()
