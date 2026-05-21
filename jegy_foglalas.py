class JegyFoglalas:
    def __init__(self, utas_neve, jarat, datum):
        self._utas_neve = utas_neve
        self._jarat = jarat
        self._datum = datum

    @property
    def utas_neve(self):
        return self._utas_neve

    @property
    def jarat(self):
        return self._jarat

    @property
    def datum(self):
        return self._datum

    def __str__(self):
        return f"Utas: {self._utas_neve} | Járat: {self._jarat.jaratszam} ({self._jarat.get_tipus()}) -> {self._jarat.celallomas} | Dátum: {self._datum} | Ár: {self._jarat.jegyar} Ft"