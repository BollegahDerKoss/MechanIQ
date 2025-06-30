

class AufgabeSchnittkraefte:

    def __init__(self, aufgabenstellung, loesung):

        # private Variablen (mit __ geschützt)
        self.__aufgabenstellung = aufgabenstellung
        self.__loesung = loesung  # Richtige Antwortoption ("A", "B" oder "C")


    def getAufgabenstellungText(self):
        return self.__aufgabenstellung

    def getLoesung(self):
        return self.__loesung