import tkinter as tk
from tkinter import messagebox, simpledialog

from PIL import ImageTk, Image
from collections import Counter
import re
from openai import OpenAI

from AufgabeGleichgewichte import AufgabeGleichgewichte


# OpenAI API-Key aufrufen
api_key = "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"
client = OpenAI(api_key=api_key)


class Aufgabe3_Gleichgewichte:

    def __init__(self, master=None):

        self.aufgabe = AufgabeGleichgewichte("A_y + B_y - F1", "A_x", "-(F1 * a) + (B_y * b)")

        self.master = master # ← speichert das letzte Fenster (Schnittkräfte)

        self.Aufg3_GleichGUI = tk.Toplevel(master)
        self.Aufg3_GleichGUI.resizable(False, False)
        self.Aufg3_GleichGUI.title("Level 3.2 - Gleichgewichte")
        self.Aufg3_GleichGUI.geometry("1280x720")  # Diese Fenstergröße passt für alle Bildschirme ab 13"


        # Hintergrundbild laden und skalieren
        self.bg_image = Image.open("Hintergrund.png")
        self.bg_image_resized = self.bg_image.resize((1280, 720))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_resized)

        # Canvas erstellen und platzieren
        self.canvas = tk.Canvas(self.Aufg3_GleichGUI, width=1280, height=720, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Hintergrundbild ins Canvas zeichnen (oben links)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor='nw')

        # Bild der Aufgabe laden und skalieren
        self.bildAufgabe = Image.open("GL3_Aufgabenstellung.png").resize((700, 400))
        self.bildAufgabe_tk = ImageTk.PhotoImage(self.bildAufgabe)
        self.canvas.create_image(460, 60, image=self.bildAufgabe_tk, anchor="nw")

        # Aufgabennummer auf Canvas
        self.canvas.create_text(830, 30, text="Level 3.2 - Gleichgewichte", font=("Helvetica", 18, "bold"), fill="black")

        # Texte direkt auf Canvas (wie Label früher)
        self.canvas.create_text(520, 465, anchor="nw",text="Bitte folgende Konvention bei der Eingabe der Variablen nutzen: A_y, F1, FB, -(B_y*b)",font=("Arial", 12), fill="black")

        self.canvas.create_text(450, 520, anchor="nw", text="Kräftegleichgewicht in y-Richtung:  0 =", font=("Arial", 12),fill="black")

        self.canvas.create_text(450, 580, anchor="nw", text="Kräftegleichgewicht in x-Richtung:  0 =", font=("Arial", 12),fill="black")

        self.canvas.create_text(430, 640, anchor="nw", text="Momentengleichgewicht um Punkt A:  0 =", font=("Arial", 12),fill="black")

        # Eingabe und Buttons platzieren
        self.eingabeFY = tk.Entry(self.Aufg3_GleichGUI, width=30, font=("Arial", 16))
        self.eingabeFY.place(relx=0.56, rely=520 / 720)

        self.btnFY = tk.Button(self.Aufg3_GleichGUI, text="Absenden", command=self.checkLoesungFY)
        self.btnFY.place(relx=0.85, rely=520 / 720)

        self.ergebnisLabelFY = tk.Label(self.Aufg3_GleichGUI, text="", font=("Arial", 12), bg="#ffffff")
        self.ergebnisLabelFY.place(relx=0.56, rely=550 / 720)

        self.eingabeFX = tk.Entry(self.Aufg3_GleichGUI, width=30, font=("Arial", 16))
        self.eingabeFX.place(relx=0.56, rely=580 / 720)

        self.btnFX = tk.Button(self.Aufg3_GleichGUI, text="Absenden", command=self.checkLoesungFX)
        self.btnFX.place(relx=0.85, rely=580 / 720)

        self.ergebnisLabelFX = tk.Label(self.Aufg3_GleichGUI, text="", font=("Arial", 12), bg="#ffffff")
        self.ergebnisLabelFX.place(relx=0.56, rely=610 / 720)

        self.eingabeM = tk.Entry(self.Aufg3_GleichGUI, width=30, font=("Arial", 16))
        self.eingabeM.place(relx=0.56, rely=640 / 720)

        self.btnM = tk.Button(self.Aufg3_GleichGUI, text="Absenden", command=self.checkLoesungM)
        self.btnM.place(relx=0.85, rely=640 / 720)

        self.ergebnisLabelM = tk.Label(self.Aufg3_GleichGUI, text="", font=("Arial", 12), bg="#ffffff")
        self.ergebnisLabelM.place(relx=0.56, rely=670 / 720)

        self.btnBackToMenu = tk.Button(self.Aufg3_GleichGUI, text="Menü", command=self.backToMenu, font=("Verdana", 12, "bold"), bg="white")
        self.btnBackToMenu.place(x=1270, y=15, anchor='ne')

        self.chatfenster_hinzufuegen()


    def backToMenu(self):
            self.Aufg3_GleichGUI.destroy()  # Aufgabe-Fenster schließen
            if self.master:  # Wenn master (Menü) existiert:
                self.master.deiconify()  # Wieder anzeigen

    def checkLoesungFY(self):
        benutzer_eingabe = self.eingabeFY.get()  # Text aus Entry-Feld holen
        richtige_loesung = self.aufgabe.get_LoesungFY()

        # DEBUG-Ausgabe:
        print("Eingabe zerlegt:", self.zerlege(benutzer_eingabe))
        print("Lösung zerlegt:", self.zerlege(richtige_loesung))

        # Counter -> Vergleich unabhängig der Reihenfolge der Eingabe
        if Counter(self.zerlege(benutzer_eingabe)) == Counter(self.zerlege(richtige_loesung)):
            self.ergebnisLabelFY.config(text="Richtig!")
        else:
            self.ergebnisLabelFY.config(text="Leider falsch... versuche es noch einmal!")

    def checkLoesungFX(self):
        benutzer_eingabe = self.eingabeFX.get()  # Text aus Entry-Feld holen
        richtige_loesung = self.aufgabe.get_LoesungFX()

        # DEBUG-Ausgabe:
        print("Eingabe zerlegt:", self.zerlege(benutzer_eingabe))
        print("Lösung zerlegt:", self.zerlege(richtige_loesung))

        # Counter -> Vergleich unabhängig der Reihenfolge der Eingabe
        if Counter(self.zerlege(benutzer_eingabe)) == Counter(self.zerlege(richtige_loesung)):
            self.ergebnisLabelFX.config(text="Richtig!")
        else:
            self.ergebnisLabelFX.config(text="Leider falsch... versuche es noch einmal!")

    def checkLoesungM(self):
        benutzer_eingabe = self.eingabeM.get()  # Text aus Entry-Feld holen
        richtige_loesung = self.aufgabe.get_LoesungMoment()

        # DEBUG-Ausgabe:
        print("Eingabe zerlegt:", self.zerlege(benutzer_eingabe))
        print("Lösung zerlegt:", self.zerlege(richtige_loesung))

        # Counter -> Vergleich unabhängig der Reihenfolge der Eingabe
        if Counter(self.zerlege(benutzer_eingabe)) == Counter(self.zerlege(richtige_loesung)):
            self.ergebnisLabelM.config(text="Richtig!")
        else:
            self.ergebnisLabelM.config(text="Leider falsch... versuche es noch einmal!")


    # Methode zum Zerlegen des Ausdrucks in Terme mit Vorzeichen
    def zerlege(self, gleichung):
        gleichung = gleichung.replace(" ", "")
        # Wenn der Ausdruck nicht mit + oder - beginnt, setze + davor (damit jedes Element ein Vorzeichen hat)
        if gleichung[0] not in '+-':
            gleichung = '+' + gleichung
        # Mit regex alle Terme mit Vorzeichen extrahieren
        return re.findall(r'[+-][^+-]+', gleichung)


    # --- KI BOT ---
    def chatfenster_hinzufuegen(self, verlauf=""):
        if hasattr(self, 'chat_frame') and self.chat_frame:
            self.chat_frame.destroy()

        self.chat_frame = tk.Frame(self.Aufg3_GleichGUI, bg="#7b4be6", bd=1, relief=tk.GROOVE)
        self.chat_frame.place(relx=0.01, rely=0.05, width=390, height=650)

        scrollbar = tk.Scrollbar(self.chat_frame)
        scrollbar.place(relx=1.0, rely=0.0, relheight=0.85, anchor='ne')

        self.chat_display = tk.Text(
            self.chat_frame, wrap=tk.WORD, height=7, state=tk.NORMAL,
            bg="white", font=("Helvetica", 10), yscrollcommand=scrollbar.set
        )
        self.chat_display.insert(tk.END, verlauf)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.place(relx=0, rely=0, relwidth=0.97, relheight=0.85)
        scrollbar.config(command=self.chat_display.yview)

        input_frame = tk.Frame(self.chat_frame, bg="#7b4be6")
        input_frame.place(relx=0.01, rely=0.9, relwidth=0.99, relheight=0.06)

        # chat_entry mit place
        self.chat_entry = tk.Entry(input_frame, font=("Helvetica", 10))
        self.chat_entry.place(relx=0.0, rely=0.1, relwidth=0.75, relheight=0.8)
        self.chat_entry.bind("<Return>", lambda event: self.kitutor())

        # send_button mit place
        self.send_button = tk.Button(input_frame, text="KI-Bot fragen", command=self.kitutor)
        self.send_button.place(relx=0.77, rely=0.1, relwidth=0.22, relheight=0.8)

    def kitutor(self):
        frage = self.chat_entry.get()
        if not frage.strip():
            return
        self.chat_entry.delete(0, tk.END)

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"Du: {frage}\n", "user")
        self.chat_display.tag_config("user", foreground="darkblue", font=("Verdana", 10, "bold"))
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein KI-Tutor für Mechanik 1 und sollst Probleme mit praxisnahen Beispielen erklären."},
                    {"role": "user", "content": frage}
                ],
                max_tokens=600,
                temperature=0.5
            )
            antwort = response.choices[0].message.content

            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"KI-Bot: {antwort}\n\n", "ki")
            self.chat_display.tag_config("ki", foreground="black", font=("Verdana", 11))
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)

        except Exception as e:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"[Fehler]: {e}\n", "error")
            self.chat_display.tag_config("error", foreground="red")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)





