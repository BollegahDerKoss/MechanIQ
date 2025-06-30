import tkinter as tk
from PIL import ImageTk, Image

from Aufgabe1_Schnittkraefte import Aufgabe1_Schnittkraefte
from Aufgabe2_Schnittkraefte import Aufgabe2_Schnittkraefte
from Aufgabe3_Schnittkraefte import Aufgabe3_Schnittkraefte


class GUI_Menu:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry("1280x720")
        self.root.title("MechanIQ")

        # Canvas erstellen
        self.canvas = tk.Canvas(self.root, width=1280, height=720, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Hintergrundbild laden und platzieren
        self.bg_image = Image.open("Hintergrund.png").resize((1280, 720))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")

        # Schriftzugbild laden und platzieren
        self.imageSchriftzugMechanIQ = Image.open("Schriftzug_MechanIQ.png").resize((250, 209))
        self.imageSchriftzugMechanIQ_tk = ImageTk.PhotoImage(self.imageSchriftzugMechanIQ)
        self.canvas.create_image(640, 180, image=self.imageSchriftzugMechanIQ_tk, anchor="center")


        # Icon Aufgabe1 laden und resize
        self.imageAuf1 = Image.open("Aufgabe1_Icon.png")
        self.imageAuf1_resized = self.imageAuf1.resize((100, 100))
        self.imageAuf1_tk = ImageTk.PhotoImage(self.imageAuf1_resized)

        # Icon Aufgabe2 laden und resize
        self.imageAuf2 = Image.open("Aufgabe2_Icon.png")
        self.imageAuf2_resized = self.imageAuf2.resize((100, 100))
        self.imageAuf2_tk = ImageTk.PhotoImage(self.imageAuf2_resized)

        # Icon Aufgabe3 laden und resize
        self.imageAuf3 = Image.open("Aufgabe3_Icon.png")
        self.imageAuf3_resized = self.imageAuf3.resize((100, 100))
        self.imageAuf3_tk = ImageTk.PhotoImage(self.imageAuf3_resized)

        # Button Aufgabe 1
        self.btnAuf1 = tk.Button(self.root, image=self.imageAuf1_tk, command=self.oeffneAufgabe1)
        self.btnAuf1.place(relx=0.3, rely=0.5, anchor="center")

        # Button Aufgabe 2
        self.btnAuf2 = tk.Button(self.root, image=self.imageAuf2_tk, command=self.oeffneAufgabe2)
        self.btnAuf2.place(relx=0.5, rely=0.5, anchor="center")

        # Button Aufgabe 3
        self.btnAuf3 = tk.Button(self.root, image=self.imageAuf3_tk, command=self.oeffneAufgabe3)
        self.btnAuf3.place(relx=0.7, rely=0.5, anchor="center")


        # Hauptfenster daher mainloop()
        self.root.mainloop()

    def oeffneAufgabe1(self):
        # Toplevel bekommt master übergeben
        Aufgabe1_Schnittkraefte(master=self.root)
        # Versteckt das Fenster, ohne es komplett zu schließen
        self.root.withdraw()

    def oeffneAufgabe2(self):
        # Toplevel bekommt master übergeben
        Aufgabe2_Schnittkraefte(master=self.root)
        # Versteckt das Fenster, ohne es komplett zu schließen
        self.root.withdraw()

    def oeffneAufgabe3(self):
        # Toplevel bekommt master übergeben
        Aufgabe3_Schnittkraefte(master=self.root)
        # Versteckt das Fenster, ohne es komplett zu schließen
        self.root.withdraw()


# Hauptprogramm starten
if __name__ == "__main__":
    GUI_Menu()
