from datetime import datetime
from jegy_foglalas import JegyFoglalas

class LegiTarsasag:
    def __init__(self, nev):
        self._nev = nev
        self._jaratok = []
        self._foglalasok = []

    @property
    def nev(self):
        return self._nev

    @property
    def jaratok(self):
        return self._jaratok

    @property
    def foglalasok(self):
        return self._foglalasok

    def jarat_hozzaad(self, jarat):
        self._jaratok.append(jarat)

    def foglalas_keszites(self, jaratszam, utas_neve, datum_str):
        # üres mezők ellenőrzése
        if not utas_neve.strip() or not jaratszam.strip() or not datum_str.strip():
            return "Hiba: Minden mezőt kötelező kitölteni!"

        # 2. adatok, dátumok
        try:
            datum_obj = datetime.strptime(datum_str, "%Y-%m-%d")
            if datum_obj.date() < datetime.now().date():
                return "Hiba: Nem foglalhatsz múltbeli dátumra!"
        except ValueError:
            return "Hiba: Érvénytelen dátumformátum! Kérjük, használja az ÉÉÉÉ-HH-NN formátumot."

        # 3. Adatok járatok 
        valasztott_jarat = next((j for j in self._jaratok if j.jaratszam == jaratszam), None)
        if not valasztott_jarat:
            return f"Hiba: A '{jaratszam}' számú járat nem létezik a rendszerben!"

        # Adat OK mentés. Minden oké mindenki örül nyaralás ON
        uj_foglalas = JegyFoglalas(utas_neve.strip(), valasztott_jarat, datum_str)
        self._foglalasok.append(uj_foglalas)
        return f"Sikeres foglalás!\nUtas: {utas_neve}\nFizetendő összeg: {valasztott_jarat.jegyar} Ft"

    def foglalas_lemondas(self, utas_neve, jaratszam):
        if not utas_neve.strip() or not jaratszam.strip():
            return "Hiba: A lemondáshoz adja meg a nevet és a járatszámot is!"

        # Valid foglalás lemondása és csak felkiáltójel
        for f in self._foglalasok:
            if f.utas_neve.lower() == utas_neve.strip().lower() and f.jarat.jaratszam == jaratszam.strip():
                self._foglalasok.remove(f)
                return f"Sikeres lemondás: {utas_neve} foglalása a {jaratszam} járatra törölve."
        
        return "Hiba: Nem található ilyen foglalás a megadott névvel és járatszámmal!"

    def foglalasok_listazasa(self):
        if not self._foglalasok:
            return "Jelenleg nincsenek aktív foglalások a rendszerben."
        return "\n\n".join([str(f) for f in self._foglalasok])