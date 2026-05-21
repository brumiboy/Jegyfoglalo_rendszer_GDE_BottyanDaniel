import tkinter as tk
from legi_tarsasag import LegiTarsasag
from belfoldi_jarat import BelfoldiJarat
from nemzetkozi_jarat import NemzetkoziJarat
from gui import RepuloGUI

def rendszer_inicializalas():
    
    tarsasag = LegiTarsasag("AirPlane!")

    
    j1 = BelfoldiJarat("B101", "Debrecen", 14500)
    j2 = BelfoldiJarat("B102", "Szeged", 11900)
    j3 = NemzetkoziJarat("N501", "Párizs", 48000)

    tarsasag.jarat_hozzaad(j1)
    tarsasag.jarat_hozzaad(j2)
    tarsasag.jarat_hozzaad(j3)

    
    tarsasag.foglalas_keszites("B101", "Kovács András Péter", "2026-06-15")
    tarsasag.foglalas_keszites("B101", "Bottyán Dániel", "2026-06-20")
    tarsasag.foglalas_keszites("B102", "Id. Adalbert ", "2026-07-02")
    tarsasag.foglalas_keszites("N501", "Kiss Gutya", "2026-08-12")
    tarsasag.foglalas_keszites("N501", "II. Pál", "2026-08-14")
    tarsasag.foglalas_keszites("B102", "Ali Ann", "2026-09-01")

    return tarsasag

if __name__ == "__main__":
    
    aeroline = rendszer_inicializalas()

    
    root = tk.Tk()
    app = RepuloGUI(root, aeroline)
    root.mainloop()