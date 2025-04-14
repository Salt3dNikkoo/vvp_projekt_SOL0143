# vvp_projekt_SOL0143

# Vizualizace fraktálů

## Textový popis

Tento projekt se zaměřuje na vizualizaci fraktálů. Cílem je
implementovat algoritmy pro efektivní generování známých fraktálů, jako
jsou Mandelbrotova a Juliova množina (pro
$f\left(z\right)=z^{2}+c,c\in\mathbb{C}$), a vytvořit interaktivní
vizualizace (viz [Matplotlib
widgets](https://matplotlib.org/stable/gallery/widgets/index.html))
těchto fraktálů pomocí knihovny Matplotlib. Možností je také využít knihovnu [Pygame](https://www.pygame.org/news) pro vytvoření interaktivních vizualizací.

Výstupem projektu budou interaktivní vizualizace fraktálů, které
umožňují uživateli prozkoumávat různé části fraktálu a přizpůsobovat
parametry pro generování fraktálů ($c\in\mathbb{C}$ pro Juliovu
množinu).

## Funkcionality

- Implementovat algoritmus pro efektivní generování Mandelbrotovy
  množiny pomocí knihoven NumPy a Numba
- Implementovat algoritmus pro efektivní generování Juliovy množiny
  (pro $f\left(z\right)=z^{2}+c,c\in\mathbb{C}$) pomocí knihoven NumPy a Numba
- Vytvořit funkci pro vizualizaci fraktálů pomocí knihovny Matplotlib,
  která zobrazuje fraktály pomocí barevného mapování podle iterací
  potřebných k dosažení určitého prahu
- Implementovat interaktivní prvky vizualizace, které umožňují
  uživateli (v případě implementace skrze Pygame lze nahradit ovladáním klávesnicí a myší):
  - přiblížit nebo oddálit fraktál
  - měnit barevné schéma vykreslení počtu iterací do divergence
  - přizpůsobovat parametry pro generování fraktálů (např. počet
    iterací, $c$)
