import tkinter as tk
from tkinter import messagebox, ttk
import os  

class RepuloGUI:
    def __init__(self, root, tarsasag):
        self.tarsasag = tarsasag
        self.root = root
        self.root.title(f"{tarsasag.nev} - Repülőjegy Rendszer")
        self.root.geometry("800x600")
        self.root.minsize(750, 480)

        # Színek
        self.colors = {
            "sidebar_bg": "#2c3e50",
            "sidebar_btn": "#34495e",
            "sidebar_active": "#1abc9c",
            "main_bg": "#f5f6fa",
            "card_bg": "#ffffff",
            "text_dark": "#2f3640",
            "text_light": "#ffffff",
            "btn_success": "#2ecc71",
            "btn_danger": "#e74c3c"
        }

        self.root.configure(bg=self.colors["main_bg"])

        # Oldalsáv méretezéssel. 
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar_bg"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Kép beillesztése - remélem már jó
        try:
            # mappakeresés
            aktualis_mappa = os.path.dirname(os.path.abspath(__file__))
            
            kep_utvonal = os.path.join(aktualis_mappa, "airplane.png")

            nyers_kep = tk.PhotoImage(file=kep_utvonal)
            
            # illesztés
            szelesseg = nyers_kep.width()
            if szelesseg > 800:
                self.logo_img = nyers_kep.subsample(6, 6)
            elif szelesseg > 400:
                self.logo_img = nyers_kep.subsample(3, 3)
            elif szelesseg > 180:
                self.logo_img = nyers_kep.subsample(2, 2)
            else:
                self.logo_img = nyers_kep

            self.image_label = tk.Label(self.sidebar, image=self.logo_img, bg=self.colors["sidebar_bg"])
            self.image_label.pack(pady=(25, 5))
        except Exception as e:
            print(f"Grafikus logó (airplane.png) nem található vagy hibás, szöveges mód: {e}")

        # Cím és név vagy mi 
        tk.Label(self.sidebar, text="Airplane (since 1980)", fg=self.colors["text_light"], 
                 bg=self.colors["sidebar_bg"], font=("Helvetica", 18, "bold")).pack(pady=(0, 25))

        # Menügombok
        self._create_menu_btn("Foglalások listája", self.show_listazas)
        self._create_menu_btn("Új jegy foglalása", self.show_foglalas)
        self._create_menu_btn("Foglalás lemondása", self.show_lemondas)

        
        self.main_container = tk.Frame(self.root, bg=self.colors["main_bg"])
        self.main_container.pack(side="right", expand=True, fill="both", padx=25, pady=25)

        # lista
        self.show_listazas()

    def _create_menu_btn(self, text, command):
        btn = tk.Button(self.sidebar, text=text, command=command,
                       bg=self.colors["sidebar_btn"], fg=self.colors["text_light"],
                       font=("Segoe UI", 10, "bold"), relief="flat", activebackground=self.colors["sidebar_active"],
                       activeforeground="white", cursor="hand2", bd=0, pady=14)
        btn.pack(fill="x", pady=5, padx=15)

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_listazas(self):
        self.clear_container()
        
        tk.Label(self.main_container, text="Aktuális foglalások", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self.main_container, bg=self.colors["card_bg"], bd=1, relief="solid", highlightthickness=0)
        card.pack(expand=True, fill="both")

        # foglalások show
        txt = tk.Text(card, font=("Segoe UI", 10), bg=self.colors["card_bg"], fg=self.colors["text_dark"], 
                      relief="flat", wrap="word", padx=15, pady=15)
        scrollbar = ttk.Scrollbar(card, command=txt.yview)
        txt.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        txt.pack(side="left", expand=True, fill="both")

        txt.insert("1.0", self.tarsasag.foglalasok_listazasa())
        txt.config(state="disabled")

    def show_foglalas(self):
        self.clear_container()

        tk.Label(self.main_container, text="Új repülőjegy foglalása", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self.main_container, bg=self.colors["main_bg"])
        form.pack(fill="x", anchor="w")

        def create_field(label_text, placeholder=""):
            tk.Label(form, text=label_text, font=("Segoe UI", 10, "bold"), bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(5, 2))
            entry = tk.Entry(form, font=("Segoe UI", 11), width=40, bd=1, relief="solid")
            entry.pack(anchor="w", ipady=4, pady=(0, 10))
            if placeholder:
                entry.insert(0, placeholder)
            return entry

        e_nev = create_field("Utas teljes neve:")
        e_jsz = create_field("Járatszám (Elérhető: B101, B102, N501):", "B101")
        e_dat = create_field("Utazás dátuma (ÉÉÉÉ-HH-NN):", "2026-06-15")

        def ment():
            eredmeny = self.tarsasag.foglalas_keszites(e_jsz.get(), e_nev.get(), e_dat.get())
            if "Hiba" in eredmeny:
                messagebox.showerror("Hiba történt", eredmeny)
            else:
                messagebox.showinfo("Siker", eredmeny)
                self.show_listazas()

        tk.Button(self.main_container, text="Foglalás rögzítése", command=ment, 
                  bg=self.colors["btn_success"], fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=15)

    def show_lemondas(self):
        self.clear_container()

        tk.Label(self.main_container, text="Foglalás lemondása", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(0, 20))

        form = tk.Frame(self.main_container, bg=self.colors["main_bg"])
        form.pack(fill="x", anchor="w")

        tk.Label(form, text="Utas neve:", font=("Segoe UI", 10, "bold"), bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(5, 2))
        e_nev = tk.Entry(form, font=("Segoe UI", 11), width=40, bd=1, relief="solid")
        e_nev.pack(anchor="w", ipady=4, pady=(0, 10))

        tk.Label(form, text="Járatszám:", font=("Segoe UI", 10, "bold"), bg=self.colors["main_bg"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(5, 2))
        e_jsz = tk.Entry(form, font=("Segoe UI", 11), width=40, bd=1, relief="solid")
        e_jsz.pack(anchor="w", ipady=4, pady=(0, 10))

        def torol():
            eredmeny = self.tarsasag.foglalas_lemondas(e_nev.get(), e_jsz.get())
            if "Hiba" in eredmeny:
                messagebox.showerror("Hiba történt", eredmeny)
            else:
                messagebox.showinfo("Siker", eredmeny)
                self.show_listazas()

        tk.Button(self.main_container, text="Foglalás törlése", command=torol, 
                  bg=self.colors["btn_danger"], fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=15)