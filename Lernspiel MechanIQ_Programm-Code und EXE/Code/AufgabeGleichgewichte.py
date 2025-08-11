

class AufgabeGleichgewichte:

    def __init__(self, LoesungFY, LoesungFX, LoesungMoment):
        # private Variablen (mit __ geschützt)
        self.__LoesungFY = LoesungFY
        self.__LoesungFX = LoesungFX
        self.__LoesungMoment = LoesungMoment


    # Getter-Methoden
    def get_LoesungFY(self):
        return self.__LoesungFY

    def get_LoesungFX(self):
        return self.__LoesungFX

    def get_LoesungMoment(self):
        return self.__LoesungMoment




