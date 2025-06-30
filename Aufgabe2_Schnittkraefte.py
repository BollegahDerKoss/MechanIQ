import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from openai import OpenAI

from AufgabeSchnittkraefte import AufgabeSchnittkraefte
from Aufgabe2_Gleichgewichte import Aufgabe2_Gleichgewichte

api_key = "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"
client = OpenAI(api_key=api_key)

class Aufgabe2_Schnittkraefte:

    def __init__(self, master=None):

        self.aufgabe = AufgabeSchnittkraefte("Wähle das korrekte Freikörperbild!", "C")

        self.master = master
        self.Aufg2_SchnittGUI = tk.Toplevel(master)
        self.Aufg2_SchnittGUI.resizable(False, False)
        self.Aufg2_SchnittGUI.title("Level 2.1 - Schnittkraefte")
        self.Aufg2_SchnittGUI.geometry("1280x720")

        # Hintergrundbild laden und skalieren
        self.bg_image = Image.open("Hintergrund.png")
        self.bg_image_resized = self.bg_image.resize((1280, 720))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image_resized)

        # Canvas erstellen und platzieren
        self.canvas = tk.Canvas(self.Aufg2_SchnittGUI, width=1280, height=720, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Hintergrundbild ins Canvas zeichnen (oben links)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor='nw')

        # Texte auf Canvas platzieren
        self.canvas.create_text(830, 30, text="Level 2.1 - Freikörperbild", font=("Helvetica", 18, "bold"), fill="black")
        self.canvas.create_text(830, 70, text=self.aufgabe.getAufgabenstellungText(), font=("Verdana", 12), fill="black", width=400)

        # Bild der Aufgabe laden
        self.bildAufgabe = Image.open("SK2_Aufgabenstellung.png")
        self.bildAufgabe_resized = self.bildAufgabe.resize((750, 420))
        self.bildAufgabe_tk = ImageTk.PhotoImage(self.bildAufgabe_resized)

        # Bild im Canvas anzeigen
        self.canvas.create_image(830, 100, image=self.bildAufgabe_tk, anchor='n')

        # Button Menü
        self.btnBackToMenu = tk.Button(self.Aufg2_SchnittGUI, text="Menü", command=self.backToMenu, font=("Verdana", 12, "bold"), bg="white")
        self.btnBackToMenu.place(x=1270, y=15, anchor='ne')

        # Antwortbilder laden
        self.bilder = {}
        for name in ["a", "b", "c"]:
            try:
                img = Image.open(f"SK2_Antwort_{name}.png").resize((200, 150))
                self.bilder[name.upper()] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                self.bilder[name.upper()] = None
                # Fehlermeldung direkt als Canvas-Text anzeigen
                self.canvas.create_text(830, 600 + 30 * (ord(name) - ord('a')),
                                        text=f"Bild SK2_Antwort_{name}.png fehlt!", fill="red", font=("Helvetica", 10))

        # Antwort-Buttons auf Canvas platzieren (über dem Canvas, deshalb mit place)
        x_start = 600
        spacing = 230
        y_buttons = 550
        for i, name in enumerate(["A", "B", "C"]):
            if self.bilder[name]:
                btn = tk.Button(self.Aufg2_SchnittGUI, image=self.bilder[name], command=lambda n=name: self.pruefe_aufgabe(n))
                btn.place(x=x_start + i * spacing, y=y_buttons, anchor='n')

        # Chatfenster hinzufügen
        self.chatfenster_hinzufuegen()

    def pruefe_aufgabe(self, auswahl):
        korrekt = self.aufgabe.getLoesung()
        if auswahl == korrekt:
            messagebox.showinfo("Richtig", "Richtig! Weiter zu den Gleichgewichten!")
            self.oeffneAufgabeGleichgewichte()
        else:
            messagebox.showwarning("Falsch", "Leider falsch. Versuche es noch einmal!")

    def oeffneAufgabeGleichgewichte(self):
        Aufgabe2_Gleichgewichte(master=self.master)
        self.Aufg2_SchnittGUI.withdraw()

    def backToMenu(self):
        self.Aufg2_SchnittGUI.destroy()
        if self.master:
            self.master.deiconify()

    def chatfenster_hinzufuegen(self, verlauf=""):
        if hasattr(self, 'chat_frame') and self.chat_frame:
            self.chat_frame.destroy()

        self.chat_frame = tk.Frame(self.Aufg2_SchnittGUI, bg="#7b4be6", bd=1, relief=tk.GROOVE)
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
            self.chat_display.tag_config("ki", foreground="black",font=("Verdana", 11))
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)

        except Exception as e:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"[Fehler]: {e}\n", "error")
            self.chat_display.tag_config("error", foreground="red")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
